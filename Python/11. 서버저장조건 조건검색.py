import asyncio
import ebest
from app_keys import *
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    # 조건검색식 리스트 조회
    request = {
        "t1866InBlock": {
            "user_id": user_id, # 사용자ID 8자리
            "gb": "0", # 0 : 그룹+조건리스트 조회, 1 : 그룹리스트조회, 2 : 그룹명에 속한 조건리스트조회
            "group_name": "",
            "cont": "0",
            "cont_key": "",
        }
    }
    response = await api.request("t1866", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["t1866OutBlock1"]
    table = PrettyTable()
    table.field_names = data[0]
    table.add_rows([x.values() for x in data])
    print(table)
    
    # 요청할 조건검색식 선택
    cond_len = len(data)
    sel_index = int(input(f'조건검색식index (0~{cond_len-1})를 입력하세요:'))
    if sel_index >= cond_len: return print("잘못된 index")
    
    # 조건검색식 조회
    query_index = data[sel_index]['query_index']
    request = {
        "t1859InBlock": {
            "query_index": query_index,
        }
    }
    response = await api.request("t1859", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    item_list = response.body.get('t1859OutBlock1', None)
    if item_list:
        table = PrettyTable()
        table.field_names = item_list[0]
        table.add_rows([x.values() for x in item_list])
        print(table)
    else:
        print(f"조건검색식[{query_index}] 결과 없음")
    
    ... # 다른 작업 수행
    await api.close()


asyncio.run(main())
