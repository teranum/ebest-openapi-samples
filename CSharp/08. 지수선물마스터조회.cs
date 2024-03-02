using eBEST.OpenApi;

namespace CSharp;

internal class _08 : SampleBase
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

        // [요청] t8432 : 지수선물마스터조회API용
        t8432 tr_data = new()
        {
            t8432InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8432OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8432OutBlock 데이터 처리
        print(tr_data.t8432OutBlock);
    }

    // t8432 : 지수선물마스터조회API용
    public record t8432InBlock(string gubun);
    public record t8432OutBlock(string hname, string shcode, string expcode, double uplmtprice, double dnlmtprice, double jnilclose, double jnilhigh, double jnillow, double recprice);

    [Path("/futureoption/market-data")]
    public class t8432 : TrBase
    {
        // 요청
        public t8432InBlock? t8432InBlock { get; set; }

        // 응답
        public t8432OutBlock[]? t8432OutBlock { get; set; }
    }
}
