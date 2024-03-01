import sys, asyncio, json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from qasync import QEventLoop, asyncSlot

import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

form_class = uic.loadUiType("31. MainWindow.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self, loop=None):
        """생성자"""
        super().__init__()
        self.setupUi(self)
        self.api = ebest.OpenApi()
        
        self.text_itemcode.setPlainText("005930")
        self.btn_login.clicked.connect(self.func_login)
        self.btn_reqInfo.clicked.connect(self.func_req_itemInfo)
        self.btn_chart.clicked.connect(self.func_req_chart)
        self.btn_clear.clicked.connect(self.func_clear)
        

    def print(self, data):
        """텍스트박스에 출력"""
        text = json.dumps(data, indent=4, ensure_ascii=False)
        self.text_result.setPlainText(text)

    def func_clear(self):
        """텍스트박스 내용 지우기"""
        self.text_result.setPlainText("")
        
    @asyncSlot()
    async def func_login(self):
        """로그인"""
        api = self.api
        if not await api.login(appkey, appsecretkey): return self.print(f"로그인 실패: {api.last_message}")
        self.print("로그인 성공: 접속서버: " + ("모의투자" if api.is_simulation else "실투자"))
        
    @asyncSlot()
    async def func_req_itemInfo(self):
        """종목정보조회"""
        api = self.api
        request = {
            "t1102InBlock": {
                "shcode": self.text_itemcode.toPlainText(), # 종목코드
            }
        }
        response = await api.request("t1102", request)
        if not response: return self.print(f"요청실패: {api.last_message}")
        self.print(response.body)
        
    @asyncSlot()
    async def func_req_chart(self):
        """차트조회"""
        api = self.api
        request = {
            "t8410InBlock": {
                "shcode": self.text_itemcode.toPlainText(), # 종목코드
                "gubun": "2", # 주기구분(2:일3:주4:월5:년)
                "qrycnt": 100, # 요청건수(최대-압축:2000비압축:500)
                "sdate": "", # 시작일자
                "edate": "99999999", # 종료일자
                "cts_date": "", # 연속일자
                "comp_yn": "N", # 압축여부(Y:압축N:비압축)
                "sujung": "Y", # 수정주가여부(Y:적용N:비적용)
            }
        }
        response = await api.request("t8410", request)
        if not response: return self.print(f"요청실패: {api.last_message}")
        self.print(response.body)


def main():
    """메인함수"""
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(loop)
    window.show()
    
    with loop:
        loop.run_forever()



if __name__ == '__main__':
    main()

