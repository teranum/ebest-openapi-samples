using eBEST.OpenApi;
using System.Text.Json;

namespace CSharp;

internal class _21 : SampleBase
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

        // [실시간 시세 요청] S3_ : KOSPI체결
        if (!await api.AddRealtimeRequest("S3_", "005930")) // 삼성전자
        {
            print($"실시간 시세 요청 실패: {api.LastErrorMessage}");
            return;
        }

        // 10분후 리턴
        print("10분동안 실시간 작동중...");
        await Task.Delay(600000);
        await api.RemoveRealtimeRequest("S3_", "005930");

    }

    private static void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
    {
        // OnRealtimeEvent 이벤트
        print($"{e.TrCode}, {e.Key}");
        if (e.TrCode.Equals("S3_"))
        {
            var outBlockData = e.RealtimeBody.Deserialize<S3_OutBlock>(_jsonOptions);
            if (outBlockData is not null)
            {
                print(outBlockData);
            }
        }
    }

    // S3_ : KOSPI체결
    public record S3_OutBlock(string chetime, string sign, int change, double drate, int price, string opentime, int open, string hightime, int high, string lowtime, int low, string cgubun, int cvolume, long volume, long value, long mdvolume, int mdchecnt, long msvolume, int mschecnt, double cpower, int w_avrg, int offerho, int bidho, string status, long jnilvolume, string shcode);
}
