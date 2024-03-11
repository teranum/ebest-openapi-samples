using System.Text.Json;

namespace CSharp;

internal class _21 : SampleBase
{
    public override async Task ActionImplement()
    {
        api.OnRealtimeEvent += Api_OnRealtimeEvent;

        // [실시간 시세 요청] S3_ : KOSPI체결
        if (!await api.AddRealtimeRequest("S3_", "005930")) // 삼성전자
        {
            print($"실시간 시세 요청 실패: {api.LastErrorMessage}");
            return;
        }

        print("실시간 작동중... 중지 할려면 아무키를 누르세요");
        var key = await GetReadKeyAsync();

        await api.RemoveRealtimeRequest("S3_", "005930");

        api.OnRealtimeEvent -= Api_OnRealtimeEvent;
    }

    private void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
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
}
