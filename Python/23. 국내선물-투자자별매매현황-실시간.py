import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")

    # [요청] t1602 : 시간대별투자자매매추이
    request = {
        "t1602InBlock": {
            "market": "4",      # 시장구분: 0:전체, 1:코스피, 2:KP200, 3:코스닥, 4:선물, 5:콜옵션, 6:풋옵션, 7:ELW, 8:ETF
            "upcode": "900",    # 업종코드: 001:코스피, 101:KP200, 301:코스닥, 900:선물, 700:콜옵션, 800:풋옵션, 550:ELW, 560:ETF
            "gubun1": "2",      # 수량구분: 1:수량, 2:금액
            "gubun2": "0",      # 전일분구분: 0:금일, 1:전일
            "cts_time": "",     # 연속조회시간
            "cts_idx": 0,       # 사용안함
            "cnt": 10,          # 조회건수
            "gubun3": "",       # 직전대비구분(C:직전대비)
        },
    }
    response = await api.request("t1602", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    print_table(response.body["t1602OutBlock"])
    print_table(response.body["t1602OutBlock1"])
    
    # [실시간 시세 요청] BM_ : 업종별투자자별매매현황
    await api.add_realtime("BM_", "900")
    
    # 10분후 실시간 시세 중지
    print("10분동안 실시간 작동중...");
    await asyncio.sleep(600)
    await api.remove_realtime("BM_", 900)
    await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()
    

def on_message(api:ebest.OpenApi, msg:str): print(f"on_message: {msg}")

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == "FC0":
        print(f"선물 체결시세: {trcode}, {key}, {realtimedata}")
        
asyncio.run(main())

# Output:
"""
+----------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|   time   | sv_08 | sv_17 | sv_18 | sv_01 | sv_03 | sv_04 | sv_02 | sv_05 | sv_06 | sv_07 | sv_11 | sv_00 |
+----------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| 18103000 |  1360 | -5444 |  3703 |  6406 | -2902 |  -22  |   63  |   17  |  141  |  381  |   0   |   0   |
| 18100000 |  1360 | -5444 |  3703 |  6406 | -2902 |  -22  |   63  |   17  |  141  |  381  |   0   |   0   |
| 18093000 |  1360 | -5444 |  3703 |  6406 | -2902 |  -22  |   63  |   17  |  141  |  381  |   0   |   0   |
| 18090000 |  1360 | -5444 |  3703 |  6406 | -2902 |  -22  |   63  |   17  |  141  |  381  |   0   |   0   |

"""
