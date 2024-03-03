using eBEST.OpenApi;

namespace CSharp;

internal class _10 : SampleBase
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
    }
}
