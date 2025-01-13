import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

import pandas as pd

'''
가장 표준 지표인 이동평균선을 이용한 매매 전략 백테스팅 샘플

1. 선물종목
    코스피200 연결지수선물 1계약 기준, 일봉 데이터
    
2. 진입조건
    - 롱만 진입
    - 60일선과 120일선 정배열에서, 5일선이 60일선을 돌파할 때 진입
    
3. 익절조건
    - 200만원(8pt) 이상 수익 발생시, 트레일링 스탑을 적용, 최대수익대비 50% 수익감소시 청산
    
4. 손절 및 청산 조건
    - 100만원(4pt) 이상 손실 발생시 청산
    - 5일선과 20일선 모두 60일선 아래로 떨어질 때 청산
'''

async def sample(api):
    while True:
        shcode = '90199999' # 기본값, 연결선물지수
        count_str = await ainput(f'조회할 데이터 건수를 입력하세요(ex 1500):')
        if len(count_str) == 0: break
        if not count_str.isdigit(): continue
        count = int(count_str)
        if count == 0: count = 1500 # 기본값
        if count < 500: count = 500

        # 일봉 데이터 조회
        df = await GetFutureStockChartData(api, shcode, count)

        length = len(df)
        if length < 120:
            print(f'데이터 부족: {length}건')
            continue
    
        # 5일 이동평균선, 20일 이동평균선, 60일, 120일 이동평균선
        calc_df = pd.DataFrame()
        calc_df['일자'] = df['time']
        calc_df['종가'] = df['close']
        calc_df['고가'] = df['high']
        calc_df['저가'] = df['low']
        calc_df['ma5'] = df['close'].rolling(window=5).mean()
        calc_df['ma20'] = df['close'].rolling(window=20).mean()
        calc_df['ma60'] = df['close'].rolling(window=60).mean()
        calc_df['ma120'] = df['close'].rolling(window=120).mean()


        result_df = pd.DataFrame([], columns = ['진입명', '일자', '진입가', '보유수량', '청산가', '청산수량', '청산손익(pt)', '누적손익(pt)'])

        누적손익 = 0
        보유수량 = 0
        진입가격 = 0
        진입횟수 = 0
        수익횟수 = 0
        수익누계 = 0
        손실누계 = 0
        진입당최대수익 = 0
        TS최대수익 = 0
        연속손실합계 = 0
        최대연속손실 = 0

        for i in range(120, length, 1):
            ma5 = calc_df['ma5'][i]
            ma20 = calc_df['ma20'][i]
            ma60 = calc_df['ma60'][i]
            ma120 = calc_df['ma120'][i]
            ma5_1 = calc_df['ma5'][i-1] # 전날 5일 이동평균선
            ma60_1 = calc_df['ma60'][i-1] # 전날 60일 이동평균선
            고가 = calc_df['고가'][i]
            저가 = calc_df['저가'][i]
            종가 = calc_df['종가'][i]
            일자 = calc_df['일자'][i]
            
            if 보유수량 == 0:
                # 진입 조건 체크
                if ma60 > ma120 and ma5_1 < ma60_1 and ma5 > ma60: # 60일선과 120일선이 정배열, 5일선이 60일선을 상향돌파할 때
                    # 신규 롱 진입
                    진입횟수 += 1
                    진입가격 = 종가
                    보유수량 = 1
                    진입당최대수익 = 0
                    TS최대수익 = 0
                    result_df.loc[-1] = ['롱 진입', 일자, 진입가격, 보유수량, 0, 0, 0, round(누적손익,2)]
                    result_df.index += 1
                    pass
            else:
                청산가 = 종가
                청산손익 = (청산가 - 진입가격) * 보유수량
                최대수익 = ((고가 if 보유수량 > 0 else 저가) - 진입가격) * 보유수량
                if 최대수익 > 진입당최대수익: 진입당최대수익 = 최대수익
                
                청산명 = None

                if 보유수량 > 0 and ma5 < ma60 and ma20 < ma60: # 롱 청산 조건 체크: 5일선과 20일선 모두 60일선 아래로 떨어질 때
                    청산명 = '이평청산'
                else:
                    if 청산손익 <= -4: # 손절
                        청산명 = '손절'
                    elif TS최대수익 == 0:
                        if 최대수익 >= 8: TS최대수익 = 최대수익
                    else:
                        if 최대수익 > TS최대수익: TS최대수익 = 최대수익
                        if 청산손익 <= TS최대수익 * 0.5: # 수익 절반 감소
                            청산명 = 'TS청산'

                if 청산명 is not None:
                    누적손익 += 청산손익
                    if 청산손익 > 0:
                        수익횟수 += 1
                        수익누계 += 청산손익
                        연속손실합계 = 0
                    else:
                        손실누계 += 청산손익
                        연속손실합계 += 청산손익
                        if 연속손실합계 < 최대연속손실: 최대연속손실 = 연속손실합계
                        
                    result_df.loc[-1] = [청산명, 일자, 진입가격, 0, 청산가, 보유수량, round(청산손익, 2), round(누적손익,2)]
                    result_df.index += 1
                    보유수량 = 0
            pass
    
        최종평가포인트 = 누적손익 + (calc_df['종가'][length-1] - 진입가격) * 보유수량
        if 보유수량 == 0: 진입가격 = 0

        # 출력
        result_df.loc[-1] = ['최종평가', calc_df['일자'][length-1], 진입가격, 보유수량, 0, 0, 0, round(최종평가포인트, 2)]
        result_df.index += 1
        print_table(result_df)
        
        연평균수익포인트 = 최종평가포인트 / ((count - 120) / 240.0) # 240일 영업일 기준 1년으로 계산, 120일은 이동평균선 계산을 위한 기간
        print(f'일자: {calc_df['일자'][120]}~{calc_df['일자'][length-1]}')
        print(f'총수익(pt): {round(수익누계, 2)}, 총손실(pt): {round(손실누계, 2)}, 최대연속손실(pt): {round(최대연속손실, 2)}')
        print(f'수익/진입 횟수: {수익횟수} / {진입횟수}, 승율: {round(수익횟수/진입횟수 * 100, 2)}%, 손익비: {round(수익누계 / (-손실누계), 2)}')
        print(f'최종평가손익(pt): {round(최종평가포인트, 2)}, 연평균손익(pt): {round(연평균수익포인트, 2)}')
        print(f'최종평가손익(원): {int(최종평가포인트 * 250000):,}, 연평균손익(원): {int(연평균수익포인트 * 250000):,}')
        print('')
        pass

