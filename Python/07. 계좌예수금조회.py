import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "CSPAQ22200InBlock1": {
            "BalCreTp": "0",
        }
    }
    response = await api.request("CSPAQ22200", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["CSPAQ22200OutBlock1"]
    table = PrettyTable(['key','value'])
    table.add_rows([list(x) for x in data.items()])
    print(table)
    
    data = response.body["CSPAQ22200OutBlock2"]
    table = PrettyTable(['key','value'])
    table.add_rows([list(x) for x in data.items()])
    print(table)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
