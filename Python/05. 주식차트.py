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
    
    print_table(response.body["t8410OutBlock1"])
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())

# Output:
"""
Row Count = 100
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
|   date   |  open |  high |  low  | close | jdiff_vol |  value  | jongchk | rate | pricechk | ratevalue | sign |
+----------+-------+-------+-------+-------+-----------+---------+---------+------+----------+-----------+------+
| 20231005 | 67300 | 67400 | 66700 | 66700 |  15904419 | 1064750 |    0    | 0.00 |    0     |     0     |  5   |
| 20231006 | 67100 | 67300 | 66000 | 66000 |  14238326 |  945986 |    0    | 0.00 |    0     |     0     |  5   |
| 20231010 | 66200 | 67600 | 66200 | 66400 |  19188108 | 1284566 |    0    | 0.00 |    0     |     0     |  2   |

...

| 20240226 | 72300 | 73200 | 72200 | 72800 |  14549894 | 1059031 |    0    | 0.00 |    0     |     0     |  5   |
| 20240227 | 73100 | 73400 | 72700 | 72900 |  13050455 |  952221 |    0    | 0.00 |    0     |     0     |  2   |
| 20240228 | 72900 | 73900 | 72800 | 73200 |  11684297 |  858249 |    0    | 0.00 |    0     |     0     |  2   |
| 20240229 | 72600 | 73400 | 72000 | 73400 |  20502140 | 1494456 |    0    | 0.00 |    0     |     0     |  2   |
"""
