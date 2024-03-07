import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    
    while True:
        symbol = input(f'해외선물 종목코드를 입력하세요:')

        # [요청] o3105 : 해외선물현재가(종목정보)조회-API용
        request = {
            "o3105InBlock": {
                "symbol": symbol,
            },
        }
        response = await api.request("o3105", request)
        if response:
            print_table(response.body['o3105OutBlock'])
        else:
            print(f"요청실패: {api.last_message}")
    
        pass # 무한 반복으로 다른 종목정보 불러온다
    
    await api.close()

asyncio.run(main())


# Output:
'''
해외선물 종목코드를 입력하세요:HSIH24
Field Count = 58
+------------+--------------------+
|    key     |       value        |
+------------+--------------------+
|   Symbol   |       HSIH24       |
|  SymbolNm  | Hang Seng(2024.03) |
|  ApplDate  |      20240307      |
|  BscGdsCd  |        HSI         |
|  BscGdsNm  |     Hang Seng      |
|   ExchCd   |        HKEX        |
|   ExchNm   |     홍콩거래소     |
|    EcCd    |         1          |
|  CrncyCd   |        HKD         |
|   NotaCd   |         10         |
|   UntPrc   |        1.0         |
|  MnChgAmt  |    50.000000000    |
|  RgltFctr  |    1.0000000000    |
| CtrtPrAmt  |       50.00        |
| LstngMCnt  |         12         |
|   GdsCd    |        001         |
|   MrktCd   |        001         |
|  EminiCd   |         0          |
|  LstngYr   |        2024        |
|   LstngM   |         H          |
|   SeqNo    |         1          |
|  LstngDt   |      20230925      |
|   MtrtDt   |      20240327      |
|  FnlDlDt   |      20240327      |
| FstTrsfrDt |                    |
|   EcPrc    |      16436.0       |
|    DlDt    |      20240307      |
|  DlStrtTm  |       181500       |
|  DlEndTm   |       173000       |
| OvsStrDay  |      20240306      |
|  OvsStrTm  |       171500       |
| OvsEndDay  |      20240307      |
|  OvsEndTm  |       163000       |
|  DlPsblCd  |         1          |
|  MgnCltCd  |         1          |
|  OpngMgn   |      74746.00      |
|  MntncMgn  |      74746.00      |
|  OpngMgnR  |         0          |
| MntncMgnR  |         0          |
|   DotGb    |         0          |
|  TimeDiff  |         -1         |
|  OvsDate   |      20240307      |
|  KorDate   |      20240307      |
|   TrdTm    |       115956       |
|   RcvTm    |       125956       |
|    TrdP    |      16378.0       |
|    TrdQ    |         1          |
|    TotQ    |       73462        |
|   TrdAmt   |      16378.00      |
|   TotAmt   |        0.00        |
|   OpenP    |      16438.0       |
|   HighP    |      16552.0       |
|    LowP    |      16343.0       |
|   CloseP   |      16436.0       |
|   YdiffP   |       -58.0        |
| YdiffSign  |         5          |
|   Cgubun   |                    |
|    Diff    |       -0.35        |
+------------+--------------------+
'''