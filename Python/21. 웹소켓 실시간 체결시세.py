import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api:ebest.OpenApi):
    # key = '0059300' #  단건: 삼성전자 주식 실시간 시세 요청, 국내주식은 6자리 해외선물은 8자리
    key = '005930000660' # 연속: 삼성전자, SK하이닉스 주식 실시간 시세 요청, 국내주식은 6자리 해외선물은 8자리
    ok = await api.add_realtime('S3_', key)
    if not ok:
        return print(f"실시간등록 실패: {api.last_message}")
    
    # 1분후 실시간 시세 중지
    print('1분동안 실시간 작동중...');
    await asyncio.sleep(60)
    await api.remove_realtime('S3_', key)
    print('실시간중지');
    

def on_message(api:ebest.OpenApi, msg:str): print(f'on_message: {msg}')

def on_realtime(api:ebest.OpenApi, trcode:str, key:str, realtimedata:dict):
    if trcode == 'S3_':
        print(f'{trcode}, {key}, {realtimedata}')
    

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')

    # 이벤트 핸들러 등록
    api.on_message.connect(on_message)
    api.on_realtime.connect(on_realtime)

    await sample(api)

    # 이벤트 핸들러 해제
    api.on_message.disconnect(on_message)
    api.on_realtime.disconnect(on_realtime)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())

# Output:
'''
S3_, 005930, {'mdchecnt': '29019', 'sign': '5', 'mschecnt': '42887', 'mdvolume': '8092721', 'w_avrg': '54106', 'cpower': '77.87', 'offerho': '54000', 'cvolume': '438', 'high': '54600', 'bidho': '53900', 'low': '53700', 'price': '53900', 'cgubun': '-', 'value': '797428', 'change': '200', 'shcode': '005930', 'chetime': '151055', 'opentime': '090010', 'lowtime': '104355', 'volume': '14738346', 'drate': '-0.37', 'hightime': '090102', 'jnilvolume': '13529438', 'msvolume': '6301901', 'open': '54200', 'status': '00'}
S3_, 000660, {'mdchecnt': '27348', 'sign': '2', 'mschecnt': '31689', 'mdvolume': '1175070', 'w_avrg': '195052', 'cpower': '99.02', 'offerho': '194800', 'cvolume': '1', 'high': '197900', 'bidho': '194700', 'low': '193600', 'price': '194700', 'cgubun': '-', 'value': '484105', 'change': '400', 'shcode': '000660', 'chetime': '151055', 'opentime': '090005', 'lowtime': '090900', 'volume': '2481923', 'drate': '0.21', 'hightime': '093908', 'jnilvolume': '4098160', 'msvolume': '1163587', 'open': '194300', 'status': '00'}
S3_, 000660, {'mdchecnt': '27348', 'sign': '2', 'mschecnt': '31690', 'mdvolume': '1175070', 'w_avrg': '195052', 'cpower': '99.02', 'offerho': '194800', 'cvolume': '9', 'high': '197900', 'bidho': '194700', 'low': '193600', 'price': '194800', 'cgubun': '+', 'value': '484107', 'change': '500', 'shcode': '000660', 'chetime': '151055', 'opentime': '090005', 'lowtime': '090900', 'volume': '2481932', 'drate': '0.26', 'hightime': '093908', 'jnilvolume': '4098160', 'msvolume': '1163596', 'open': '194300', 'status': '00'}
S3_, 000660, {'mdchecnt': '27349', 'sign': '2', 'mschecnt': '31690', 'mdvolume': '1175075', 'w_avrg': '195052', 'cpower': '99.02', 'offerho': '194800', 'cvolume': '5', 'high': '197900', 'bidho': '194700', 'low': '193600', 'price': '194700', 'cgubun': '-', 'value': '484108', 'change': '400', 'shcode': '000660', 'chetime': '151055', 'opentime': '090005', 'lowtime': '090900', 'volume': '2481937', 'drate': '0.21', 'hightime': '093908', 'jnilvolume': '4098160', 'msvolume': '1163596', 'open': '194300', 'status': '00'}
S3_, 005930, {'mdchecnt': '29019', 'sign': '5', 'mschecnt': '42888', 'mdvolume': '8092721', 'w_avrg': '54106', 'cpower': '77.87', 'offerho': '54000', 'cvolume': '10', 'high': '54600', 'bidho': '53900', 'low': '53700', 'price': '54000', 'cgubun': '+', 'value': '797428', 'change': '100', 'shcode': '005930', 'chetime': '151055', 'opentime': '090010', 'lowtime': '104355', 'volume': '14738356', 'drate': '-0.18', 'hightime': '090102', 'jnilvolume': '13529438', 'msvolume': '6301911', 'open': '54200', 'status': '00'}
S3_, 005930, {'mdchecnt': '29020', 'sign': '5', 'mschecnt': '42888', 'mdvolume': '8092724', 'w_avrg': '54106', 'cpower': '77.87', 'offerho': '54000', 'cvolume': '3', 'high': '54600', 'bidho': '53900', 'low': '53700', 'price': '53900', 'cgubun': '-', 'value': '797428', 'change': '200', 'shcode': '005930', 'chetime': '151055', 'opentime': '090010', 'lowtime': '104355', 'volume': '14738359', 'drate': '-0.37', 'hightime': '090102', 'jnilvolume': '13529438', 'msvolume': '6301911', 'open': '54200', 'status': '00'}
S3_, 005930, {'mdchecnt': '29021', 'sign': '5', 'mschecnt': '42888', 'mdvolume': '8092737', 'w_avrg': '54106', 'cpower': '77.87', 'offerho': '54000', 'cvolume': '13', 'high': '54600', 'bidho': '53900', 'low': '53700', 'price': '53900', 'cgubun': '-', 'value': '797429', 'change': '200', 'shcode': '005930', 'chetime': '151055', 'opentime': '090010', 'lowtime': '104355', 'volume': '14738372', 'drate': '-0.37', 'hightime': '090102', 'jnilvolume': '13529438', 'msvolume': '6301911', 'open': '54200', 'status': '00'}
S3_, 005930, {'mdchecnt': '29021', 'sign': '5', 'mschecnt': '42889', 'mdvolume': '8092737', 'w_avrg': '54106', 'cpower': '77.87', 'offerho': '54000', 'cvolume': '100', 'high': '54600', 'bidho': '53900', 'low': '53700', 'price': '54000', 'cgubun': '+', 'value': '797434', 'change': '100', 'shcode': '005930', 'chetime': '151056', 'opentime': '090010', 'lowtime': '104355', 'volume': '14738472', 'drate': '-0.18', 'hightime': '090102', 'jnilvolume': '13529438', 'msvolume': '6302011', 'open': '54200', 'status': '00'}
'''