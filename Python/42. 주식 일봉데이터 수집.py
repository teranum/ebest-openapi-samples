import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey, stock_dir
# app_keys.py 파일에 appkey, appsecretkey, stock_dir 변수를 정의하고 사용하세요
# stock_dir 변수에 저장할 디렉토리를 설정하세요. (ex. stock_dir = 'C:/stockdata')

'''
주식시장 전체종목 일봉데이터 수집
'''
async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    # [요청] t8436 : 주식종목조회 API용
    request = {
        "t8436InBlock": {
            "gubun": "0",
        },
    }
    response = await api.request("t8436", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    all_items = response.body['t8436OutBlock']
    
    # 시장전체 종목중, 주식종목만 필터 (ETF, ETN, 기타 이상한 종목 제외)
    stock_codes = [item["shcode"] for item in all_items if item["etfgubun"] == "0" and item["bu12gubun"] == "01" and item["spac_gubun"] == "N"]
    
    # 또는 필요한 종목만 설정 (ex. stock_codes = ['005930','000020'])
    # stock_codes = ['005930','000020'];

    req_count = len(stock_codes)
    print(f"{req_count}개 종목 일봉데이터 수집 시작, 예상 소요시간 {req_count * 3.5} 초")
    # 종목 일봉 데이터 조회
    for i in range(0, req_count, 1):
        code = stock_codes[i]
        print(f"{code} 요청중... 남은시간 {(req_count - i - 1) * 3.5}초")
        # [요청] t8410 : API전용주식챠트(일주월년)
        request = {
            "t8410InBlock": {
                "shcode": code, # 종목코드
                "gubun": "2", # 주기구분(2:일3:주4:월5:년)
                "qrycnt": 500, # 요청건수(최대-압축:2000비압축:500)
                "sdate": "", # 시작일자
                "edate": "99999999", # 종료일자
                "cts_date": "", # 연속일자
                "comp_yn": "N", # 압축여부(Y:압축N:비압축)
                "sujung": "Y", # 수정주가여부(Y:적용N:비적용)
            }
        }
        response = await api.request("t8410", request)
        if not response:
            print(f"요청실패: {code}, {api.last_message}")
        else:
            data = response.body["t8410OutBlock1"]
            # 데이터를 csv로 저장
            TOHLCV = [list((x['date'], x['open'], x['high'], x['low'], x['close'], x['jdiff_vol'])) for x in data]
            TOHLCV_to_csv(f"{stock_dir}/{code}.csv", TOHLCV)
            
        if i < req_count - 1: # 마지막 종목이 아니면 약간의 딜레이
            await asyncio.sleep(3.5) # 3.5초간 대기 (조회제한 10분단 200건, 최대 3초당 1건 요청 가능)
        pass

    
    await api.close()



asyncio.run(main())


# Output:
"""
2536개 종목 일봉데이터 수집 시작, 예상 소요시간 8876.0 초
000020 요청중... 남은시간 8872.5초
000040 요청중... 남은시간 8869.0초
000050 요청중... 남은시간 8865.5초
000070 요청중... 남은시간 8862.0초
000075 요청중... 남은시간 8858.5초
...
파일 000020.csv
time,open,high,low,close,volume
20220221,12350,13050,12300,12900,536897
20220222,12500,12950,12500,12750,208419
20220223,12800,13000,12650,12650,175395
20220224,12500,12700,12150,12150,233193
20220225,12350,12600,12200,12450,234491
20220228,12250,12800,12250,12650,128937
20220302,12650,12900,12600,12800,136796
20220303,12850,13100,12700,12900,208456
20220304,12850,13000,12750,12950,142363
20220307,12950,13200,12750,12900,194201
...
"""
