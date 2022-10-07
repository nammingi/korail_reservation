import re
import telepot
from kor.korail import *
import time

class KTX_Telegram():
    def __init__(self):
        print('텔레그램 시작합니다.')
        self.token = "5662385841:AAE9oTJX9INCPqCGhdzBGdSnLJ-qvq3OB0c"
        self.bot = telepot.Bot(self.token)
        self.korail = KTX_Korail()
        self.bot.message_loop(self.conversation_telegram)
        while True:
            pass

    def sendMessage(self, msg):
        self.bot.sendMessage(self.chat_id, msg)

    def conversation_telegram(self, msg, result = None):
        self.chat_id = msg['chat']['id']
        self.korail.chat_id = self.chat_id
        con_text = msg['text']
        if con_text == '로그인':
            if not self.korail.korail_id or not self.korail.korail_pw:
                self.sendMessage("아래 예시를 참고하여 아이디와 비밀번호를 입력해주세요. \n 예) id1234567890 pw12345")
                self.korail.korail_id = None
                self.korail.korail_pw = None
            else:
                self.sendMessage("로그인중입니다. 잠시만 기다려주세요")
                retValue = self.korail.login()

                print(retValue)
                if retValue=="error_none":
                    self.sendMessage("로그인이 정상적으로 완료되었습니다.\n출발지와 도착지를 설정합니다. 아래 예시와 같이 입력해주세요. \n 예) 출발서울\n예) 도착대전\n또한 원하시는 날짜와 시간이 있다면 입력해주세요. 미입력시 현재 시간을 기준으로 합니다.\n예) 05일\n예) 02시\n모두 입력 후 [검색]을 입력하세요.")
                elif retValue == "error_login":
                    self.sendMessage("코레일 멤버십에 등록되지 않은 정보이거나 회원번호(이메일/휴대전화) 또는 비밀번호를 잘못 입력하셨습니다.")
                    retValue = "error_none"

        start_city = re.compile("출발*")
        start_city_find = re.compile("[^출발]")

        #목적지 설정을 위한 정규표현식
        arrival_city = re.compile("도착*")
        arrival_city_find = re.compile("[^도착]")

        #년을 선택하기 위한 정규표현식
        year_select = re.compile("202\d{1}년")
        year_select_find = re.compile("[^년]")

        #월을 선택하기 위한 정규표현식
        month_select = re.compile("[0-9]+월")
        month_select_find = re.compile("[^월]")

        #일을 선택하기 위한 정규표현식
        day_select = re.compile("[0-9]+일")
        day_select_find = re.compile("[^일]")

        #시간을 선택하기 위한 정규표현식
        hour_select = re.compile("[0-9]+시")
        hour_select_find = re.compile("[^시]")

        ticket_reservation = re.compile("예약[0-9]")
        ticket_reservation_find = re.compile("[^예약]")
        
        if start_city.match(con_text):
            start_city_name = start_city_find.findall(con_text)
            start_city_name = ''.join(start_city_name)
            _retValue = self.korail.korail_start_city(start_city_name)
            if _retValue == "error_none":
                self.sendMessage("{}에서 출발합니다.".format(start_city_name))


        if arrival_city.match(con_text):
            arrival_city_name = arrival_city_find.findall(con_text)
            arrival_city_name = ''.join(arrival_city_name)
            _retValue = self.korail.korail_arrival_city(arrival_city_name)
            if _retValue == "error_none":
                self.sendMessage("도착지는 {} 입니다.".format(arrival_city_name))

        if year_select.match(con_text):
            year_select_name = year_select_find.findall(con_text)
            year_select_name = ''.join(year_select_name)
            _retValue = self.korail.korail_year_select(year_select_name)
            if _retValue == "error_none":
                self.sendMessage("{}년으로 설정되었습니다.".format(year_select_name))

        if month_select.match(con_text):
            month_select_name = month_select_find.findall(con_text)
            month_select_name = ''.join(month_select_name)
            _retValue = self.korail.korail_month_select(month_select_name)
            if _retValue == "error_none":
                self.sendMessage("{}월로 설정되었습니다.".format(month_select_name))

        if day_select.match(con_text):
            day_select_name = day_select_find.findall(con_text)
            day_select_name = ''.join(day_select_name)
            _retValue = self.korail.korail_day_select(day_select_name)
            if _retValue == "error_none":
                self.sendMessage("{}일로 설정되었습니다.".format(day_select_name))

        if hour_select.match(con_text):
            hour_select_name = hour_select_find.findall(con_text)
            hour_select_name = ''.join(hour_select_name)
            _retValue = self.korail.korail_hour_select(hour_select_name)
            if _retValue == "error_none":
                self.sendMessage("{}시로 설정되었습니다.".format(hour_select_name))
        
        if ticket_reservation.match(con_text):
            
            index_seq = ticket_reservation_find.findall(con_text)
            index_seq = ''.join(index_seq)
            self.sendMessage("{}번 시간대 예약을 시작합니다.".format(index_seq))
            self.korail.ticket_reservation(index_seq)

        if "분" in con_text:
            self.sendMessage("분은 설정할 수 없습니다.")

        if con_text[:2] == "id":
            self.korail.korail_id = con_text[2:].split(" pw")[0]
            self.korail.korail_pw = con_text[2:].split(" pw")[1]
            self.sendMessage("아이디와 비밀번호가 설정되었습니다. [로그인]을 입력하여 로그인하세요.")

        if con_text == "검색":
            self.korail.korail_search()

        if con_text == "결과":
            self.token = "5662385841:AAE9oTJX9INCPqCGhdzBGdSnLJ-qvq3OB0c"
            self.bot = telepot.Bot(self.token)
            self.sendMessage(result)
            
        if con_text == "debug_test":
            self.korail.korail_id = "1676456612"
            self.korail.korail_pw = "administ12!"

            if not self.korail.korail_id or not self.korail.korail_pw:
                self.sendMessage("아이디와 비밀번호를 입력해주세요. \n 예) id1234567890pw12345")
                self.korail.korail_id = None
                self.korail.korail_pw = None
            else:
                self.sendMessage("로그인중입니다. 잠시만 기다려주세요")
                retValue = self.korail.login()
                if retValue=="error_none":
                    self.sendMessage("로그인이 정상적으로 완료되었습니다.\n예약 페이지를 불러오고 있습니다. 잠시만 기다려주세요.")
                elif retValue == "error_login":
                    self.sendMessage("코레일 멤버십에 등록되지 않은 정보이거나 회원번호(이메일/휴대전화) 또는 비밀번호를 잘못 입력하셨습니다.")
                    retValue = "error_none"
        if ("help" in con_text)or("머" in con_text)or("어케" in con_text)or("시작" in con_text)or("start" in con_text):
            self.sendMessage("[[코레일 자동 예매 봇입니다.]]\n - 사용하기 위해서 코레일톡(레츠코레일) 계정이 필요합니다.\n - 계정이 없다면 먼저 어플 혹은 홈페이지에 접속하여 회원가입을 진행하세요.\n - 계정이 있다면 채팅창에 [로그인]을 입력하여 id와 pw를 양식에 맞게 입력하세요.")
            pass

        """    def sendMessage(self, chat_id, text,
                    parse_mode=None,
                    disable_web_page_preview=None,
                    disable_notification=None,
                    reply_to_message_id=None,
                    reply_markup=None):
        #See: https://core.telegram.org/bots/api#sendmessage 
        p = _strip(locals())
        return self._api_request('sendMessage', _rectify(p))"""
        