using System.Text.Json;

namespace CSharp;

internal class _12 : SampleBase
{
    public override async Task ActionImplement()
    {
        // [요청] t1866 : 서버저장조건리스트조회(API)
        t1866 tr_data = new()
        {
            t1866InBlock = new(Secret.UserId, "0", "", "0", ""),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1866OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1866OutBlock 데이터 처리
        print(tr_data.t1866OutBlock);
        print(tr_data.t1866OutBlock1);

        if (tr_data.t1866OutBlock1 == null)
        {
            print("서버에 저장된 조건검색식이 없습니다.");
            return;
        }

        // 요청할 조건검색식 선택
        int sel_index;
        do
        {
            Console.Write($"조건검색식index (0~{tr_data.t1866OutBlock.result_count - 1})를 입력하세요:");
            int.TryParse(Console.ReadLine(), out sel_index);
            if (sel_index < 0 || sel_index >= tr_data.t1866OutBlock.result_count)
            {
                print("잘못된 입력입니다.");
                sel_index = -1;
            }
        } while (sel_index == -1);

        // [요청] t1859 : 서버저장조건 조건검색
        var query_index = tr_data.t1866OutBlock1[sel_index].query_index;
        t1859 tr_data_cond = new()
        {
            t1859InBlock = new(tr_data.t1866OutBlock1[sel_index].query_index),
        };
        await api.GetTRData(tr_data_cond);
        if (tr_data_cond.t1859OutBlock is null)
        {
            // 오류 처리
            print(tr_data_cond.rsp_cd.Length > 0 ? $"{tr_data_cond.rsp_cd}-{tr_data_cond.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data_cond.t1859OutBlock 데이터 처리
        print(tr_data_cond.t1859OutBlock);
        print(tr_data_cond.t1859OutBlock1);

        // [요청] t1860 : 서버저장조건 실시간검색
        t1860 tr_data_real = new()
        {
            t1860InBlock = new("U", "E", "", query_index),
        };
        await api.GetTRData(tr_data_real);
        if (tr_data_real.t1860OutBlock is null)
        {
            // 오류 처리
            print(tr_data_real.rsp_cd.Length > 0 ? $"{tr_data_real.rsp_cd}-{tr_data_real.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data_real.t1860OutBlock 데이터 처리
        print(tr_data_real.t1860OutBlock);

        // 실시간 시세등록
        api.OnRealtimeEvent += Api_OnRealtimeEvent;
        if (!await api.AddRealtimeRequest("AFR", tr_data_real.t1860OutBlock.sAlertNum))
        {
            print($"AFR 실시간 등록 오류:{api.LastErrorMessage}");
            return;
        }

        // 10분후 리턴
        print("10분동안 실시간 조건검색 작동중...");
        await Task.Delay(600000);
    }

    private static void Api_OnRealtimeEvent(object? sender, eBEST.OpenApi.Events.EBestOnRealtimeEventArgs e)
    {
        if (e.TrCode.Equals("AFR")) // API사용자조건검색실시간
        {
            var real_cond = e.RealtimeBody.Deserialize<AFROutBlock>(); // JsonSerializer.Deserialize<AFROutBlock>(e.RealtimeBody);
            print($"{e.TrCode}, {e.Key}");
            print(real_cond);
        }
    }
}
