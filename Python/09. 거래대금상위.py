import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    request = {
        't1463InBlock': {
            'gubun': '0', # 0:전체, 1:코스피, 2:코스닥
            'jnilgubun': '0', # 0 : 당일 1 : 전일
            'jc_num': 0, # 대상제외
            'sprice': 10000, # 현재가 >= sprice
            'eprice': 1000000, # 현재가 <= eprice
            'volume': 1000000, # 거래량 >= volume
            'idx': 0, # 처음 조회시는 0 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
            'jc_num2': 0, # 대상제외2
        }
    }
    response = await api.request('t1463', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    print_table(response.body['t1463OutBlock'])
    print_table(response.body['t1463OutBlock1'])
    

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
Field Count = 1
+-----+-------+
| key | value |
+-----+-------+
| idx |   20  |
+-----+-------+
Row Count = 20
+--------------------+--------+------+--------+-------+----------+---------+-----------+----------+--------+--------+------------+
|       hname        | price  | sign | change |  diff |  volume  |  value  | jnilvalue | bef_diff | shcode | filler | jnilvolume |
+--------------------+--------+------+--------+-------+----------+---------+-----------+----------+--------+--------+------------+
|      삼성전자      | 73400  |  2   |  200   |  0.27 | 20502140 | 1494456 |   866533  |  172.46  | 005930 |        |  11795859  |
|        기아        | 124500 |  2   |  6800  |  5.78 | 5862121  |  721607 |   211155  |  341.74  | 000270 |        |  1833765   |
|       현대차       | 250500 |  2   |  2500  |  1.01 | 2038396  |  507778 |   464303  |  109.36  | 005380 |        |  1911431   |
|     SK하이닉스     | 156200 |  5   |  1800  | -1.14 | 3233605  |  506194 |   576353  |  87.83   | 000660 |        |  3666960   |
|      알테오젠      | 160600 |  5   |  3900  | -2.37 | 2367010  |  398407 |   339506  |  117.35  | 196170 |        |  2161844   |
|       NAVER        | 195000 |  5   |  9000  | -4.41 | 2016957  |  397064 |   120373  |  329.86  | 035420 |        |   597421   |
...
'''
