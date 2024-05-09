import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

'''
1. 국내선물 잔고 및 미체결 조회
2. 주문요청 : (매수, 매도, 정정, 취소), (시장가, 지정가)
'''

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f'연결실패: {api.last_message}')
    print('연결성공, 접속서버: ' + ('모의투자' if api.is_simulation else '실투자'))
    
    while True:
        # 잔고 표시
        print('잔고조회중...')
        request = {
            't0441InBlock': {
                'cts_expcode': '',
                'cts_medocd': '',
            },
        }
        response = await api.request('t0441', request)
        if not response: return print(f'잔고 요청실패: {api.last_message}')
        if not response.body.__contains__('t0441OutBlock1'):
            print('보유잔고가 없습니다.')
        else:
            balances = [dict({
                '종목코드': x['expcode'],
                '구분': x['medosu'],
                '잔고수량': x['jqty'],
                '청산가능수량': x['cqty'],
                '평균단가': x['pamt'],
                '현재가': x['price'],
                '평가손익': x['dtsunik1'],
            }) for x in response.body['t0441OutBlock1']]
            print_table(balances)
        
        # 미체결 표시
        print('미체결조회중...')
        request = {
            't0434InBlock': {
                'expcode': '', # 종목코드
                'chegb': '2', # 체결구분 : 0:전체, 1:체결, 2:미체결
                'sortgb': '1', # 정렬기준 : 1:주문번호 역순, 2:주문번호 순
                'cts_ordno': '', # 연속조회키 : 연속조회시 사용
            },
        }
        response = await api.request('t0434', request)
        if not response: return print(f'미체결 요청실패: {api.last_message}')
        if not response.body.__contains__('t0434OutBlock1'):
            print('미체결내역이 없습니다.')
        else:
            unfills = [dict({
                '주문번호': x['ordno'],
                '종목코드': x['expcode'],
                '구분': x['medosu'],
                '주문수량': x['qty'],
                '주문가격': x['price'],
                '미체결잔량': x['ordrem'],
                '원주문번호': x['orgordno'],
                '주문시간': x['ordtime'],
            }) for x in response.body['t0434OutBlock1']]
            print_table(unfills)

        # 주문요청 입력
        주문요청 = input(f'주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):')
        if 주문요청 == '1' or 주문요청 == '2':
            # 주문 정보 입력
            종목코드 = input(f'선물옵션 종목코드를 입력하세요 (ex 국선 24년 6월물 경우 101V6000):')
            매매구분 = '2' if 주문요청 == '1' else '1'
            주문구분 = input(f'주문구분을 입력하세요 (00:지정가, 03:시장가):')
            주문가격 = float(0 if 주문구분 == '03' else input(f'주문가격을 입력하세요:'))
            주문수량 = int(input(f'주문수량을 입력하세요:'))
        
            # 신규주문 요청
            request = {
                'CFOAT00100InBlock1': {
                    'FnoIsuNo': 종목코드, # 종목코드
                    'BnsTpCode': 매매구분, # 매매구분: 1:매도 2:매수
                    'FnoOrdprcPtnCode': 주문구분, # 호가유형코드: 00:지정가 03:시장가
                    'FnoOrdPrc': 주문가격, # 주문가
                    'OrdQty': 주문수량, # 주문수량
                },
            }
    
            response = await api.request('CFOAT00100', request)
            if not response: print(f'주문 요청실패: {api.last_message}')
            elif response.body.__contains__('rsp_msg'):
                print(f'주문 요청 결과: {response.body['rsp_msg']}')
    
        elif 주문요청 == '3' or 주문요청 == '4':
            # 정정/취소 정보 입력
            주문번호 = int(input(f'주문번호를 입력하세요:'))
            정정가격 = float(input(f'정정가격을 입력하세요:') if 주문요청 == '3' else 0)
        
            # 주문번호 일치하는 미체결내역 조회
            matched_unfill = next((x for x in unfills if x['주문번호'] == 주문번호), None)
            if not matched_unfill:
                 print(f'주문번호 {주문번호}에 대한 미체결내역이 없습니다.')
            else:
                if 주문요청 == '3':
                    # 정정요청
                    request = {
                        'CFOAT00200InBlock1': {
                            'OrgOrdNo': 주문번호, # 원주문번호
                            'FnoIsuNo': matched_unfill['종목코드'], # 종목코드
                            'FnoOrdprcPtnCode': '00', # 호가유형코드: 00@지정가, 03@시장가 ...
                            'FnoOrdPrc': 정정가격, # 주문가
                            'MdfyQty': matched_unfill['미체결잔량'], # 정정수량
                        },
                    }
                    response = await api.request('CFOAT00200', request)
                    if not response: print(f'정정 요청실패: {api.last_message}')
                    elif response.body.__contains__('rsp_msg'):
                        print(f'정정 요청 결과: {response.body['rsp_msg']}')
                else:
                    # 취소요청
                    request = {
                        'CFOAT00300InBlock1': {
                            'OrgOrdNo': 주문번호, # 원주문번호
                            'FnoIsuNo': matched_unfill['종목코드'], # 종목코드
                            'CancQty': matched_unfill['미체결잔량'], #
                         },
                    }
                    response = await api.request('CFOAT00300', request)
                    if not response: return print(f'취소 요청실패: {api.last_message}')
                    if response.body.__contains__('rsp_msg'):
                        print(f'취소 요청 결과: {response.body['rsp_msg']}')
        
        await asyncio.sleep(1) # 1초 대기 후 반복
        pass
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())

# Output:
'''
연결성공, 접속서버: 모의투자
잔고조회중...
Row Count = 1
+----------+------+----------+--------------+----------+--------+----------+
| 종목코드 | 구분 | 잔고수량 | 청산가능수량 | 평균단가 | 현재가 | 평가손익 |
+----------+------+----------+--------------+----------+--------+----------+
| 101V6000 | 매수 |    1     |      1       |  372.10  | 372.25 |  37500   |
+----------+------+----------+--------------+----------+--------+----------+
미체결조회중...
Row Count = 1
+----------+----------+------+----------+----------+------------+------------+----------+
| 주문번호 | 종목코드 | 구분 | 주문수량 | 주문가격 | 미체결잔량 | 원주문번호 | 주문시간 |
+----------+----------+------+----------+----------+------------+------------+----------+
|  22576   | 101V6000 | 매수 |    1     |  370.00  |     1      |     0      | 12584878 |
+----------+----------+------+----------+----------+------------+------------+----------+
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):3
주문번호를 입력하세요:22576
정정가격을 입력하세요:371
정정 요청 결과: 모의투자 정정주문이 완료 되었습니다.
...
'''
