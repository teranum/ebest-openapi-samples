import asyncio
import ebest
import pandas as pd
from tabulate import tabulate
from app_keys import *

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    if api.is_simulation: return print("실시간검색은 실서버에서만 가능합니다")
     
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
    cond_df = pd.DataFrame(response.body['t1866OutBlock1'])
    print(tabulate(cond_df))
    
    # 요청할 조건검색식 선택
    cond_len = len(cond_df)
    sel_index = int(input(f'조건검색식index (0~{cond_len-1})를 입력하세요:'))
    if sel_index >= cond_len: return print("잘못된 index")
    
    # 조건검색식 조회
    query_index = cond_df['query_index'][sel_index]
    request = {
        "t1859InBlock": {
            "query_index": query_index,
        }
    }
    response = await api.request("t1859", request)
    if not response: return print(f"요청실패: {api.last_message}")
    item_list = response.body.get('t1859OutBlock1', None)
    if item_list:
        df = pd.DataFrame(item_list)
        print(tabulate(df))
    else:
        print(f"조건검색식[{query_index}] 결과 없음")
    
    # 실시간검색 등록
    request = {
        "t1860InBlock": {
            "sSysUserFlag": "U", # 'U' 고정
            "sFlag": "E", # 'E:'등록, 'D':중지
            "sAlertNum": "", # Flag 값 'D':중지 일떄만 입력 - 등록 요청 시 수신받은 t1860OutBlock.sAlertNum 값
            "query_index": query_index,
        }
    }
    response = await api.request("t1860", request)
    if not response: return print(f"요청실패: {api.last_message}")
    print(response.body)
    
    sAlertNum:str = response.body["t1860OutBlock"]["sAlertNum"]
    if sAlertNum == "":
        print("실시간검색 등록실패")
    else:
        print("실시간검색 등록성공")
        await api.add_realtime("AFR", sAlertNum)
        await asyncio.sleep(60) # 60초동안 유효, 후에 중지
        await api.remove_realtime("AFR", sAlertNum)
        await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()

def on_message(api:ebest.OpenApi, msg:str): print(f"on_message: {msg}")

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == "AFR":
        print(f"실시간조건검색: {trcode}, {key}, {realtimedata}")

asyncio.run(main())
