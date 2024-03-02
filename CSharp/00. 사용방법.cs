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
40 ~ 실전 응용
*/
