from multiprocessing.managers import RemoteError
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import telepot
import time



class KTX_Korail():
    def __init__(self):
        super().__init__()
        self.korail_id = None
        self.korail_pw = None
        self.error = None
        self.chat_id = None
        _token = "5662385841:AAE9oTJX9INCPqCGhdzBGdSnLJ-qvq3OB0c"

        self.bot = telepot.Bot(_token)

    def login(self):
        try:
            self.driver = webdriver.Firefox()
            self.driver.get("https://www.letskorail.com/korail/com/login.do")
            time.sleep(1)
            self.driver.find_element(By.ID, "txtMember").send_keys(self.korail_id)
            self.driver.find_element(By.ID, "txtPwd").send_keys(self.korail_pw)

            self.driver.find_element(By.XPATH, '//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, "h3.first > a:nth-child(1) > img:nth-child(1)").click()
        except UnexpectedAlertPresentException:
            self.driver.close()
            return "error_login"
        
        return "error_none"

    def sendMessage(self, msg):
        self.bot.sendMessage(self.chat_id, msg)

    #출발지 입력
    def korail_start_city(self, city):
        _start_city = self.driver.find_element(By.ID,"start")
        _start_city.clear()
        _start_city.send_keys(city)
        _start_city.send_keys(Keys.RETURN)
        return "error_none"

    #도착지 입력
    def korail_arrival_city(self, city):
        _arrival_city = self.driver.find_element(By.ID,"get")
        _arrival_city.clear()
        _arrival_city.send_keys(city)
        _arrival_city.send_keys(Keys.RETURN)
        return "error_none"

    #년 선택
    def korail_year_select(self, year):
        _year_select = Select(self.driver.find_element(By.ID,"s_year"))
        _year_select.select_by_value(year)
        return "error_none"

    #월 선택
    def korail_month_select(self, month):
        _month_select = Select(self.driver.find_element(By.ID,"s_month"))
        _month_select.select_by_value(month)
        return "error_none"

    #일 선택
    def korail_day_select(self, day):
        _day_select = Select(self.driver.find_element(By.ID,"s_day"))
        _day_select.select_by_value(day)
        return "error_none"

    #시간 선택
    def korail_hour_select(self, hour):
        _hour_select = Select(self.driver.find_element(By.ID,"s_hour"))
        _hour_select.select_by_value(hour)  
        return "error_none" 

    def korail_search(self):
        _departure = self.driver.find_element(By.XPATH,'//*[@id="start"]').get_attribute("value")
        _arrival   = self.driver.find_element(By.XPATH,'//*[@id="get"]').get_attribute("value")
        print(_departure,_arrival)
        self.sendMessage(f"{_departure}에서 {_arrival}가는 시간표를 검색합니다. 잠시만 기다려주세요.")

        self.driver.find_element(By.CSS_SELECTOR, ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        time.sleep(1)
        _ktx_list = []
        for index_seq in range(1,11):
            try:
                _ktx_list.append("["+str(index_seq)+"]")
                _ktx_list.append(self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[3]" % index_seq).text)
                _ktx_list.append(self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[4]" % index_seq).text)
                try:
                    _ktx_list.append(self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[6]/img" % index_seq).get_attribute("alt"))
                except:
                    _ktx_list.append(self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[6]/a[1]/img" % index_seq).get_attribute("alt"))
                _ktx_list.append("---------------")
            except:
                _ktx_list.append("해당시간 이후의 기차표는 없습니다.")

        ktx_info = '\n'.join(_ktx_list)
        #telegram_message = {'chat': {'id': 챗봇의 id값}, 'text': '결과'}
        if len(ktx_info) == 0:
            self.sendMessage("오류가 발생했습니다. [검색]을 다시 입력해주세요.")
        else:
            self.sendMessage(ktx_info)
            self.sendMessage("예약하고자 하는 번호를 아래 예시와 같이 입력하세요.\n예) 예약5")

    def ticket_reservation(self, index_seq):
        #from tel.telegram import KTX_Telegram
        _is_reserve = None
        _reserveCnt = 0
        self.sendMessage("성공할때까지 예약을 반복합니다. 취소는 불가능합니다.")
        while True:
            #self.sendMessage("[%d]번째 예약을 시도합니다." % _reserveCnt+1)
            time.sleep(1)
            try:
                _is_reserve = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[6]/a[1]/img" % index_seq).get_attribute("alt")
                if _is_reserve == "예약하기":
                    self.driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[%s]/td[6]/a[1]/img" % index_seq).click()
                    #telegram_message = {'chat': {'id': "goodsell_korail_bot"}, 'text': '예약완료'}
                    time.sleep(2)
                    try:
                        _sancheon_popup_iframe = self.driver.find_element(By.ID, "embeded-modal-traininfo")
                        self.driver.switch_to.frame(_sancheon_popup_iframe)
                        self.driver.find_element(By.XPATH, "/html/body/div/div[2]/p[3]/a").click()
                        time.sleep(2)
                    finally:
                        _alert = self.driver.switch_to.alert
                        _alert.accept()
                        self.sendMessage('예약이 완료되었습니다.\n[필수] 코레일톡 어플을 실행하고 三 표시를 누른 뒤, 아래 "예약 승차권 조회 ● 취소"를 눌러 결제를 진행해주세요.')
                        time.sleep(1)
            except NoSuchElementException:
                _reserveCnt += 1
                self.driver.find_element(By.CSS_SELECTOR, ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
                time.sleep(1)
                self.driver.switch_to.alert.accept()