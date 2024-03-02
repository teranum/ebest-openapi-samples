using eBEST.OpenApi;

namespace CSharp;

internal class _05 : SampleBase
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

        // [요청] t8410 : API전용주식챠트(일주월년)
        t8410 tr_data = new()
        {
            t8410InBlock = new("005930", "2", 100, "", "99999999", "", "N", "Y"), // 삼성전자, 일봉, 100개
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8410OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8410OutBlock 데이터 처리
        print(tr_data.t8410OutBlock);
        print(tr_data.t8410OutBlock1);
    }

    // t8410 : API전용주식챠트(일주월년)
    public record t8410InBlock(string shcode, string gubun, int qrycnt, string sdate, string edate, string cts_date, string comp_yn, string sujung);
    public record t8410OutBlock(string shcode, int jisiga, int jihigh, int jilow, int jiclose, long jivolume, int disiga, int dihigh, int dilow, int diclose, int highend, int lowend, string cts_date, string s_time, string e_time, string dshmin, int rec_count, int svi_uplmtprice, int svi_dnlmtprice);
    public record t8410OutBlock1(string date, long open, long high, long low, long close, long jdiff_vol, long value, long jongchk, double rate, long pricechk, long ratevalue, string sign);

    [Path("/stock/chart")]
    public class t8410 : TrBase
    {
        // 요청
        public t8410InBlock? t8410InBlock { get; set; }

        // 응답
        public t8410OutBlock? t8410OutBlock { get; set; }
        public t8410OutBlock1[]? t8410OutBlock1 { get; set; }
    }
}
