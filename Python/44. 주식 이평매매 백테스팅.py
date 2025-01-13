import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

import pandas as pd

'''
가장 표준 지표인 이동평균선을 이용한 매매 전략 백테스팅 샘플

1. 종목 및 데이터
    시총 상위 종목 또는 대장주, 일봉 데이터
    
2. 진입조건
    - 60일선과 120일선 정배열에서, 5일선이 60일선을 돌파할 때 진입
    
3. 익절조건
    - 분할익절, 수익15퍼에서 보유수량의 절반 익절, 다음 15퍼 상승마다 남은수량 절반씩 익절
    
4. 손절 및 청산 조건
    - 5일선과 20일선 모두 60일선 아래로 떨어질 때 전량청산
'''

async def sample(api):
    while True:
        shcode = await ainput(f'종목코드 6자리를 입력하세요(ex 005930):')
        if len(shcode) == 0: break
        if len(shcode) != 6: continue # 종목코드 6자리 체크
        count = 0
        count_str = await ainput(f'조회할 데이터 건수를 입력하세요(ex 1500):')
        if len(count_str) != 0 and not count_str.isdigit(): continue
        if len(count_str) != 0: count = int(count_str)
        if count == 0: count = 1500 # 기본값
        if count < 500: count = 500

        # 일봉 데이터 조회
        df = await GetStockChartData(api, shcode, count)

        length = len(df)
        if length < 120:
            print(f'데이터 부족: {length}건')
            continue
    
        # 5일 이동평균선, 20일 이동평균선, 60일, 120일 이동평균선
        calc_df = pd.DataFrame()
        calc_df['일자'] = df['time']
        calc_df['종가'] = df['close']
        calc_df['고가'] = df['high']
        calc_df['ma5'] = df['close'].rolling(window=5).mean()
        calc_df['ma20'] = df['close'].rolling(window=20).mean()
        calc_df['ma60'] = df['close'].rolling(window=60).mean()
        calc_df['ma120'] = df['close'].rolling(window=120).mean()


        result_df = pd.DataFrame([], columns = ['진입명', '일자', '진입가', '보유수량', '청산가', '청산수량', '계좌평가금액', '계좌수익율(%)'])

        초기투자금 = 10000000 # 1000만원
        예수금 = 초기투자금
        보유수량 = 0
        진입가격 = 0
        익절횟수 = 0
        진입횟수 = 0

        for i in range(120, length, 1):
            ma5 = calc_df['ma5'][i]
            ma20 = calc_df['ma20'][i]
            ma60 = calc_df['ma60'][i]
            ma120 = calc_df['ma120'][i]
            ma5_1 = calc_df['ma5'][i-1] # 전날 5일 이동평균선
            ma60_1 = calc_df['ma60'][i-1] # 전날 60일 이동평균선
            고가 = calc_df['고가'][i]
            종가 = calc_df['종가'][i]
            일자 = calc_df['일자'][i]
            
            if 보유수량 == 0:
                # 진입 조건 체크
                if ma60 > ma120 and ma5_1 < ma60_1 and ma5 > ma60: # 60일선과 120일선이 정배열, 5일선이 60일선을 돌파할 때
                    # 신규 진입
                    익절횟수 = 0
                    진입횟수 += 1
                    진입가격 = 종가
                    보유수량 = int(예수금 / 진입가격)
                    현재계좌평가금액 = 예수금
                    예수금 -= 진입가격 * 보유수량
                    result_df.loc[-1] = ['신규진입', 일자, 진입가격, 보유수량, 0, 0
                                         , 현재계좌평가금액, round((현재계좌평가금액-초기투자금) / 초기투자금 * 100.00, 2)]
                    result_df.index += 1
            else:
                # 청산 조건 체크
                if ma5 < ma60 and ma20 < ma60: # 5일선과 20일선 모두 60일선 아래로 떨어질 때
                    # 전량 청산
                    청산가 = 종가
                    예수금 += 청산가 * 보유수량
                    result_df.loc[-1] = ['청산', 일자, 진입가격, 0, 청산가, 보유수량, 예수금, round((예수금-초기투자금) / 초기투자금 * 100.00, 2)]
                    result_df.index += 1
                    보유수량 = 0
                else:
                    # 익절 체크
                    당일최대수익률 = (고가 - 진입가격) / 진입가격 * 100
                    while True:
                        # 15퍼센트 단위로 절반씩 익절
                        당일익절기준 = 15 * (익절횟수 + 1)
                        if 당일최대수익률 > 당일익절기준: # 수익 15퍼 마다 보유수량의 절반 익절
                            익절횟수 += 1
                            익절청산가 = int(진입가격 * (100 + 당일익절기준) / 100)
                            익절수량 = int(보유수량 / 2)
                            if 익절수량 == 0:
                                익절수량 = 보유수량
                            예수금 += 익절청산가 * 익절수량
                            보유수량 -= 익절수량
                            현재계좌평가금액 = 종가 * 보유수량 + 예수금
                            result_df.loc[-1] = [f'익절{익절횟수}', 일자, 진입가격, 보유수량
                                                 , 익절청산가, 익절수량, 현재계좌평가금액, round((현재계좌평가금액-초기투자금) / 초기투자금 * 100.00, 2)]
                            result_df.index += 1
                            if 보유수량 == 0:
                                break
                        else:
                            break
                        pass
            
            pass
    
        최종평가금 = 예수금 + calc_df['종가'][length-1] * 보유수량
        if 보유수량 == 0: 진입가격 = 0

        # 출력
        최종수익율 = (최종평가금-초기투자금) / 초기투자금 * 100.00
        연평균수익율 = 최종수익율 / ((count - 120) / 240.0) # 240일 영업일 기준 1년으로 계산, 120일은 이동평균선 계산을 위한 기간
        result_df.loc[-1] = ['최종평가', calc_df['일자'][length-1], 진입가격, 보유수량, 0, 0
                             , 최종평가금, round(최종수익율, 2)]
        result_df.index += 1
        print_table(result_df)
        print(f'진입횟수: {진입횟수}회, 최종수익율: {round(최종수익율, 2)}%, 연평균수익율: {round(연평균수익율, 2)}%')
        print('')

