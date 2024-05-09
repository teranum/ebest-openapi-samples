import sys, asyncio, json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from qasync import QEventLoop, asyncSlot

import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

form_class = uic.loadUiType('36. MainWindow.ui')[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        '''생성자'''
        super().__init__()
        self.setupUi(self)
        self.api = ebest.OpenApi()
        self.api.on_message = lambda api, msg: self.print(msg)
        self.api.on_realtime = lambda api, trcode, key, realtimedata: self.print(f'{trcode}, {key}, {realtimedata}')
        
        self.btn_clear.clicked.connect(self.list_result.clear)
        self.btn_login.clicked.connect(self.func_login)
        
        self.btn_item_info.clicked.connect(self.func_item_info)
        self.btn_realtime_add.clicked.connect(self.func_realtime_add)
        self.btn_realtime_remove.clicked.connect(self.func_realtime_remove)
        

    def print(self, data):
        '''리스트에 출력'''
        text = json.dumps(data, ensure_ascii=False)
        self.list_result.addItem(text)

    @asyncSlot()
    async def func_login(self):
        '''로그인'''
        api = self.api
        if not await api.login(appkey, appsecretkey): return self.print(f'로그인 실패: {api.last_message}')
        self.print('로그인 성공: 접속서버: ' + ('모의투자' if api.is_simulation else '실투자'))

        # 로그인 성공시, 지수선물 마스터 종목 조회
        request = {
            't8432InBlock': {
                'gubun': '0',
            }
        }
        response = await api.request('t8432', request)
        if not response: return print(f'요청실패: {api.last_message}')
    
        # 조회결과 ComboBox에 추가
        items = response.body['t8432OutBlock']
        self.combo_items.clear()
        for item in items:
            self.combo_items.addItem(f'{item['shcode']}, {item['hname']}')
            
        # 버튼 활성화
        self.btn_login.setEnabled(False)
        self.btn_item_info.setEnabled(True)
        self.btn_realtime_add.setEnabled(True)
        self.btn_realtime_remove.setEnabled(True)
            

    @asyncSlot()
    async def func_item_info(self):
        '''선물/옵션현재가(시세)조회'''
        api = self.api
        symbol = self.combo_items.currentText().split(',')[0]
        request = {
            "t2101InBlock": {
                "focode": symbol,
            },
        }
        response = await self.api.request("t2101", request)
        if not response: return self.print(f"요청실패: {api.last_message}")
        info = response.body['t2101OutBlock']
        self.print(info)
        
    @asyncSlot()
    async def func_realtime_add(self):
        '''실시간시세요청'''
        symbol = self.combo_items.currentText().split(',')[0]
        await self.api.add_realtime('FC0', symbol)
        self.print(f'{symbol} 실시간시세 요청 시작')

    
    @asyncSlot()
    async def func_realtime_remove(self):
        '''실시간시세중지'''
        symbol = self.combo_items.currentText().split(',')[0]
        await self.api.remove_realtime('FC0', symbol)
        self.print(f'{symbol} 실시간시세 요청 중지')


def main():
    '''메인함수'''
    loop = QEventLoop(QApplication(sys.argv))
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    
    with loop:
        loop.run_forever()



if __name__ == '__main__':
    main()

