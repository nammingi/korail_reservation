# *은 tel폴더 telegram.py 파일의 모든 클래스, 함수를 호출한다.
from tel.telegram import *

class KTX_Main():
    def __init__(self):
        print('KTX 예매 시작')
        KTX_Telegram()

#해당 __init__.py 파일에서 실행했을경우 KTX_Main() 클래스가 실행됨
if __name__ == "__main__":
    KTX_Main()