async def GetStockChartData(api, code, count, gubun='2'):
    '''
    주식 차트 데이터 조회 함수
    api: ebest api 객체
    code: 주식 종목코드
    count: 조회할 데이터 건수
    gubun: 주기구분(2:일3:주4:월5:년), 기본값: 일
    return: DataFrame
    '''
    received_count = 0
    cts_date = ''
    tr_cont = 'N'
    tr_cont_key = '0'
    all_data = []
    req_fram_count = 0
    while received_count < count:
        # 일봉 데이터 조회
        req_fram_count += 1
        print (f'[{code}] 차트요청중...{req_fram_count}')
        req_count = min(500, count - received_count)
        request = {
            't8410InBlock': {
                'shcode': code, # 종목코드
                'gubun': gubun, # 주기구분(2:일3:주4:월5:년)
                'qrycnt': req_count, # 요청건수
                'sdate': '', # 시작일자
                'edate': '99999999', # 종료일자
                'cts_date': cts_date, # 연속일자
                'comp_yn': 'N', # 압축여부(Y:압축N:비압축)
                'sujung': 'Y', # 수정주가여부(Y:적용N:비적용)
            }
        }
        response = await api.request('t8410', request, tr_cont = tr_cont, tr_cont_key = tr_cont_key)
        if not response:
            print(f'요청실패: {api.last_message}')
            break
        
        # 시간, 시가, 고가, 저가, 종가, 거래량 데이터로 변환
        data = response.body.get('t8410OutBlock1', None)
        if data is None: break
        
        all_data = data + all_data
        received_count = len(all_data)
        if received_count >= count:
            break
        cts_date = response.body['t8410OutBlock']['cts_date']
        tr_cont = response.tr_cont
        tr_cont_key = response.tr_cont_key
        if tr_cont == 'N': break
        await asyncio.sleep(1)
        pass
    
    return pd.DataFrame([list((x['date'], x['open'], x['high'], x['low'], x['close'], x['jdiff_vol'])) for x in all_data]
                        , columns = ['time', 'open', 'high', 'low', 'close', 'volume'])

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')
    await sample(api)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())

