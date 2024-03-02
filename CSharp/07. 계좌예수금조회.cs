﻿using eBEST.OpenApi;

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

    // CSPAQ22200 : 현물계좌예수금 주문가능금액 총평가2
    public record CSPAQ22200InBlock1(/*int RecCnt, string MgmtBrnNo, string AcntNo, string Pwd, */string BalCreTp);
    public record CSPAQ22200OutBlock1(int RecCnt, string MgmtBrnNo, string AcntNo, string Pwd, string BalCreTp);
    public record CSPAQ22200OutBlock2(int RecCnt, string BrnNm, string AcntNm, long MnyOrdAbleAmt, long SubstOrdAbleAmt, long SeOrdAbleAmt, long KdqOrdAbleAmt, long CrdtPldgOrdAmt, long MgnRat100pctOrdAbleAmt, long MgnRat35ordAbleAmt, long MgnRat50ordAbleAmt, long CrdtOrdAbleAmt, long Dps, long SubstAmt, long MgnMny, long MgnSubst, long D1Dps, long D2Dps, long RcvblAmt, long D1ovdRepayRqrdAmt, long D2ovdRepayRqrdAmt, long MloanAmt, double ChgAfPldgRat, long RqrdPldgAmt, long PdlckAmt, long OrgPldgSumAmt, long SubPldgSumAmt, long CrdtPldgAmtMny, long CrdtPldgSubstAmt, long Imreq, long CrdtPldgRuseAmt, long DpslRestrcAmt, long PrdaySellAdjstAmt, long PrdayBuyAdjstAmt, long CrdaySellAdjstAmt, long CrdayBuyAdjstAmt, long CslLoanAmtdt1);

    [Path("/stock/accno")]
    public class CSPAQ22200 : TrBase
    {
        // 요청
        public CSPAQ22200InBlock1? CSPAQ22200InBlock1 { get; set; }

        // 응답
        public CSPAQ22200OutBlock1? CSPAQ22200OutBlock1 { get; set; }
        public CSPAQ22200OutBlock2? CSPAQ22200OutBlock2 { get; set; }
    }
}
