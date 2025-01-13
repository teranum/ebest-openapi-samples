import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    request = {
        't8432InBlock': {
            'gubun': '0',
        }
    }
    response = await api.request('t8432', request)
    if not response: return print(f'요청실패: {api.last_message}')
    
    print_table(response.body['t8432OutBlock'])
    

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
Row Count = 13
+--------------+----------+--------------+------------+------------+-----------+----------+---------+----------+
|    hname     |  shcode  |   expcode    | uplmtprice | dnlmtprice | jnilclose | jnilhigh | jnillow | recprice |
+--------------+----------+--------------+------------+------------+-----------+----------+---------+----------+
|    F 2403    | 101V3000 | KR4101V30005 |   385.75   |   328.65   |   357.20  |  358.10  |  352.70 |  357.20  |
|    F 2406    | 101V6000 | KR4101V60002 |   386.50   |   329.30   |   357.90  |  359.15  |  353.75 |  357.90  |
|    F 2409    | 101V9000 | KR4101V90009 |   388.90   |   331.30   |   360.10  |  360.10  |  360.10 |  360.10  |
|    F 2412    | 101VC000 | KR4101VC0004 |   390.70   |   332.90   |   361.80  |  361.80  |  358.75 |  361.80  |
|    F 2506    | 101W6000 | KR4101W60000 |   394.65   |   336.25   |   365.45  |   0.00   |   0.00  |  365.45  |
|    F 2512    | 101WC000 | KR4101WC0003 |   399.35   |   340.25   |   369.80  |   0.00   |   0.00  |  369.80  |
|    F 2612    | A016C000 | KR4A016C0004 |   405.15   |   345.15   |   375.15  |   0.00   |   0.00  |  375.15  |
| F SP 03-2406 | 401V3V6S | KR4401V3V6S0 |   18.55    |   -17.15   |    1.10   |   1.15   |   0.95  |   0.00   |
| F SP 03-2409 | 401V3V9S | KR4401V3V9S4 |   20.75    |   -14.95   |    0.00   |   0.00   |   0.00  |   0.00   |
| F SP 03-2412 | 401V3VCS | KR4401V3VCS0 |   22.45    |   -13.25   |    0.00   |   0.00   |   0.00  |   0.00   |
| F SP 03-2506 | 401V3W6S | KR4401V3W6S9 |   26.10    |   -9.60    |    0.00   |   0.00   |   0.00  |   0.00   |
| F SP 03-2512 | 401V3WCS | KR4401V3WCS8 |   30.45    |   -5.25    |    0.00   |   0.00   |   0.00  |   0.00   |
| F SP 03-2612 | 401V36CS | KR4401V36CS2 |   35.80    |    0.10    |    0.00   |   0.00   |   0.00  |   0.00   |
+--------------+----------+--------------+------------+------------+-----------+----------+---------+----------+
'''