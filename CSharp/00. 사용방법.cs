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

* 샘플프로젝트는 이용된 TR에 해당되는 모델클래스를 nuget ebest.OpenAPI.Models를 이용하여 참조하였음
        - Program.cs 파일에 global using ebest.OpenAPI.Models; 추가)
        - ebest.OpenAPI.Models 에는 이베스트 전체 TR에 해당되는 클래스가 포함되어 있음
        - 일부만 필요할 경우, 필요한 TR에 해당되는 클래스만 개발 프로젝트에 복사해서 사용
*/
