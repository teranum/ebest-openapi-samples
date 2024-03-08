/*
1. NET8.0 이상으로 프로젝트 생성
2. nuget 패키지 관리자
    install ConsoleTables
    install ebest.OpenAPI

3. 샘플폴더에 app_keys.cs 파일 생성
    app_keys.cs 파일에 아래와 같이 변수 세팅

    namespace CSharp;
    internal class Secret
    {
        public const string AppKey = "발급받은 앱Key";
        public const string AppSecretKey = "발급받은 앱 비밀Key";
    }


4. 샘플코드 실행

01 ~ 샘플코드는 로그인, 계좌조회, 시세 및 차트조회
10 ~ 조건검색, 실시간검색
20 ~ 웹소켓 을 이용한 실시간 시세
40 ~ 기타 샘플코드

* 샘플코드에 포함되지 않은 TR모델클래스 참조방법 (3가지)
    1. 샘플코드 Models.cs 양식으로 필요한 TR에 해당되는 블록과 모델 클래스를 직접 코딩 하거나
    2. 이베스트 OpenApi용 DevCenter(오픈소스) https://github.com/teranum/eBEST.OpenApi.DevCenter 에서 릴리즈버전 설치후 모델소스를 참조
    3. 또는 nuget ebest.OpenAPI.Models 를 이용, 이베스트 전체 TR에 해당되는 클래스가 포함되어 있음
       이 경우 코드에 using ebest.OpenAPI.Models; 추가, 또는 필요한 TR에 해당되는 클래스만 개발 프로젝트에 복사해서 사용
*/
