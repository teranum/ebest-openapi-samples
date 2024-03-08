using eBEST.OpenApi;

namespace CSharp;

internal class _24 : SampleBase
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

        // [요청] o3101 : 해외선물마스터조회-API용
        o3101 tr_data = new()
        {
            o3101InBlock = new("0"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.o3101OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.o3101OutBlock 데이터 처리
        print(tr_data.o3101OutBlock);
    }
}

// Output:
/*
o3101OutBlock[], Field Count = 26, Data Count = 41
| Symbol  | SymbolNm                              | ApplDate | BscGdsCd | BscGdsNm                     | ExchCd | ExchNm     | CrncyCd | NotaCd | UntPrc | MnChgAmt | RgltFctr | CtrtPrAmt | GdsCd | LstngYr | LstngM |  EcPrc | DlStrtTm | DlEndTm | DlPsblCd | MgnCltCd | OpngMgn | MntncMgn | OpngMgnR | MntncMgnR | DotGb |
|---------|---------------------------------------|----------|----------|------------------------------|--------|------------|---------|--------|--------|----------|----------|-----------|-------|---------|--------|--------|----------|---------|----------|----------|---------|----------|----------|-----------|-------|
| CUSH24  | Renminbi_USD/CNH(2024.03)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | H      |  7.205 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| CUSJ24  | Renminbi_USD/CNH(2024.04)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | J      | 7.1916 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| CUSK24  | Renminbi_USD/CNH(2024.05)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | K      | 7.1777 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| CUSM24  | Renminbi_USD/CNH(2024.06)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | M      | 7.1578 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| CUSU24  | Renminbi_USD/CNH(2024.09)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | U      | 7.1139 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| CUSZ24  | Renminbi_USD/CNH(2024.12)             | 20240308 | CUS      | Renminbi_USD/CNH             | HKEX   | 홍콩거래소 | CNY     | 10     | 0.0001 |       10 |        1 |    100000 | 002   | 2024    | Z      | 7.0705 | 201500   | 193000  | 1        | 1        |   14337 |    14337 |        0 |         0 |     4 |
| HCEIH24 | H-Share(2024.03)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | H      |   5622 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCEIJ24 | H-Share(2024.04)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | J      |   5642 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCEIK24 | H-Share(2024.05)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | K      |   5653 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCEIM24 | H-Share(2024.06)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | M      |   5625 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCEIU24 | H-Share(2024.09)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | U      |   5557 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCEIZ24 | H-Share(2024.12)                      | 20240308 | HCEI     | H-Share                      | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | Z      |   5634 | 181500   | 173000  | 1        | 1        |   31255 |    31255 |        0 |         0 |     0 |
| HCHHH24 | CES China 120(2024.03)                | 20240308 | HCHH     | CES China 120                | HKEX   | 홍콩거래소 | HKD     | 10     |    0.5 |       25 |        1 |        50 | 001   | 2024    | H      |   4878 | 101500   | 173000  | 1        | 1        |   16478 |    16478 |        0 |         0 |     1 |
| HCHHJ24 | CES China 120(2024.04)                | 20240308 | HCHH     | CES China 120                | HKEX   | 홍콩거래소 | HKD     | 10     |    0.5 |       25 |        1 |        50 | 001   | 2024    | J      |   4878 | 101500   | 173000  | 1        | 1        |   16478 |    16478 |        0 |         0 |     1 |
| HCHHM24 | CES China 120(2024.06)                | 20240308 | HCHH     | CES China 120                | HKEX   | 홍콩거래소 | HKD     | 10     |    0.5 |       25 |        1 |        50 | 001   | 2024    | M      |   4879 | 101500   | 173000  | 1        | 1        |   16478 |    16478 |        0 |         0 |     1 |
| HCHHU24 | CES China 120(2024.09)                | 20240308 | HCHH     | CES China 120                | HKEX   | 홍콩거래소 | HKD     | 10     |    0.5 |       25 |        1 |        50 | 001   | 2024    | U      |   4879 | 101500   | 173000  | 1        | 1        |   16478 |    16478 |        0 |         0 |     1 |
| HMCEH24 | Mini H-Shares(2024.03)                | 20240308 | HMCE     | Mini H-Shares                | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | H      |   5622 | 181500   | 173000  | 1        | 1        |    6251 |     6251 |        0 |         0 |     0 |
| HMCEJ24 | Mini H-Shares(2024.04)                | 20240308 | HMCE     | Mini H-Shares                | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | J      |   5642 | 181500   | 173000  | 1        | 1        |    6251 |     6251 |        0 |         0 |     0 |
| HMCEM24 | Mini H-Shares(2024.06)                | 20240308 | HMCE     | Mini H-Shares                | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | M      |   5625 | 181500   | 173000  | 1        | 1        |    6251 |     6251 |        0 |         0 |     0 |
| HMCEU24 | Mini H-Shares(2024.09)                | 20240308 | HMCE     | Mini H-Shares                | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | U      |   5557 | 181500   | 173000  | 1        | 1        |    6251 |     6251 |        0 |         0 |     0 |
| HMHH24  | Mini Hang Seng(2024.03)               | 20240308 | HMH      | Mini Hang Seng               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | H      |  16241 | 181500   | 173000  | 1        | 1        |   14949 |    14949 |        0 |         0 |     0 |
| HMHJ24  | Mini Hang Seng(2024.04)               | 20240308 | HMH      | Mini Hang Seng               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | J      |  16298 | 181500   | 173000  | 1        | 1        |   14949 |    14949 |        0 |         0 |     0 |
| HMHM24  | Mini Hang Seng(2024.06)               | 20240308 | HMH      | Mini Hang Seng               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | M      |  16194 | 181500   | 173000  | 1        | 1        |   14949 |    14949 |        0 |         0 |     0 |
| HMHU24  | Mini Hang Seng(2024.09)               | 20240308 | HMH      | Mini Hang Seng               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       10 |        1 |        10 | 001   | 2024    | U      |  16056 | 181500   | 173000  | 1        | 1        |   14949 |    14949 |        0 |         0 |     0 |
| HSIH24  | Hang Seng(2024.03)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | H      |  16241 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HSIJ24  | Hang Seng(2024.04)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | J      |  16298 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HSIK24  | Hang Seng(2024.05)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | K      |  16275 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HSIM24  | Hang Seng(2024.06)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | M      |  16194 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HSIU24  | Hang Seng(2024.09)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | U      |  16056 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HSIZ24  | Hang Seng(2024.12)                    | 20240308 | HSI      | Hang Seng                    | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | Z      |  16205 | 181500   | 173000  | 1        | 1        |   74746 |    74746 |        0 |         0 |     0 |
| HTIH24  | Hang Seng TECH(2024.03)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | H      |   3359 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| HTIJ24  | Hang Seng TECH(2024.04)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | J      |   3366 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| HTIK24  | Hang Seng TECH(2024.05)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | K      |   3380 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| HTIM24  | Hang Seng TECH(2024.06)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | M      |   3389 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| HTIU24  | Hang Seng TECH(2024.09)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | U      |   3422 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| HTIZ24  | Hang Seng TECH(2024.12)               | 20240308 | HTI      | Hang Seng TECH               | HKEX   | 홍콩거래소 | HKD     | 10     |      1 |       50 |        1 |        50 | 001   | 2024    | Z      |   3464 | 181500   | 173000  | 1        | 1        |   17981 |    17981 |        0 |         0 |     0 |
| MCAH24  | MSCI China A50 Connect Index(2024.03) | 20240308 | MCA      | MSCI China A50 Connect Index | HKEX   | 홍콩거래소 | USD     | 10     |    0.2 |        5 |        1 |        25 | 001   | 2024    | H      | 1873.4 | 181500   | 173000  | 1        | 1        |    3404 |     3404 |        0 |         0 |     2 |
| MCAJ24  | MSCI China A50 Connect Index(2024.04) | 20240308 | MCA      | MSCI China A50 Connect Index | HKEX   | 홍콩거래소 | USD     | 10     |    0.2 |        5 |        1 |        25 | 001   | 2024    | J      |   1872 | 181500   | 173000  | 1        | 1        |    3404 |     3404 |        0 |         0 |     2 |
| MCAM24  | MSCI China A50 Connect Index(2024.06) | 20240308 | MCA      | MSCI China A50 Connect Index | HKEX   | 홍콩거래소 | USD     | 10     |    0.2 |        5 |        1 |        25 | 001   | 2024    | M      | 1863.2 | 181500   | 173000  | 1        | 1        |    3404 |     3404 |        0 |         0 |     2 |
| MCAU24  | MSCI China A50 Connect Index(2024.09) | 20240308 | MCA      | MSCI China A50 Connect Index | HKEX   | 홍콩거래소 | USD     | 10     |    0.2 |        5 |        1 |        25 | 001   | 2024    | U      | 1843.2 | 181500   | 173000  | 1        | 1        |    3404 |     3404 |        0 |         0 |     2 |
| MCAZ24  | MSCI China A50 Connect Index(2024.12) | 20240308 | MCA      | MSCI China A50 Connect Index | HKEX   | 홍콩거래소 | USD     | 10     |    0.2 |        5 |        1 |        25 | 001   | 2024    | Z      | 1847.8 | 181500   | 173000  | 1        | 1        |    3404 |     3404 |        0 |         0 |     2 |
*/
