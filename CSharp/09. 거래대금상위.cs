using eBEST.OpenApi;

namespace CSharp;

internal class _09 : SampleBase
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

        // [요청] t1463 : 거래대금상위
        t1463 tr_data = new()
        {
            t1463InBlock = new("0", "0", 0, 10000, 3000000, 1000000, 0, 0),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1463OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1463OutBlock 데이터 처리
        print(tr_data.t1463OutBlock);
        print(tr_data.t1463OutBlock1);
    }

    // t1463 : 거래대금상위
    public record t1463InBlock(string gubun, string jnilgubun, long jc_num, int sprice, int eprice, long volume, int idx, long jc_num2);
    public record t1463OutBlock(int idx);
    public record t1463OutBlock1(string hname, int price, string sign, int change, double diff, long volume, long value, long jnilvalue, double bef_diff, string shcode, string filler, long jnilvolume);

    [Path("/stock/high-item")]
    public class t1463 : TrBase
    {
        // 요청
        public t1463InBlock? t1463InBlock { get; set; }

        // 응답
        public t1463OutBlock? t1463OutBlock { get; set; }
        public t1463OutBlock1[]? t1463OutBlock1 { get; set; }
    }
}
