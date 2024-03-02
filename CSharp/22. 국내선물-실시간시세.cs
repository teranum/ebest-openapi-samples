using eBEST.OpenApi;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace CSharp;

internal class _22 : SampleBase
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

        api.OnRealtimeEvent += Api_OnRealtimeEvent;

        // [요청] t9943 : 지수선물마스터조회API용
        t9943 tr_data = new()
        {
            t9943InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t9943OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t9943OutBlock 데이터 처리
        print(tr_data.t9943OutBlock);

        // 대표 월물 가져온다
        var main_item = tr_data.t9943OutBlock[0];
        print($"대표월물: {main_item}");
        var shcode = main_item.shcode;

        if (!await api.AddRealtimeRequest("FC0", main_item.shcode)) // 대표월물
        {
            print($"실시간 시세 요청 실패: {api.LastErrorMessage}");
            return;
        }

        // 10분후 리턴
        print("10분동안 실시간 작동중...");
        await Task.Delay(600000);

    }

    private static void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
    {
        // OnRealtimeEvent 이벤트
        print($"{e.TrCode}, {e.Key}");
        if (e.TrCode.Equals("FC0"))
        {
            var outBlockData = e.RealtimeBody.Deserialize<FC0OutBlock>(_jsonOptions);
            if (outBlockData is not null)
            {
                print(outBlockData);
            }
        }
    }

    // t9943 : 지수선물마스터조회API용
    public record t9943InBlock(string gubun);
    public record t9943OutBlock(string hname, string shcode, string expcode);

    [Path("/futureoption/market-data")]
    public class t9943 : TrBase
    {
        // 요청
        public t9943InBlock? t9943InBlock { get; set; }

        // 응답
        public t9943OutBlock[]? t9943OutBlock { get; set; }
    }

    // FC0 : KOSPI200선물체결(C0)
    public record FC0OutBlock(string chetime, string sign, double change, double drate, double price, double open, double high, double low, string cgubun, int cvolume, long volume, long value, long mdvolume, int mdchecnt, long msvolume, int mschecnt, double cpower, double offerho1, double bidho1, int openyak, double k200jisu, double theoryprice, double kasis, double sbasis, double ibasis, int openyakcha, string jgubun, long jnilvolume, string futcode);
}
