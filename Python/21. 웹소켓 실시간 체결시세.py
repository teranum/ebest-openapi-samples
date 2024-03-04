import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')

    # 삼성전자 주식 실시간 시세 요청
    await api.add_realtime('S3_', '005930')
    
    # 10분후 실시간 시세 중지
    print('10분동안 실시간 작동중...');
    await asyncio.sleep(600)
    await api.remove_realtime('S3_', '005930')
    await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()
    

def on_message(api:ebest.OpenApi, msg:str): print(f'on_message: {msg}')

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == 'S3_':
        print(f'체결시세: {trcode}, {key}, {realtimedata}')
        
asyncio.run(main())
