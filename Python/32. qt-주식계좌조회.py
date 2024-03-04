import sys, asyncio, json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from qasync import QEventLoop, asyncSlot

import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

form_class = uic.loadUiType('32. MainWindow.ui')[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self, loop=None):
        '''생성자'''
        super().__init__()
        self.setupUi(self)
        self.api = ebest.OpenApi()
        
        self.btn_login.clicked.connect(self.func_login)
        self.btn_clear.clicked.connect(self.func_clear)
        
        self.btn_jango.clicked.connect(self.func_jango)
        self.btn_miche.clicked.connect(self.func_miche)
        self.btn_yesu.clicked.connect(self.func_yesu)
        

    def print(self, data):
        '''텍스트박스에 출력'''
        text = json.dumps(data, indent=4, ensure_ascii=False)
        self.text_result.setPlainText(text)

    def func_clear(self):
        '''텍스트박스 내용 지우기'''
        self.text_result.setPlainText('')
        
    @asyncSlot()
    async def func_login(self):
        '''로그인'''
        api = self.api
        if not await api.login(appkey, appsecretkey): return self.print(f'로그인 실패: {api.last_message}')
        self.print('로그인 성공: 접속서버: ' + ('모의투자' if api.is_simulation else '실투자'))
        
    @asyncSlot()
    async def func_jango(self):
        '''현물계좌 잔고내역조회(API)'''
        api = self.api
        request = {
            'CSPAQ12300InBlock1': {
                'BalCreTp': '0',
                'CmsnAppTpCode': '0',
                'D2balBaseQryTp': '0',
                'UprcTpCode': '0',
            },
        }
        response = await api.request('CSPAQ12300', request)
        if not response: return self.print(f'요청실패: {api.last_message}')
        self.print(response.body)
        
    @asyncSlot()
    async def func_miche(self):
        '''현물계좌 주문체결내역 조회(API)'''
        api = self.api
        request = {
            'CSPAQ13700InBlock1': {
                'OrdMktCode': '00',
                'BnsTpCode': '0',
                'IsuNo': '',
                'ExecYn': '3',
                'OrdDt': '',
                'SrtOrdNo2': 0,
                'BkseqTpCode': '0',
                'OrdPtnCode': '00',
            },
        }
        response = await api.request('CSPAQ13700', request)
        if not response: return self.print(f'요청실패: {api.last_message}')
        self.print(response.body)
        
    @asyncSlot()
    async def func_yesu(self):
        '''현물계좌예수금 주문가능금액 총평가 조회'''
        api = self.api
        request = {
            'CSPAQ12200InBlock1': {
                'BalCreTp': '1',
            },
        }
        response = await api.request('CSPAQ12200', request)
        if not response: return self.print(f'요청실패: {api.last_message}')
        self.print(response.body)


def main():
    '''메인함수'''
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(loop)
    window.show()
    
    with loop:
        loop.run_forever()



if __name__ == '__main__':
    main()

