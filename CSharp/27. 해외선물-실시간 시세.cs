using System.Text.Json;

namespace CSharp;

internal class _27 : SampleBase
{
    public override async Task ActionImplement()
    {
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

        print("실시간 작동중... 중지 할려면 아무키를 누르세요");
        var key = await GetReadKeyAsync();

        await api.RemoveRealtimeRequest("OVC", symbol_8);

        api.OnRealtimeEvent -= Api_OnRealtimeEvent;
    }

    private void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
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