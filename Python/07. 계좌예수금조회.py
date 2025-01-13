import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    request = {
        'CSPAQ22200InBlock1': {
            'BalCreTp': '0',
        }
    }
    response = await api.request('CSPAQ22200', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    print_table(response.body['CSPAQ22200OutBlock1'])
    print_table(response.body['CSPAQ22200OutBlock2'])
    

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')
    await sample(api)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())

# Output:
'''
Field Count = 5
+-----------+-------------+
|    key    |    value    |
+-----------+-------------+
|   RecCnt  |      1      |
| MgmtBrnNo |             |
|   AcntNo  | XXXXXXXXXXX |
|    Pwd    |   ********  |
|  BalCreTp |      0      |
+-----------+-------------+
Field Count = 37
+------------------------+-------------+
|          key           |    value    |
+------------------------+-------------+
|         RecCnt         |      1      |
|         BrnNm          | XXXXXXXXXXX |
|         AcntNm         |    XXXXX    |
|     MnyOrdAbleAmt      |      0      |
|    SubstOrdAbleAmt     |      0      |
|      SeOrdAbleAmt      |      0      |
...
'''