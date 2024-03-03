using eBEST.OpenApi;

namespace CSharp;

internal class _07 : SampleBase
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

        // [요청] CSPAQ22200 : 현물계좌예수금 주문가능금액 총평가2
        CSPAQ22200 tr_data = new()
        {
            CSPAQ22200InBlock1 = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.CSPAQ22200OutBlock1 is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.CSPAQ22200OutBlock 데이터 처리
        print(tr_data.CSPAQ22200OutBlock1);
        print(tr_data.CSPAQ22200OutBlock2);
    }
}

// Output:
/*
CSPAQ22200OutBlock1, Field Count = 5
| Key       | Value       |
|-----------|-------------|
| RecCnt    | 1           |
| MgmtBrnNo |             |
| AcntNo    | XXXXXXXXXXX |
| Pwd       | ********    |
| BalCreTp  | 0           |

CSPAQ22200OutBlock2, Field Count = 37
| Key                    | Value       |
|------------------------|-------------|
| RecCnt                 | 1           |
| BrnNm                  | XXXXXXXXXXX |
| AcntNm                 | XXXXXX      |
| MnyOrdAbleAmt          | 0           |
| SubstOrdAbleAmt        | 0           |
| SeOrdAbleAmt           | 0           |
| KdqOrdAbleAmt          | 0           |
| CrdtPldgOrdAmt         | 0           |
| MgnRat100pctOrdAbleAmt | 0           |
| MgnRat35ordAbleAmt     | 0           |
| MgnRat50ordAbleAmt     | 0           |
| CrdtOrdAbleAmt         | 0           |
| Dps                    | 0           |
| SubstAmt               | 0           |
|
...
*/
