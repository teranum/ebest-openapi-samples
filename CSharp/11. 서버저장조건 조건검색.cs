using eBEST.OpenApi;

namespace CSharp;

internal class _11 : SampleBase
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

        // tr_data.t1859OutBlock 데이터 처리
        print(tr_data_cond.t1859OutBlock);
        print(tr_data_cond.t1859OutBlock1);
    }
}
