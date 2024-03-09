namespace CSharp;

internal class _25 : SampleBase
{
    public override async Task ActionImplement()
    {
        var shcode = await GetInputAsync("해외선물 종목코드를 입력하세요 (ex HSIH24):");
        // [요청] o3105 : 해외선물현재가(종목정보)조회-API용
        o3105 tr_data = new()
        {
            o3105InBlock = new(shcode),
        };
        await api.GetTRData(tr_data);
        if (tr_data.o3105OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.o3105OutBlock 데이터 처리
        print(tr_data.o3105OutBlock);
    }
}

// Output:
/*
해외선물 종목코드를 입력하세요 (ex HSIH24):HSIH24
o3105OutBlock, Field Count = 58
| Key        | Value              |
|------------|--------------------|
| Symbol     | HSIH24             |
| SymbolNm   | Hang Seng(2024.03) |
| ApplDate   | 20240308           |
| BscGdsCd   | HSI                |
| BscGdsNm   | Hang Seng          |
| ExchCd     | HKEX               |
| ExchNm     | 홍콩거래소         |
| EcCd       | 1                  |
| CrncyCd    | HKD                |
| NotaCd     | 10                 |
| UntPrc     | 1                  |
| MnChgAmt   | 50                 |
| RgltFctr   | 1                  |
| CtrtPrAmt  | 50                 |
| LstngMCnt  | 12                 |
| GdsCd      | 001                |
| MrktCd     | 001                |
| EminiCd    | 0                  |
| LstngYr    | 2024               |
| LstngM     | H                  |
| SeqNo      | 1                  |
| LstngDt    | 20230925           |
| MtrtDt     | 20240327           |
| FnlDlDt    | 20240327           |
| FstTrsfrDt |                    |
| EcPrc      | 16241              |
| DlDt       | 20240308           |
| DlStrtTm   | 181500             |
| DlEndTm    | 173000             |
| OvsStrDay  | 20240308           |
| OvsStrTm   | 171500             |
| OvsEndDay  | 20240311           |
| OvsEndTm   | 163000             |
| DlPsblCd   | 1                  |
| MgnCltCd   | 1                  |
| OpngMgn    | 74746              |
| MntncMgn   | 74746              |
| OpngMgnR   | 0                  |
| MntncMgnR  | 0                  |
| DotGb      | 0                  |
| TimeDiff   | -1                 |
| OvsDate    | 20240308           |
| KorDate    | 20240308           |
| TrdTm      | 171916             |
| RcvTm      | 181916             |
| TrdP       | 16350              |
| TrdQ       | 1                  |
| TotQ       | 229                |
| TrdAmt     | 16350              |
| TotAmt     | 0                  |
| OpenP      | 16345              |
| HighP      | 16356              |
| LowP       | 16343              |
| CloseP     | 16345              |
| YdiffP     | 5                  |
| YdiffSign  | 2                  |
| Cgubun     |                    |
| Diff       | 0.03               |

해외선물 종목코드를 입력하세요 (ex HSIH24):
*/