async def GetFutureStockChartData(api, code, count, gubun='2'):
    '''
    선물 차트 데이터 조회 함수
    api: ebest api 객체
    code: 선물 종목코드
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
            't8416InBlock': {
                'shcode': code, # 종목코드
                'gubun': gubun, # 주기구분(2:일3:주4:월5:년)
                'qrycnt': req_count, # 요청건수
                'sdate': '', # 시작일자
                'edate': '99999999', # 종료일자
                'cts_date': cts_date, # 연속일자
                'comp_yn': 'N', # 압축여부(Y:압축N:비압축)
            }
        }
        response = await api.request('t8416', request, tr_cont = tr_cont, tr_cont_key = tr_cont_key)
        if not response:
            print(f'요청실패: {api.last_message}')
            break
        
        # 시간, 시가, 고가, 저가, 종가, 거래량 데이터로 변환
        data = response.body.get('t8416OutBlock1', None)
        if data is None: break
        
        all_data = data + all_data
        received_count = len(all_data)
        if received_count >= count:
            break
        cts_date = response.body['t8416OutBlock']['cts_date']
        tr_cont = response.tr_cont
        tr_cont_key = response.tr_cont_key
        if tr_cont == 'N': break
        await asyncio.sleep(1)
        pass
    
    return pd.DataFrame([list((x['date'], float(x['open']), float(x['high']), float(x['low']), float(x['close']), float(x['jdiff_vol']))) for x in all_data]
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
조회할 데이터 건수를 입력하세요(ex 1500):1500
[90199999] 차트요청중...1
[90199999] 차트요청중...2
[90199999] 차트요청중...3
Row Count = 23
+----------+----------+--------+----------+--------+----------+--------------+--------------+
|  진입명  |   일자   | 진입가 | 보유수량 | 청산가 | 청산수량 | 청산손익(pt) | 누적손익(pt) |
+----------+----------+--------+----------+--------+----------+--------------+--------------+
| 롱 진입  | 20190402 | 282.5  |    1     |  0.0   |    0     |     0.0      |     0.0      |
|  TS청산  | 20190418 | 282.5  |    0     | 286.5  |    1     |     4.0      |     4.0      |
| 롱 진입  | 20191212 | 285.0  |    1     |  0.0   |    0     |     0.0      |     4.0      |
|  TS청산  | 20200102 | 285.0  |    0     | 290.75 |    1     |     5.75     |     9.75     |
| 롱 진입  | 20200206 | 301.4  |    1     |  0.0   |    0     |     0.0      |     9.75     |
|   손절   | 20200210 | 301.4  |    0     | 296.45 |    1     |    -4.95     |     4.8      |
| 롱 진입  | 20200929 | 309.95 |    1     |  0.0   |    0     |     0.0      |     4.8      |
|  TS청산  | 20201015 | 309.95 |    0     | 313.3  |    1     |     3.35     |     8.15     |
| 롱 진입  | 20201106 | 321.85 |    1     |  0.0   |    0     |     0.0      |     8.15     |
| 이평청산 | 20210323 | 321.85 |    0     | 408.15 |    1     |     86.3     |    94.45     |
| 롱 진입  | 20210405 | 424.05 |    1     |  0.0   |    0     |     0.0      |    94.45     |
|  TS청산  | 20210421 | 424.05 |    0     | 425.65 |    1     |     1.6      |    96.05     |
| 롱 진입  | 20210521 | 421.6  |    1     |  0.0   |    0     |     0.0      |    96.05     |
|  TS청산  | 20210609 | 421.6  |    0     | 428.3  |    1     |     6.7      |    102.75    |
| 롱 진입  | 20210806 | 433.55 |    1     |  0.0   |    0     |     0.0      |    102.75    |
|   손절   | 20210810 | 433.55 |    0     | 429.0  |    1     |    -4.55     |     98.2     |
| 롱 진입  | 20230328 | 317.45 |    1     |  0.0   |    0     |     0.0      |     98.2     |
|  TS청산  | 20230406 | 317.45 |    0     | 319.75 |    1     |     2.3      |    100.5     |
| 롱 진입  | 20230918 | 342.95 |    1     |  0.0   |    0     |     0.0      |    100.5     |
|   손절   | 20230921 | 342.95 |    0     | 334.2  |    1     |    -8.75     |    91.75     |
| 롱 진입  | 20240202 | 354.05 |    1     |  0.0   |    0     |     0.0      |    91.75     |
|   손절   | 20240205 | 354.05 |    0     | 349.25 |    1     |     -4.8     |    86.95     |
| 최종평가 | 20240315 |  0.0   |    0     |  0.0   |    0     |     0.0      |    86.95     |
+----------+----------+--------+----------+--------+----------+--------------+--------------+
일자: 20180808~20240315
총수익(pt): 110.0, 총손실(pt): -23.05, 최대연속손실(pt): -13.55
수익/진입 횟수: 7 / 11, 승율: 63.64%, 손익비: 4.77
최종평가손익(pt): 86.95, 연평균손익(pt): 15.12
최종평가손익(원): 21,737,499, 연평균손익(원): 3,780,434
'''
