import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t1463InBlock": {
            "gubun": "0", # 0:전체, 1:코스피, 2:코스닥
            "jnilgubun": "0", # 0 : 당일 1 : 전일
            "jc_num": 0, # 대상제외
            "sprice": 10000, # 현재가 >= sprice
            "eprice": 1000000, # 현재가 <= eprice
            "volume": 1000000, # 거래량 >= volume
            "idx": 0, # 처음 조회시는 0 연속 조회시에 이전 조회한 OutBlock의 idx 값으로 설정
            "jc_num2": 0, # 대상제외2
        }
    }
    response = await api.request("t1463", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    print(response.body)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
