import asyncio
import ebest
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
    print(response.body)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
