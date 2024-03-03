using eBEST.OpenApi;

namespace CSharp;

internal class _04 : SampleBase
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

        // [요청] t1102 : 주식현재가(시세)조회
        t1102 tr_data = new()
        {
            t1102InBlock = new("005930"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1102OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1102OutBlock 데이터 처리
        print(tr_data.t1102OutBlock);
    }
}

// Output:
/*
t1102OutBlock, Field Count = 160
| Key                | Value      |
|--------------------|------------|
| hname              | 삼성전자   |
| price              | 73400      |
| sign               | 2          |
| change             | 200        |
| diff               | 0.27       |
| volume             | 20502140   |
| recprice           | 73200      |
| avg                | 72892      |
| uplmtprice         | 95100      |
| dnlmtprice         | 51300      |
| jnilvolume         | 11795859   |
| volumediff         | 8706281    |
| open               | 72600      |
| opentime           | 090002     |
| high               | 73400      |
| hightime           | 153024     |
| low                | 72000      |
...
*/
