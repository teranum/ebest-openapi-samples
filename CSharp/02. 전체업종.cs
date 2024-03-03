using eBEST.OpenApi;

namespace CSharp;

internal class _02 : SampleBase
{
    public static async Task Main()
    {
        // API 생성
        var api = new EBestOpenApi();
        // 로그인
        if (!await api.ConnectAsync(Secret.AppKey, Secret.AppSecretKey))
        {
            print($"연결실패: {api.LastErrorMessage}");
            return;
        }
        print($"연결성공, 접속서버: {(api.ServerType == EBestOpenApi.SERVER_TYPE.모의투자 ? "모의투자" : "실투자")}");

        // [요청] t8424 : 전체업종
        t8424 tr_data = new()
        {
            t8424InBlock = new("1"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8424OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8424OutBlock 데이터 처리
        print(tr_data.t8424OutBlock);
    }

    // t8424 : 전체업종
    public record t8424InBlock(string gubun1);
    public record t8424OutBlock(string hname, string upcode);

    [Path("/indtp/market-data")]
    public class t8424 : TrBase
    {
        // 요청
        public t8424InBlock? t8424InBlock { get; set; }

        // 응답
        public t8424OutBlock[]? t8424OutBlock { get; set; }
    }

}

// Output:
/*
t8424OutBlock[], Field Count = 2, Data Count = 57
| hname                | upcode |
|----------------------|--------|
| 종       합          | 001    |
| 대   형  주          | 002    |
| 중   형  주          | 003    |
| 소   형  주          | 004    |
| 음 식 료 업          | 005    |
| 섬 유 의 복          | 006    |
| 종 이 목 재          | 007    |
| 화       학          | 008    |
...
*/
