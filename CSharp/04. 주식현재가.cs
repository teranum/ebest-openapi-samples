using eBEST.OpenApi;

namespace CSharp;

internal class _04 : SampleBase
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

        // [요청] t1102 : 주식현재가(시세)조회
        t1102 tr_data = new()
        {
            t1102InBlock = new("005930"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1102OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1102OutBlock 데이터 처리
        print(tr_data.t1102OutBlock);
    }

    // t1102 : 주식현재가(시세)조회
    public record t1102InBlock(string shcode);
    public record t1102OutBlock(string hname, int price, string sign, int change, double diff, long volume, int recprice, int avg, int uplmtprice, int dnlmtprice, long jnilvolume, long volumediff, int open, string opentime, int high, string hightime, int low, string lowtime, int high52w, string high52wdate, int low52w, string low52wdate, double exhratio, double per, double pbrx, long listing, int jkrate, string memedan, string offernocd1, string bidnocd1, string offerno1, string bidno1, int dvol1, int svol1, int dcha1, int scha1, double ddiff1, double sdiff1, string offernocd2, string bidnocd2, string offerno2, string bidno2, int dvol2, int svol2, int dcha2, int scha2, double ddiff2, double sdiff2, string offernocd3, string bidnocd3, string offerno3, string bidno3, int dvol3, int svol3, int dcha3, int scha3, double ddiff3, double sdiff3, string offernocd4, string bidnocd4, string offerno4, string bidno4, int dvol4, int svol4, int dcha4, int scha4, double ddiff4, double sdiff4, string offernocd5, string bidnocd5, string offerno5, string bidno5, int dvol5, int svol5, int dcha5, int scha5, double ddiff5, double sdiff5, long fwdvl, long ftradmdcha, double ftradmddiff, long fwsvl, long ftradmscha, double ftradmsdiff, double vol, string shcode, long value, long jvolume, int highyear, string highyeardate, int lowyear, string lowyeardate, int target, long capital, long abscnt, int parprice, string gsmm, int subprice, long total, string listdate, string name, long bfsales, long bfoperatingincome, long bfordinaryincome, long bfnetincome, double bfeps, string name2, long bfsales2, long bfoperatingincome2, long bfordinaryincome2, long bfnetincome2, double bfeps2, double salert, double opert, double ordrt, double netrt, double epsrt, string info1, string info2, string info3, string info4, string janginfo, double t_per, string tonghwa, long dval1, long sval1, long dval2, long sval2, long dval3, long sval3, long dval4, long sval4, long dval5, long sval5, int davg1, int savg1, int davg2, int savg2, int davg3, int savg3, int davg4, int savg4, int davg5, int savg5, long ftradmdval, long ftradmsval, int ftradmdvag, int ftradmsvag, string info5, string spac_gubun, int issueprice, string alloc_gubun, string alloc_text, string shterm_text, int svi_uplmtprice, int svi_dnlmtprice, string low_lqdt_gu, string abnormal_rise_gu, string lend_text, string ty_text);

    [Path("/stock/market-data")]
    public class t1102 : TrBase
    {
        // 요청
        public t1102InBlock? t1102InBlock { get; set; }

        // 응답
        public t1102OutBlock? t1102OutBlock { get; set; }
    }
}
