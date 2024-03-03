using eBEST.OpenApi;
using System.Text.Json;

namespace CSharp;

internal class _23 : SampleBase
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

        // 10분후 실시간 시세 중지
        print("10분동안 실시간 작동중...");
        await Task.Delay(600000);
        await api.RemoveRealtimeRequest("BM_", "900");

    }

    private static void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
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

    // t1602 : 시간대별투자자매매추이
    public record t1602InBlock(string market, string upcode, string gubun1, string gubun2, string cts_time, int cts_idx, int cnt, string gubun3);
    public record t1602OutBlock(string cts_time, string tjjcode_08, long ms_08, long md_08, long rate_08, long svolume_08, string jjcode_17, long ms_17, long md_17, long rate_17, long svolume_17, string jjcode_18, long ms_18, long md_18, long rate_18, long svolume_18, string jjcode_01, long ms_01, long md_01, long rate_01, long svolume_01, string jjcode_03, long ms_03, long md_03, long rate_03, long svolume_03, string jjcode_04, long ms_04, long md_04, long rate_04, long svolume_04, string jjcode_02, long ms_02, long md_02, long rate_02, long svolume_02, string jjcode_05, long ms_05, long md_05, long rate_05, long svolume_05, string jjcode_06, long ms_06, long md_06, long rate_06, long svolume_06, string jjcode_07, long ms_07, long md_07, long rate_07, long svolume_07, string jjcode_11, long ms_11, long md_11, long rate_11, long svolume_11, string jjcode_00, long ms_00, long md_00, long rate_00, long svolume_00);
    public record t1602OutBlock1(string time, long sv_08, long sv_17, long sv_18, long sv_01, long sv_03, long sv_04, long sv_02, long sv_05, long sv_06, long sv_07, long sv_11, long sv_00);

    [Path("/stock/investor")]
    public class t1602 : TrBase
    {
        // 요청
        public t1602InBlock? t1602InBlock { get; set; }

        // 응답
        public t1602OutBlock? t1602OutBlock { get; set; }
        public t1602OutBlock1[]? t1602OutBlock1 { get; set; }
    }

    // BM_ : 업종별투자자별매매현황
    public record BM_OutBlock(string tjjcode, string tjjtime, int msvolume, int mdvolume, int msvol, int p_msvol, int msvalue, int mdvalue, int msval, int p_msval, string upcode);
}
