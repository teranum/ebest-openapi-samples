import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    print('연결성공, 접속서버: ' + ('모의투자' if api.is_simulation else '실투자'))
    
    ... # 다른 작업 수행


async def main():
    api=ebest.OpenApi()
    await sample(api)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())

# Output:
'''
연결성공, 접속서버: 실투자
'''