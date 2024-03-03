import asyncio
import ebest
from app_keys import appkey, appsecretkey, stock_dir # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    # [요청] t9945 : 주식마스터조회API용-종목명40bytes
    request = {
        "t9945InBlock": {
            "gubun": "1",
        },
    }
    response = await api.request("t9945", request)
    
    # 당일보관된 데이터가 없으면 종료
    
    
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["t8436OutBlock"]
    table = PrettyTable()
    table.field_names = data[0]
    table.add_rows([x.values() for x in data])
    print(table)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())


# Output:
"""
+----------------------+--------+--------------+----------+------------+------------+-----------+---------+----------+-------+-----------+------------+--------+
|        hname         | shcode |   expcode    | etfgubun | uplmtprice | dnlmtprice | jnilclose | memedan | recprice | gubun | bu12gubun | spac_gubun | filler |
+----------------------+--------+--------------+----------+------------+------------+-----------+---------+----------+-------+-----------+------------+--------+
|       동화약품       | 000020 | KR7000020008 |    0     |   12740    |    6860    |    9800   |  00001  |   9800   |   1   |     01    |     N      |        |
|       KR모터스       | 000040 | KR7000040006 |    0     |    604     |    326     |    465    |  00001  |   465    |   1   |     01    |     N      |        |
|         경방         | 000050 | KR7000050005 |    0     |   11510    |    6210    |    8860   |  00001  |   8860   |   1   |     01    |     N      |        |
|      삼양홀딩스      | 000070 | KR7000070003 |    0     |   93200    |   50200    |   71700   |  00001  |  71700   |   1   |     01    |     N      |        |
|     삼양홀딩스우     | 000075 | KR7000071001 |    0     |   70800    |   38200    |   54500   |  00001  |  54500   |   1   |     01    |     N      |        |
|      하이트진로      | 000080 | KR7000080002 |    0     |   26300    |   14200    |   20250   |  00001  |  20250   |   1   |     01    |     N      |        |
|    하이트진로2우B    | 000087 | KR7000082008 |    0     |   20400    |   10990    |   15700   |  00001  |  15700   |   1   |     01    |     N      |        |
|       유한양행       | 000100 | KR7000100008 |    0     |   89300    |   48100    |   68700   |  00001  |  68700   |   1   |     01    |     N      |        |
|      유한양행우      | 000105 | KR7000101006 |    0     |   78300    |   42300    |   60300   |  00001  |  60300   |   1   |     01    |     N      |        |
|      CJ대한통운      | 000120 | KR7000120006 |    0     |   162200   |   87400    |   124800  |  00001  |  124800  |   1   |     01    |     N      |        |
|

(중략 ...)
"""