using eBEST.OpenApi;
using System.Text.Json;

namespace CSharp;

internal class _27 : SampleBase
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

        // 해외선물 종목코드 입력
        var symbol = await GetInputAsync("해외선물 종목코드를 입력하세요 (ex HSIH24):");

        string symbol_8 = (symbol + "        ")[..8]; // 8자리로 맞추기

        // [실시간 시세 요청] OVC : 해외선물 현재가체결
        if (!await api.AddRealtimeRequest("OVC", symbol_8))
        {
            print($"실시간 시세 요청 실패: {api.LastErrorMessage}");
            return;
        }

        // 10분후 리턴
        print("10분동안 실시간 작동중...");
        await Task.Delay(600000);
        await api.RemoveRealtimeRequest("OVC", symbol_8);

    }

    private static void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
    {
        // OnRealtimeEvent 이벤트
        print($"{e.TrCode}, {e.Key}");
        if (e.TrCode.Equals("OVC"))
        {
            var outBlockData = e.RealtimeBody.Deserialize<OVCOutBlock>(_jsonOptions);
            if (outBlockData is not null)
            {
                print(outBlockData);
            }
        }
    }
}

// Output:
/*
해외선물 종목코드를 입력하세요 (ex HSIH24):HSIH24
10분동안 실시간 작동중...
OVC, HSIH24
OVCOutBlock, Field Count = 18
| Key       | Value    |
|-----------|----------|
| symbol    | HSIH24   |
| ovsdate   | 20240308 |
| kordate   | 20240308 |
| trdtm     | 181153   |
| kortm     | 191153   |
| curpr     | 16360    |
| ydiffpr   | 15       |
| ydiffSign | 2        |
| open      | 16345    |
| high      | 16471    |
| low       | 16339    |
| chgrate   | 0.09     |
| trdq      | 1        |
| totq      | 3565     |
| cgubun    | -        |
| mdvolume  |          |
| msvolume  |          |
| ovsmkend  | 20240311 |

OVC, HSIH24
OVCOutBlock, Field Count = 18
| Key       | Value    |
|-----------|----------|
| symbol    | HSIH24   |
| ovsdate   | 20240308 |
| kordate   | 20240308 |
| trdtm     | 181153   |
| kortm     | 191153   |
| curpr     | 16360    |
| ydiffpr   | 15       |
| ydiffSign | 2        |
| open      | 16345    |
| high      | 16471    |
| low       | 16339    |
| chgrate   | 0.09     |
| trdq      | 1        |
| totq      | 3566     |
| cgubun    | -        |
| mdvolume  |          |
| msvolume  |          |
| ovsmkend  | 20240311 |
 */