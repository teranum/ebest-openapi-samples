import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

import pandas as pd

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    
    while True:
        shcode = input(f'해외선물 종목코드를 입력하세요:')
        ncnt = int(input(f'N분주기를 입력하세요(1, 3, 5, 10, 15, 30, 45, 60, ...):'))
        readcnt = int(input(f'요청건수를 입력하세요(100, 500, 1000, ...):'))

        # 해외선물 분 차트 데이터 조회용 함수 호출
        df = await GetFutureStockChartData(api, shcode, ncnt, readcnt)
        print_table(df)
        pass # 무한 반복으로 다른 종목 데이터 불러온다
    
    await api.close()



async def GetFutureStockChartData(api, shcode, ncnt, readcnt):
    '''
    해외선물 분 차트 데이터 조회 함수
    api: ebest api 객체
    shcode: 선물 종목코드
    ncnt: N분주기 (1, 3, 5, 10, 15, 30, 45, 60, ...)
    readcnt: 조회할 데이터 건수
    return: DataFrame
    '''
    received_count = 0
    cts_date = ''
    cts_time = ''
    tr_cont = 'N'
    tr_cont_key = '0'
    all_data = []
    req_fram_count = 0
    while received_count < readcnt:
        # 일봉 데이터 조회
        req_fram_count += 1
        print (f'[{shcode}] 차트요청중...{req_fram_count}')
        req_count = min(500, readcnt - received_count)
        request = {
            "o3123InBlock": {
                "mktgb": "F", # 시장구분: F:선물, O:옵션
                "shcode": shcode, # 종목코드
                "ncnt": ncnt, # N분주기 (1, 3, 5, 10, 15, 30, 45, 60, ...)
                "readcnt": req_count, # 요청건수
                "cts_date": cts_date,
                "cts_time": cts_time,
            },
        }
        response = await api.request('o3123', request, tr_cont = tr_cont, tr_cont_key = tr_cont_key)
        if not response:
            print(f'요청실패: {api.last_message}')
            break
        
        # 날짜, 시간, 시가, 고가, 저가, 종가, 거래량 데이터로 변환
        data = response.body.get('o3123OutBlock1', None)
        if data is None: break
        
        all_data = data + all_data
        received_count = len(all_data)
        if received_count >= readcnt:
            break
        cts_date = response.body['o3123OutBlock']['cts_date']
        cts_time = response.body['o3123OutBlock']['cts_time']
        tr_cont = response.tr_cont
        tr_cont_key = response.tr_cont_key
        if tr_cont == 'N': break
        await asyncio.sleep(1)
        pass
    
    return pd.DataFrame([list((x['date'], x['time'], float(x['open']), float(x['high']), float(x['low']), float(x['close']), float(x['volume']))) for x in all_data]
                        , columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

asyncio.run(main())

# Output:
'''
해외선물 종목코드를 입력하세요:HSIH24
N분주기를 입력하세요(1, 3, 5, 10, 15, 30, 45, 60, ...):5
요청건수를 입력하세요(100, 500, 1000, ...):1000
[HSIH24] 차트요청중...1
[HSIH24] 차트요청중...2
Row Count = 1000
+----------+--------+---------+---------+---------+---------+--------+
|   date   |  time  |   open  |   high  |   low   |  close  | volume |
+----------+--------+---------+---------+---------+---------+--------+
| 20240304 | 203000 | 16523.0 | 16533.0 | 16523.0 | 16533.0 |  25.0  |
| 20240304 | 202500 | 16529.0 | 16529.0 | 16523.0 | 16523.0 |  26.0  |
| 20240304 | 202000 | 16530.0 | 16531.0 | 16528.0 | 16529.0 |  17.0  |
| 20240304 | 201500 | 16524.0 | 16530.0 | 16523.0 | 16530.0 |  28.0  |
| 20240304 | 201000 | 16535.0 | 16536.0 | 16526.0 | 16526.0 |  35.0  |
| 20240304 | 200500 | 16537.0 | 16542.0 | 16536.0 | 16539.0 |  25.0  |
| 20240304 | 200000 | 16532.0 | 16540.0 | 16532.0 | 16539.0 |  30.0  |
| 20240304 | 195500 | 16533.0 | 16536.0 | 16532.0 | 16533.0 |  17.0  |
...
| 20240304 | 211000 | 16520.0 | 16525.0 | 16518.0 | 16523.0 |  71.0  |
| 20240304 | 210500 | 16521.0 | 16524.0 | 16519.0 | 16520.0 |  92.0  |
| 20240304 | 210000 | 16525.0 | 16526.0 | 16521.0 | 16521.0 |  36.0  |
| 20240304 | 205500 | 16534.0 | 16534.0 | 16525.0 | 16526.0 |  83.0  |
| 20240304 | 205000 | 16533.0 | 16539.0 | 16531.0 | 16533.0 |  54.0  |
| 20240304 | 204500 | 16521.0 | 16532.0 | 16521.0 | 16532.0 |  61.0  |
| 20240304 | 204000 | 16529.0 | 16529.0 | 16521.0 | 16523.0 |  25.0  |
| 20240304 | 203500 | 16532.0 | 16534.0 | 16529.0 | 16530.0 |  31.0  |
+----------+--------+---------+---------+---------+---------+--------+
'''
