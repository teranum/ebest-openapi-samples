namespace CSharp;

// 로그인 기능은 SampleBase Main 함수에서 구현 되어 있음
internal class _01 : SampleBase
{
    public override Task ActionImplement()
    {
        print("로그인 기능은 SampleBase Main 함수에서 구현 되어 있음");
        return Task.CompletedTask;
    }
}

// Output
/*
연결성공, 접속서버: 실투자
로그인 기능은 SampleBase Main 함수에서 구현 되어 있음
*/
