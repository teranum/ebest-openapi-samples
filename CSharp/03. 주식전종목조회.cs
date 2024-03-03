using eBEST.OpenApi;

namespace CSharp;

internal class _03 : SampleBase
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

        // [요청] t8436 : 주식종목조회 API용
        t8436 tr_data = new()
        {
            t8436InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8436OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8436OutBlock 데이터 처리
        print(tr_data.t8436OutBlock);
    }
}

// Output:
/*
t8436OutBlock[], Field Count = 13, Data Count = 3873
| hname                | shcode | expcode      | etfgubun | uplmtprice | dnlmtprice | jnilclose | memedan | recprice | gubun | bu12gubun | spac_gubun | filler |
|----------------------|--------|--------------|----------|------------|------------|-----------|---------|----------|-------|-----------|------------|--------|
| 동화약품             | 000020 | KR7000020008 | 0        |      12740 |       6860 |      9800 | 00001   |     9800 | 1     | 01        | N          |        |
| KR모터스             | 000040 | KR7000040006 | 0        |        604 |        326 |       465 | 00001   |      465 | 1     | 01        | N          |        |
| 경방                 | 000050 | KR7000050005 | 0        |      11510 |       6210 |      8860 | 00001   |     8860 | 1     | 01        | N          |        |
| 삼양홀딩스           | 000070 | KR7000070003 | 0        |      93200 |      50200 |     71700 | 00001   |    71700 | 1     | 01        | N          |        |
| 삼양홀딩스우         | 000075 | KR7000071001 | 0        |      70800 |      38200 |     54500 | 00001   |    54500 | 1     | 01        | N          |        |
| 하이트진로           | 000080 | KR7000080002 | 0        |      26300 |      14200 |     20250 | 00001   |    20250 | 1     | 01        | N          |        |
| 하이트진로2우B       | 000087 | KR7000082008 | 0        |      20400 |      10990 |     15700 | 00001   |    15700 | 1     | 01        | N          |        |
| 유한양행             | 000100 | KR7000100008 | 0        |      89300 |      48100 |     68700 | 00001   |    68700 | 1     | 01        | N          |        |
| 유한양행우           | 000105 | KR7000101006 | 0        |      78300 |      42300 |     60300 | 00001   |    60300 | 1     | 01        | N          |        |
| CJ대한통운           | 000120 | KR7000120006 | 0        |     162200 |      87400 |    124800 | 00001   |   124800 | 1     | 01        | N          |        |
| 하이트진로홀딩스     | 000140 | KR7000140004 | 0        |      11770 |       6350 |      9060 | 00001   |     9060 | 1     | 01        | N          |        |
| 하이트진로홀딩스우   | 000145 | KR7000141002 | 0        |      16000 |       8620 |     12310 | 00001   |    12310 | 1     | 01        | N          |        |
...
*/
