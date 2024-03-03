"""
패키지 설치
pip install asyncio
pip install ebest

(일부 샘플은 prettytable 패키지 필요)

ebest 모듈사용
프로퍼티:
    connected -> bool: 연결여부 (연결: True, 미연결: False)
    is_simulation -> bool: 모의투자인지 여부 (모의투자: True, 실거래: False))
    last_message -> str: 마지막 메시지
    mac_address -> str: MAC주소 (법인인 경우 필수 세팅)
    
메소드:
    login(appkey:str, appsecretkey:str) -> bool: 로그인
        appkey:str - 앱키
        appsecretkey:str - 앱시크릿키
        reutrn: bool - 로그인 성공여부 (성공: True, 실패: False)
        
    request(tr_cd:str, data:dict, *, path:str=None, tr_cont:str="N", tr_cont_key:str="0") -> None: 요청
        tr_cd:str - TR 코드
        data:dict - 요청 데이터
        * - path, tr_cont, tr_cont_key는 옵션(기본값으로 설정됨)
        path:str - PATH경로, 기본값: None, 설정 필요시 URL값으로 세팅 ex) "/stock/market-data"
        tr_cont:str - 연속조회여부 (연속조회: "Y", 단순조회: "N"), 기본값: "N"
        tr_cont_key:str - 연속조회키 (연속조회여부가 "Y"인 경우 필수 세팅), 기본값: "0"
        return: 응답 데이터 (dict), 요청 실패시 None
    
    add_realtime(tr_cd:str, tr_key:str) -> bool: 실시간 등록
        tr_cd:str - TR 코드
        tr_key:str - 키
        return: bool - 성공여부 (성공: True, 실패: False)
        
    remove_realtime(tr_cd:str, tr_key:str) -> bool: 실시간 해제
        tr_cd:str - TR 코드
        tr_key:str - 키
        return: bool - 성공여부 (성공: True, 실패: False)
        
    close() -> None: 연결 종료
        
이벤트:
    on_message(msg:str): 메시지 수신 이벤트 (오류 또는 웹소켓 끊김시 발생)
        msg - 메시지
        
    on_realtime(trcode:str, key:str, realtimedata:dict): 실시간 수신 이벤트 (실시간 데이터 수신시 발생)
        trcode:str - TR 코드
        key:str - 키
        realtimedata - 실시간 데이터
    
샘플 코드 이용
1. 샘플폴더에 app_keys.py 파일 생성
2. app_keys.py 파일에 아래와 같이 변수 세팅
    appkey = "발급받은 앱Key"
    appsecretkey = "발급받은 앱 비밀Key"
3. 샘플코드 실행

01 ~ 샘플코드는 로그인, 계좌조회, 시세 및 차트조회
10 ~ 조건검색, 실시간검색
20 ~ 웹소켓 을 이용한 실시간 시세
30 ~ PyQt6를 이용한 GUI 샘플코드

"""
