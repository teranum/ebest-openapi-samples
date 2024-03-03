import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t8410InBlock": {
            "shcode": "005930", # 삼성전자
            "gubun": "2", # 주기구분(2:일3:주4:월5:년)
            "qrycnt": 100, # 요청건수(최대-압축:2000비압축:500)
            "sdate": "", # 시작일자
            "edate": "99999999", # 종료일자
            "cts_date": "", # 연속일자
            "comp_yn": "N", # 압축여부(Y:압축N:비압축)
            "sujung": "Y", # 수정주가여부(Y:적용N:비적용)
        }
    }
    response = await api.request("t8410", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["t8410OutBlock1"]
    
    # 연속조회
    if response.tr_cont == "Y":
        await asyncio.sleep(1) # 1초 대기
        request["t8410InBlock"]["cts_date"] = response.body["t8410OutBlock"]["cts_date"]
        response = await api.request("t8410", request, tr_cont=response.tr_cont, tr_cont_key=response.tr_cont_key)
        if not response:
            print(f"연속 요청실패: {api.last_message}")
        else:
            data = response.body["t8410OutBlock1"] + data # 연속조회 데이터와 첫번째 조회 데이터를 합침
    
    print_table(data)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())

# Output:
"""
Row Count = 200
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
|   date   |  open |  high |  low  | close | jdiff_vol |  value  | jongchk | rate | pricechk | ratevalue | sign |
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
| 20230509 | 65800 | 65800 | 65100 | 65300 |  9293835  |  607727 |    0    | 0.00 |    0     |     0     |  5   |
| 20230510 | 65500 | 65500 | 64300 | 64600 |  13042129 |  844224 |    0    | 0.00 |    0     |     0     |  5   |
| 20230511 | 64700 | 65100 | 64200 | 64200 |  11648905 |  752009 |    0    | 0.00 |    0     |     0     |  5   |
| 20230512 | 63700 | 64600 | 63600 | 64100 |  7546680  |  484312 |    0    | 0.00 |    0     |     0     |  5   |
| 20230515 | 64100 | 64600 | 63900 | 64500 |  8157143  |  524320 |    0    | 0.00 |    0     |     0     |  2   |
| 20230516 | 65800 | 65900 | 65300 | 65400 |  12200178 |  799675 |    0    | 0.00 |    0     |     0     |  2   |
| 20230517 | 65900 | 65900 | 64800 | 65000 |  10217085 |  666669 |    0    | 0.00 |    0     |     0     |  5   |

...

| 20240223 | 73600 | 74200 | 72900 | 72900 |  16060746 | 1177781 |    0    | 0.00 |    0     |     0     |  5   |
| 20240226 | 72300 | 73200 | 72200 | 72800 |  14549894 | 1059031 |    0    | 0.00 |    0     |     0     |  5   |
| 20240227 | 73100 | 73400 | 72700 | 72900 |  13050455 |  952221 |    0    | 0.00 |    0     |     0     |  2   |
| 20240228 | 72900 | 73900 | 72800 | 73200 |  11684297 |  858249 |    0    | 0.00 |    0     |     0     |  2   |
| 20240229 | 72600 | 73400 | 72000 | 73400 |  20502140 | 1494456 |    0    | 0.00 |    0     |     0     |  2   |
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
"""