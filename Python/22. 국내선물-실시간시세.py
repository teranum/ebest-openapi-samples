import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api:ebest.OpenApi):
    # 지수선물마스터조회API용 요청
    request = {
        't9943InBlock': {
            'gubun': '0', # 0:전체, 1:코스피, 2:코스닥
        }
    }
    response = await api.request('t9943', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    # 대표 월물 가져온다
    item = response.body['t9943OutBlock'][0] # {'hname':'F 2406','shcode':'101V6000','expcode':'KR4101V60002'}
    print(f'대표월물: {item}')
    shcode = item['shcode']

    # FC0 : KOSPI200선물체결(C0)
    await api.add_realtime('FC0', shcode)
    
    # 10분후 실시간 시세 중지
    print('10분동안 실시간 작동중...');
    await asyncio.sleep(600)
    await api.remove_realtime('FC0', shcode)
    print('실시간중지');
    

def on_message(api:ebest.OpenApi, msg:str): print(f'on_message: {msg}')

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == 'FC0':
        print(f'선물 체결시세: {trcode}, {key}, {realtimedata}')

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
