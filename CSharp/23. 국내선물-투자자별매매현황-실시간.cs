using System.Text.Json;

namespace CSharp;

internal class _23 : SampleBase
{
    public override async Task ActionImplement()
    {
        api.OnRealtimeEvent += Api_OnRealtimeEvent;

        // [요청] t1602 : 시간대별투자자매매추이
        t1602 tr_data = new()
        {
            t1602InBlock = new(
                "4"         // 시장구분: 0:전체, 1:코스피, 2:KP200, 3:코스닥, 4:선물, 5:콜옵션, 6:풋옵션, 7:ELW, 8:ETF
                , "900"     // 업종코드: 001:코스피, 101:KP200, 301:코스닥, 900:선물, 700:콜옵션, 800:풋옵션, 550:ELW, 560:ETF
                , "2"       // 수량구분: 1:수량, 2:금액
                , "0"       // 전일분구분: 0:금일, 1:전일
                , ""        // 연속조회시간
                , 0         // 사용안함
                , 10        // 조회건수
                , ""        // 직전대비구분(C:직전대비)
                ),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1602OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1602OutBlock 데이터 처리
        print(tr_data.t1602OutBlock);
        print(tr_data.t1602OutBlock1);

        // [실시간 시세 요청] BM_ : 업종별투자자별매매현황
        await api.AddRealtimeRequest("BM_", "900");

        print("실시간 작동중... 중지 할려면 아무키를 누르세요");
        var key = await GetReadKeyAsync();

        await api.RemoveRealtimeRequest("BM_", "900");

        api.OnRealtimeEvent -= Api_OnRealtimeEvent;
    }

    private void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
    {
        // OnRealtimeEvent 이벤트
        print($"{e.TrCode}, {e.Key}");
        if (e.TrCode.Equals("BM_"))
        {
            var outBlockData = e.RealtimeBody.Deserialize<BM_OutBlock>(_jsonOptions);
            if (outBlockData is not null)
            {
                print(outBlockData);
            }
        }
    }
}
