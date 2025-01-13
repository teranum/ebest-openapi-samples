import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api:ebest.OpenApi):
    # 삼성전자 주식 실시간 시세 요청
    ok = await api.add_realtime('S3_', '005930')
    if not ok:
        return print(f"실시간등록 실패: {api.last_message}")
    
    # 1분후 실시간 시세 중지
    print('1분동안 실시간 작동중...');
    await asyncio.sleep(60)
    await api.remove_realtime('S3_', '005930')
    print('실시간중지');
    

def on_message(api:ebest.OpenApi, msg:str): print(f'on_message: {msg}')

def on_realtime(api:ebest.OpenApi, trcode:str, key:str, realtimedata:dict):
    if trcode == 'S3_':
        print(f'체결시세: {trcode}, {key}, {realtimedata}')
    

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')

    # 이벤트 핸들러 등록
    api.on_message.connect(on_message)
    api.on_realtime.connect(on_realtime)

    await sample(api)

    # 이벤트 핸들러 해제
    api.on_message.disconnect(on_message)
    api.on_realtime.disconnect(on_realtime)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())
