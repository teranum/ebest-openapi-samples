import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

import pandas as pd
import ta

'''
pandas와 ta 패키지를 이용한 보조지표 계산
'''

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    
    # 삼성전자 일봉 데이터 500개 조회
    request = {
        't8410InBlock': {
            'shcode': '005930', # 삼성전자
            'gubun': '2', # 주기구분(2:일3:주4:월5:년)
            'qrycnt': 500, # 요청건수(최대-압축:2000비압축:500)
            'sdate': '', # 시작일자
            'edate': '99999999', # 종료일자
            'cts_date': '', # 연속일자
            'comp_yn': 'N', # 압축여부(Y:압축N:비압축)
            'sujung': 'Y', # 수정주가여부(Y:적용N:비적용)
        }
    }
    response = await api.request('t8410', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    # 시간, 시가, 고가, 저가, 종가, 거래량 데이터로 변환
    data = response.body.get('t8410OutBlock1', None)
    if data is None: return print('데이터 없음')
    
    df = pd.DataFrame([list((x['date'], x['open'], x['high'], x['low'], x['close'], x['jdiff_vol'])) for x in data]
                      , columns = ['time', 'open', 'high', 'low', 'close', 'volume'])

    out_df = pd.DataFrame()
    
    # 5일 이동평균선, 20일 이동평균선, 60일 이동평균선
    out_df['일자'] = df['time']
    out_df['종가'] = df['close']
    out_df['ma5'] = df['close'].rolling(window=5).mean()
    out_df['ma20'] = df['close'].rolling(window=20).mean()
    out_df['ma60'] = df['close'].rolling(window=60).mean()

    # MACD
    out_df['macd'] = ta.trend.MACD(df['close'], window_fast=12, window_slow=26, window_sign=9).macd() 
    
    # RSI
    out_df['rsi(14)'] = ta.momentum.rsi(df['close'], window=14)
    
    # 출력
    print_table(out_df)
    
    await api.close()

asyncio.run(main())

# Output:
'''
Row Count = 500
+----------+-------+---------+---------+--------------------+----------------------+--------------------+
|   일자   |  종가 |   ma5   |   ma20  |        ma60        |         macd         |       rsi(14)      |
+----------+-------+---------+---------+--------------------+----------------------+--------------------+
| 20220221 | 74200 |   nan   |   nan   |        nan         |         nan          |        nan         |
| 20220222 | 73400 |   nan   |   nan   |        nan         |         nan          |        nan         |
| 20220223 | 73000 |   nan   |   nan   |        nan         |         nan          |        nan         |
| 20220224 | 71500 |   nan   |   nan   |        nan         |         nan          |        nan         |
| 20220225 | 71900 | 72800.0 |   nan   |        nan         |         nan          |        nan         |
| 20220228 | 72100 | 72380.0 |   nan   |        nan         |         nan          |        nan         |
...
| 20240221 | 73000 | 73180.0 | 73990.0 | 73928.33333333333  | -212.27673665466136  | 45.58786874648432  |
| 20240222 | 73100 | 73200.0 | 73885.0 |      73940.0       |  -243.3352193822211  | 46.115602717513674 |
| 20240223 | 72900 | 73220.0 | 73830.0 |      73960.0       |  -280.8501534920506  | 45.171969927494274 |
| 20240226 | 72800 | 73020.0 | 73765.0 |      73985.0       | -315.01883231323154  | 44.67968120385597  |
| 20240227 | 72900 | 72940.0 | 73740.0 | 73988.33333333333  | -330.22199854278006  | 45.321411928014726 |
| 20240228 | 73200 | 72980.0 | 73680.0 | 73996.66666666667  |  -314.4384735255444  | 47.29661874274963  |
| 20240229 | 73400 | 73040.0 | 73635.0 | 74006.66666666667  | -282.53470351461146  | 48.628934851012275 |
+----------+-------+---------+---------+--------------------+----------------------+--------------------+
'''
