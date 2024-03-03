using eBEST.OpenApi;

namespace CSharp;

internal class _09 : SampleBase
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

        // [요청] t1463 : 거래대금상위
        t1463 tr_data = new()
        {
            t1463InBlock = new("0", "0", 0, 10000, 3000000, 1000000, 0, 0),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1463OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1463OutBlock 데이터 처리
        print(tr_data.t1463OutBlock);
        print(tr_data.t1463OutBlock1);
    }
}

// Output:
/*
t1463OutBlock, Field Count = 1
| Key | Value |
|-----|-------|
| idx | 20    |

t1463OutBlock1[], Field Count = 12, Data Count = 20
| hname              |  price | sign | change |  diff |   volume |   value | jnilvalue | bef_diff | shcode | filler | jnilvolume |
|--------------------|--------|------|--------|-------|----------|---------|-----------|----------|--------|--------|------------|
| 삼성전자           |  73400 | 2    |    200 |  0.27 | 20502140 | 1494456 |    866533 |   172.46 | 005930 |        |   11795859 |
| 기아               | 124500 | 2    |   6800 |  5.78 |  5862121 |  721607 |    211155 |   341.74 | 000270 |        |    1833765 |
| 현대차             | 250500 | 2    |   2500 |  1.01 |  2038396 |  507778 |    464303 |   109.36 | 005380 |        |    1911431 |
| SK하이닉스         | 156200 | 5    |   1800 | -1.14 |  3233605 |  506194 |    576353 |    87.83 | 000660 |        |    3666960 |
...
*/
