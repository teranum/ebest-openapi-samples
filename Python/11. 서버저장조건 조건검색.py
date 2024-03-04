import asyncio
import ebest
from common import *
from app_keys import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    
    # 조건검색식 리스트 조회
    request = {
        't1866InBlock': {
            'user_id': user_id, # 사용자ID 8자리
            'gb': '0', # 0 : 그룹+조건리스트 조회, 1 : 그룹리스트조회, 2 : 그룹명에 속한 조건리스트조회
            'group_name': '',
            'cont': '0',
            'cont_key': '',
        }
    }
    response = await api.request('t1866', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    cond_list = response.body['t1866OutBlock1']
    print_table(cond_list)
    
    # 요청할 조건검색식 선택
    cond_len = len(cond_list)
    sel_index = int(input(f'조건검색식index (0~{cond_len-1})를 입력하세요:'))
    if sel_index >= cond_len: return print('잘못된 index')
    
    # 조건검색식 조회
    query_index = cond_list[sel_index]['query_index']
    request = {
        't1859InBlock': {
            'query_index': query_index,
        }
    }
    response = await api.request('t1859', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    item_list = response.body.get('t1859OutBlock1', None)
    if item_list:
        print_table(item_list)
    else:
        print(f'조건검색식[{query_index}] 결과 없음')
    
    ... # 다른 작업 수행
    await api.close()


asyncio.run(main())

# Output:
'''
Row Count = 1
+--------------+------------+------------+
| query_index  | group_name | query_name |
+--------------+------------+------------+
| XXXXXXXX0001 |  조건전략  |  고가돌파  |
+--------------+------------+------------+
조건검색식index (0~0)를 입력하세요:0
Row Count = 20
+--------+-----------------------------------+-------+------+--------+-------+--------+
| shcode |               hname               | price | sign | change |  diff | volume |
+--------+-----------------------------------+-------+------+--------+-------+--------+
| 005670 |               푸드웰              |  4770 |  2   |   40   |  0.85 |  5964  |
| 009580 |              무림P&P              |  3105 |  5   |   15   | -0.48 | 44058  |
| 009680 |               모토닉              |  8260 |  5   |   10   | -0.12 | 18460  |
| 028100 |              동아지질             | 13750 |  5   |  100   | -0.72 | 21003  |
| 032560 |             황금에스티            |  7050 |  5   |   50   | -0.70 | 40532  |
| 032750 |                삼진               |  5400 |  5   |   10   | -0.18 | 18638  |
...
'''