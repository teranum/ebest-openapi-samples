import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')

    symbol = 'HSIH24' # 항셍선물 2024년 3월물, 또는 다른 선물 종목코드로 변경하세요.
    
    sym8 = f'{symbol:8}' # 8자리로 맞추기

    # [실시간 시세 요청] OVC : 해외선물 현재가체결
    await api.add_realtime('OVC', sym8)
    
    # 10분후 실시간 시세 중지
    print('10분동안 실시간 작동중...');
    await asyncio.sleep(600)
    await api.remove_realtime('OVC', sym8)
    await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()
    

def on_message(api:ebest.OpenApi, msg:str): print(f'on_message: {msg}')

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == 'OVC':
        print(f'on_realtime: 해외선물 체결시세: {trcode}, {key}')
        print_table(realtimedata)
        
asyncio.run(main())

# Output:
'''
10분동안 실시간 작동중...
on_message: OVC(3): 정상처리되었습니다
on_realtime: 해외선물 체결시세: OVC, HSIH24
Field Count = 19
+-----------+----------+
|    key    |  value   |
+-----------+----------+
|  ovsmkend | 20240307 |
|   symbol  |  HSIH24  |
|    lSeq   |    2     |
|  chgrate  |  -0.72   |
|  kordate  | 20240307 |
|   trdtm   |  134718  |
|   curpr   | 16318.0  |
|  ovsdate  | 20240307 |
|  mdvolume |          |
|  ydiffpr  |  118.0   |
|    totq   |  82909   |
|    high   | 16552.0  |
| ydiffSign |    5     |
|    low    | 16296.0  |
|  msvolume |          |
|   cgubun  |    -     |
|    trdq   |    1     |
|    open   | 16438.0  |
|   kortm   |  144718  |
+-----------+----------+
on_realtime: 해외선물 체결시세: OVC, HSIH24
Field Count = 19
+-----------+----------+
|    key    |  value   |
+-----------+----------+
|  ovsmkend | 20240307 |
|   symbol  |  HSIH24  |
|    lSeq   |    3     |
|  chgrate  |  -0.72   |
|  kordate  | 20240307 |
|   trdtm   |  134718  |
|   curpr   | 16318.0  |
|  ovsdate  | 20240307 |
|  mdvolume |          |
|  ydiffpr  |  118.0   |
|    totq   |  82910   |
|    high   | 16552.0  |
| ydiffSign |    5     |
|    low    | 16296.0  |
|  msvolume |          |
|   cgubun  |    -     |
|    trdq   |    1     |
|    open   | 16438.0  |
|   kortm   |  144718  |
+-----------+----------+
...
'''