# Output:
'''
종목코드 6자리를 입력하세요(ex 005930):005930
조회할 데이터 건수를 입력하세요(ex 1500):1500
[005930] 차트요청중...1
[005930] 차트요청중...2
[005930] 차트요청중...3
Row Count = 26
+----------+----------+--------+----------+--------+----------+--------------+---------------+
|  진입명  |   일자   | 진입가 | 보유수량 | 청산가 | 청산수량 | 계좌평가금액 | 계좌수익율(%) |
+----------+----------+--------+----------+--------+----------+--------------+---------------+
| 신규진입 | 20190507 | 44850  |   222    |   0    |    0     |   10000000   |      0.0      |
|   청산   | 20190510 | 44850  |    0     | 42900  |   222    |   9567100    |     -4.33     |
| 신규진입 | 20190620 | 45500  |   210    |   0    |    0     |   9567100    |     -4.33     |
|   청산   | 20190819 | 45500  |    0     | 43600  |   210    |   9168100    |     -8.32     |
| 신규진입 | 20190909 | 46900  |   195    |   0    |    0     |   9168100    |     -8.32     |
|  익절1   | 20191213 | 46900  |    98    | 53935  |    97    |   10614895   |      6.15     |
|  익절2   | 20200114 | 46900  |    49    | 60970  |    49    |   11181825   |     11.82     |
|   청산   | 20200311 | 46900  |    0     | 52100  |    49    |   10794725   |      7.95     |
| 신규진입 | 20200907 | 56500  |   191    |   0    |    0     |   10794725   |      7.95     |
|  익절1   | 20201116 | 56500  |    96    | 64975  |    95    |   12540650   |     25.41     |
|  익절2   | 20201207 | 56500  |    48    | 73450  |    48    |   13200650   |     32.01     |
|  익절3   | 20210104 | 56500  |    24    | 81925  |    24    |   13659650   |      36.6     |
|  익절4   | 20210111 | 56500  |    12    | 90400  |    12    |   13844450   |     38.44     |
|   청산   | 20210316 | 56500  |    0     | 82800  |    12    |   13746050   |     37.46     |
| 신규진입 | 20210406 | 86000  |   159    |   0    |    0     |   13746050   |     37.46     |
|   청산   | 20210511 | 86000  |    0     | 81200  |   159    |   12982850   |     29.83     |
| 신규진입 | 20230111 | 60500  |   214    |   0    |    0     |   12982850   |     29.83     |
|   청산   | 20230320 | 60500  |    0     | 60200  |   214    |   12918650   |     29.19     |
| 신규진입 | 20230323 | 62300  |   207    |   0    |    0     |   12918650   |     29.19     |
|  익절1   | 20230530 | 62300  |   104    | 71645  |   103    |   14921185   |     49.21     |
|   청산   | 20230809 | 62300  |    0     | 68900  |   104    |   14567585   |     45.68     |
| 신규진입 | 20230907 | 70400  |   206    |   0    |    0     |   14567585   |     45.68     |
|   청산   | 20230922 | 70400  |    0     | 68800  |   206    |   14237985   |     42.38     |
| 신규진입 | 20240119 | 74700  |   190    |   0    |    0     |   14237985   |     42.38     |
|   청산   | 20240222 | 74700  |    0     | 73100  |   190    |   13933985   |     39.34     |
| 최종평가 | 20240304 |   0    |    0     |   0    |    0     |   13933985   |     39.34     |
+----------+----------+--------+----------+--------+----------+--------------+---------------+
진입횟수: 9회, 최종수익율: 39.34%, 연평균수익율: 6.84%
'''
