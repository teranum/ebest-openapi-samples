import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t1102InBlock": {
            "shcode": "005930", # 삼성전자
        }
    }
    response = await api.request("t1102", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["t1102OutBlock"]
    table = PrettyTable(['key','value'])
    table.add_rows([list(x) for x in data.items()])
    print(table)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())

# Output:
"""
+--------------------+------------+
|        key         |   value    |
+--------------------+------------+
|       hname        |  삼성전자  |
|       price        |   73400    |
|        sign        |     2      |
|       change       |    200     |
|        diff        |    0.27    |
|       volume       |  20502140  |
|      recprice      |   73200    |
|        avg         |   72892    |

(중략 ...)
"""
