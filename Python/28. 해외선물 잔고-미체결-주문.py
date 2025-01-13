import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

'''
1. 해외선물 잔고 및 미체결 조회
2. 주문요청 : (매수, 매도, 정정, 취소), (시장가, 지정가)
'''

async def sample(api):
    while True:
        # 잔고 표시
        print('잔고조회중...')
        request = {
            'CIDBQ01500InBlock1': {
                'AcntTpCode': '1', # 계좌구분 : 1:위탁
                'QryDt': '', # 조회일자 : YYYYMMDD
                'BalTpCode': '1', # 잔고구분 : 1:합산, 2:건별
            },
        }
        response = await api.request('CIDBQ01500', request)
        if not response: return print(f'잔고 요청실패: {api.last_message}')
        if not response.body.__contains__('CIDBQ01500OutBlock2'):
            print('보유잔고가 없습니다.')
        else:
            balances = [dict({
                '종목코드': x['IsuCodeVal'],
                '구분': '매도' if x['BnsTpCode'] == '1' else '매수',
                '잔고수량': x['BalQty'],
                '평균단가': x['PchsPrc'],
                '현재가': x['OvrsDrvtNowPrc'],
                '평가손익': x['AbrdFutsEvalPnlAmt'],
            }) for x in response.body['CIDBQ01500OutBlock2']]
            print_table(balances)
        
        # 미체결 표시
        print('미체결조회중...')
        request = {
            'CIDBQ01800InBlock1': {
                'IsuCodeVal': '', # 종목코드
                'OrdDt': '', # 주문일자 : YYYYMMDD
                'ThdayTpCode': '', # 당일구분 : SPACE
                'OrdStatCode': '2', # 주문상태 : 0:전체, 1:체결, 2:미체결
                'BnsTpCode': '0', # 매매구분 : 0:전체, 1:매도, 2:매수
                'QryTpCode': '1', # 조회구분 : 1:역순 2:정순
                'OrdPtnCode': '00', # 주문유형 : 00:전체 01:일반 02:Average 03:Spread
                'OvrsDrvtFnoTpCode': 'A', # A:전체 F:선물 O:옵션
            },
        }
        response = await api.request('CIDBQ01800', request)
        if not response: return print(f'미체결 요청실패: {api.last_message}')
        if not response.body.__contains__('CIDBQ01800OutBlock2'):
            print('미체결내역이 없습니다.')
        else:
            unfills = [dict({
                '주문번호': x['OvrsFutsOrdNo'],
                '종목코드': x['IsuCodeVal'],
                '구분': x['BnsTpNm'],
                '주문수량': x['OrdQty'],
                '주문가격': x['OvrsDrvtOrdPrc'],
                '미체결잔량': x['UnercQty'],
                '원주문번호': x['OvrsFutsOrgOrdNo'],
                '주문시간': x['OrdTime'],
            }) for x in response.body['CIDBQ01800OutBlock2']]
            print_table(unfills)

        # 주문요청 입력
        주문요청 = await ainput(f'주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):')
        if 주문요청 == '1' or 주문요청 == '2':
            # 주문 정보 입력
            종목코드 = await ainput(f'해외선물옵션 종목코드를 입력하세요:')
            매매구분 = '2' if 주문요청 == '1' else '1'
            주문구분 = await ainput(f'주문구분을 입력하세요 (1:시장가, 2:지정가):')
            주문가격 = float(0 if 주문구분 == '1' else await ainput(f'주문가격을 입력하세요:'))
            주문수량 = int(await ainput(f'주문수량을 입력하세요:'))
        
            # 신규주문 요청
            request = {
                'CIDBT00100InBlock1': {
                    'OrdDt': '', # 주문일자 : YYYYMMDD
                    'IsuCodeVal': 종목코드,
                    'FutsOrdTpCode': '1', # 선물주문구분코드 :1:신규
                    'BnsTpCode': 매매구분, # 매매구분코드 : 1:매도 2:매수
                    'AbrdFutsOrdPtnCode': 주문구분, # 해외선물주문유형코드 : 1:시장가, 2:지정가
                    'CrcyCode': '', # 통화코드 : SPACE
                    'OvrsDrvtOrdPrc': 주문가격, # 해외파생상품주문가격
                    'CndiOrdPrc': 0, # 조건주문가격
                    'OrdQty': 주문수량, # 주문수량
                    'PrdtCode': '', # 상품코드 : SPACE
                    'DueYymm': '', # 만기년월 : SPACE
                    'ExchCode': '', # 거래소코드 : SPACE
                },
            }
            response = await api.request('CIDBT00100', request)
            if not response: print(f'주문 요청실패: {api.last_message}')
            elif response.body.__contains__('rsp_msg'):
                print(f'주문 요청 결과: {response.body['rsp_msg']}')
    
        elif 주문요청 == '3' or 주문요청 == '4':
            # 정정/취소 정보 입력
            주문번호 = await ainput(f'주문번호를 입력하세요:')
            정정가격 = float(await ainput(f'정정가격을 입력하세요:') if 주문요청 == '3' else 0)
        
            # 주문번호 일치하는 미체결내역 조회
            matched_unfill = next((x for x in unfills if x['주문번호'] == 주문번호), None)
            if not matched_unfill:
                 print(f'주문번호 {주문번호}에 대한 미체결내역이 없습니다.')
            else:
                if 주문요청 == '3':
                    # 정정요청
                    request = {
                        'CIDBT00900InBlock1': {
                            'OrdDt': '', # 주문일자 : YYYYMMDD
                            'OvrsFutsOrgOrdNo': 주문번호, # 해외파생원주문번호
                            'IsuCodeVal': matched_unfill['종목코드'], # 종목코드
                            'FutsOrdTpCode': '2', # 선물주문구분코드 : 2:정정
                            'BnsTpCode': '1' if matched_unfill['구분'] == '매도' else '2', # 매매구분코드 : 1:매도, 2:매수
                            'FutsOrdPtnCode': '2', # 선물주문유형코드 : 2:지정가
                            'CrcyCodeVal': '', # 통화코드 : SPACE
                            'OvrsDrvtOrdPrc': 정정가격, # 해외파생상품주문가격
                            'CndiOrdPrc': 0, # 조건주문가격
                            'OrdQty': matched_unfill['미체결잔량'], # 주문수량
                            'OvrsDrvtPrdtCode': '', # 해외파생상품코드 : SPACE
                            'DueYymm': '', # 만기년월 : SPACE
                            'ExchCode': '', # 거래소코드 : SPACE
                        },
                    }
                    response = await api.request('CIDBT00900', request)
                    if not response: print(f'정정 요청실패: {api.last_message}')
                    elif response.body.__contains__('rsp_msg'):
                        print(f'정정 요청 결과: {response.body['rsp_msg']}')
                else:
                    # 취소요청
                    request = {
                        'CIDBT01000InBlock1': {
                            'OrdDt': '', # 주문일자 : YYYYMMDD
                            'IsuCodeVal': matched_unfill['종목코드'], # 종목코드
                            'OvrsFutsOrgOrdNo': 주문번호, # 해외파생원주문번호
                            'FutsOrdTpCode': '3', # 선물주문구분코드 : 3:취소
                            'PrdtTpCode': '', # 상품유형코드 : SPACE
                            'ExchCode': '', # 거래소코드 : SPACE
                        },
                    }
                    response = await api.request('CIDBT01000', request)
                    if not response: return print(f'취소 요청실패: {api.last_message}')
                    if response.body.__contains__('rsp_msg'):
                        print(f'취소 요청 결과: {response.body['rsp_msg']}')
        
        await asyncio.sleep(1) # 1초 대기 후 반복
        pass
    
    ... # 다른 작업 수행
    await api.close()

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
연결성공, 접속서버: 모의투자
잔고조회중...
Row Count = 1
+----------+------+----------+-------------------+-------------------+----------+
| 종목코드 | 구분 | 잔고수량 |      평균단가     |       현재가      | 평가손익 |
+----------+------+----------+-------------------+-------------------+----------+
|  HSIK24  | 매도 |    1     | 18500.00000000000 | 18500.00000000000 |   0.00   |
+----------+------+----------+-------------------+-------------------+----------+
미체결조회중...
Row Count = 2
+------------+----------+------+----------+-------------------+------------+------------+-----------+
|  주문번호  | 종목코드 | 구분 | 주문수량 |      주문가격     | 미체결잔량 | 원주문번호 |  주문시간 |
+------------+----------+------+----------+-------------------+------------+------------+-----------+
| 0000000961 |  HSIK24  | 매수 |    1     | 18480.00000000000 |     1      | 0000000960 | 141544438 |
| 0000000959 |  HSIK24  | 매도 |    2     | 18510.00000000000 |     2      | 0000000000 | 141428628 |
+------------+----------+------+----------+-------------------+------------+------------+-----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):3
주문번호를 입력하세요:0000000961
정정가격을 입력하세요:18490
정정 요청 결과: 모의투자 정정주문이 완료 되었습니다.
...
'''
