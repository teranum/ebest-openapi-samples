using eBEST.OpenApi;

namespace CSharp;

internal class _05 : SampleBase
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

        // [요청] t8410 : API전용주식챠트(일주월년)
        t8410 tr_data = new()
        {
            t8410InBlock = new("005930", "2", 100, "", "99999999", "", "N", "Y"), // 삼성전자, 일봉, 100개
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8410OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8410OutBlock 데이터 처리
        print(tr_data.t8410OutBlock);
        print(tr_data.t8410OutBlock1);
    }
}

// Output
/*
t8410OutBlock, Field Count = 19
| Key            | Value    |
|----------------|----------|
| shcode         | 005930   |
| jisiga         | 72900    |
| jihigh         | 73900    |
| jilow          | 72800    |
| jiclose        | 73200    |
| jivolume       | 11684297 |
| disiga         | 72600    |
| dihigh         | 73400    |
| dilow          | 72000    |
| diclose        | 73400    |
| highend        | 95100    |
| lowend         | 51300    |
| cts_date       | 20231004 |
| s_time         | 090000   |
| e_time         | 153000   |
| dshmin         | 10       |
| rec_count      | 100      |
| svi_uplmtprice | 79900    |
| svi_dnlmtprice | 65300    |

t8410OutBlock1[], Field Count = 12, Data Count = 100
| date     |  open |  high |   low | close | jdiff_vol |   value | jongchk | rate | pricechk | ratevalue | sign |
|----------|-------|-------|-------|-------|-----------|---------|---------|------|----------|-----------|------|
| 20231005 | 67300 | 67400 | 66700 | 66700 |  15904419 | 1064750 |       0 |    0 |        0 |         0 | 5    |
| 20231006 | 67100 | 67300 | 66000 | 66000 |  14238326 |  945986 |       0 |    0 |        0 |         0 | 5    |
| 20231010 | 66200 | 67600 | 66200 | 66400 |  19188108 | 1284566 |       0 |    0 |        0 |         0 | 2    |
| 20231011 | 68600 | 69400 | 67900 | 68200 |  21863981 | 1500354 |       0 |    0 |        0 |         0 | 2    |
| 20231012 | 68600 | 69700 | 68200 | 68900 |  19245675 | 1325738 |       0 |    0 |        0 |         0 | 2    |
| 20231013 | 68000 | 68500 | 67700 | 68000 |   9582887 |  651833 |       0 |    0 |        0 |         0 | 5    |
| 20231016 | 67900 | 68500 | 66800 | 67300 |  12591303 |  848199 |       0 |    0 |        0 |         0 | 5    |
| 20231017 | 67700 | 69900 | 67400 | 69400 |  17252771 | 1185139 |       0 |    0 |        0 |         0 | 2    |
| 20231018 | 68900 | 70500 | 68800 | 70500 |  16453843 | 1150446 |       0 |    0 |        0 |         0 | 2    |
...
*/