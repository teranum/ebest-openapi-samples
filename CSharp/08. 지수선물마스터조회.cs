using eBEST.OpenApi;

namespace CSharp;

internal class _08 : SampleBase
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

        // [요청] t8432 : 지수선물마스터조회API용
        t8432 tr_data = new()
        {
            t8432InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8432OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8432OutBlock 데이터 처리
        print(tr_data.t8432OutBlock);
    }
}

// Output:
/*
t8432OutBlock[], Field Count = 9, Data Count = 13
| hname        | shcode   | expcode      | uplmtprice | dnlmtprice | jnilclose | jnilhigh | jnillow | recprice |
|--------------|----------|--------------|------------|------------|-----------|----------|---------|----------|
| F 2403       | 101V3000 | KR4101V30005 |     385.75 |     328.65 |     357.2 |    358.1 |   352.7 |    357.2 |
| F 2406       | 101V6000 | KR4101V60002 |      386.5 |      329.3 |     357.9 |   359.15 |  353.75 |    357.9 |
| F 2409       | 101V9000 | KR4101V90009 |      388.9 |      331.3 |     360.1 |    360.1 |   360.1 |    360.1 |
| F 2412       | 101VC000 | KR4101VC0004 |      390.7 |      332.9 |     361.8 |    361.8 |  358.75 |    361.8 |
| F 2506       | 101W6000 | KR4101W60000 |     394.65 |     336.25 |    365.45 |        0 |       0 |   365.45 |
| F 2512       | 101WC000 | KR4101WC0003 |     399.35 |     340.25 |     369.8 |        0 |       0 |    369.8 |
| F 2612       | A016C000 | KR4A016C0004 |     405.15 |     345.15 |    375.15 |        0 |       0 |   375.15 |
| F SP 03-2406 | 401V3V6S | KR4401V3V6S0 |      18.55 |     -17.15 |       1.1 |     1.15 |    0.95 |        0 |
| F SP 03-2409 | 401V3V9S | KR4401V3V9S4 |      20.75 |     -14.95 |         0 |        0 |       0 |        0 |
| F SP 03-2412 | 401V3VCS | KR4401V3VCS0 |      22.45 |     -13.25 |         0 |        0 |       0 |        0 |
| F SP 03-2506 | 401V3W6S | KR4401V3W6S9 |       26.1 |       -9.6 |         0 |        0 |       0 |        0 |
| F SP 03-2512 | 401V3WCS | KR4401V3WCS8 |      30.45 |      -5.25 |         0 |        0 |       0 |        0 |
| F SP 03-2612 | 401V36CS | KR4401V36CS2 |       35.8 |        0.1 |         0 |        0 |       0 |        0 |
*/
