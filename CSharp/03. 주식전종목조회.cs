using eBEST.OpenApi;

namespace CSharp;

internal class _03
{
    static void print(string lineText) => Console.WriteLine(lineText);
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

        // [요청] t8436 : 주식종목조회 API용
        t8436 tr_data = new()
        {
            t8436InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8436OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8436OutBlock 데이터 처리
        print($"Count={tr_data.t8436OutBlock.Length}");
        foreach (var item in tr_data.t8436OutBlock)
        {
            print($"{item.hname} : {item.expcode}");
        }
    }

    // t8436 : 주식종목조회 API용
    public record t8436InBlock(string gubun);
    public record t8436OutBlock(string hname, string shcode, string expcode, string etfgubun, int uplmtprice, int dnlmtprice, int jnilclose, string memedan, int recprice, string gubun, string bu12gubun, string spac_gubun, string filler);

    [Path("/stock/etc")]
    public class t8436 : TrBase
    {
        // 요청
        public t8436InBlock? t8436InBlock { get; set; }

        // 응답
        public t8436OutBlock[]? t8436OutBlock { get; set; }
    }

}
