'''
가능한 파이썬 64비트 최신버전 사용 권장 (3.11 이상)

패키지 설치 (가능한 최신버전 사용 권장)
pip install ebest

    일부 샘플은 prettytable, cryptography, padas, ta, matplotlib 패키지 필요
    pip install prettytable
    pip install cryptography
    pip install pandas
    pip install ta
    pip install matplotlib

    QT샘플은 PyQt6, qasync 필요
    pip install PyQt6
    pip install qasync


샘플 코드 이용
1. 샘플폴더에 app_keys.py 파일 생성
2. app_keys.py 파일에 아래와 같이 변수 세팅
    appkey = '발급받은 앱Key'
    appsecretkey = '발급받은 앱 비밀Key'
3. 샘플코드 실행

LS-OpenApi DevCenter 실행
python DevCenter.py
    LS증권 OpenApi 모든 요청/실시간 테스트 가능
    테스트베드 기능 포함
    개별 샘플파일 테스트 가능
    PyQt6, qasync, prettytable, cryptography 필요

샘플목록
01 ~ 로그인, 계좌조회, 시세 및 차트조회
10 ~ 조건검색, 실시간검색
20 ~ 웹소켓 을 이용한 실시간 시세, 해외선물 조회/실시간
30 ~ PyQt6를 이용한 GUI 샘플코드
40 ~ 기타 샘플코드

'''
