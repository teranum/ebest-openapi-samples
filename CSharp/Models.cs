using eBEST.OpenApi;

//// Models.cs
/// 개발에 필요한 이베스트증권 TR 모델들을 정의합니다.
/// 모델소스는 DevCenter에서 제공하는 모델소스를 참조합니다.


/// 이베스트에서 제공되는 모든 TR 모델을 참조할 경우 eBEST.OpenApi.Models 패키지를 설치합니다.
/// nuget indtall eBEST.OpenApi.Models
/// using eBEST.OpenApi.Models;


namespace CSharp
{
    // t8424 : 전체업종
    public record t8424InBlock(string gubun1);
    public record t8424OutBlock(string hname, string upcode);

    [Path("/indtp/market-data")]
    public class t8424 : TrBase
    {
        // 요청
        public t8424InBlock? t8424InBlock { get; set; }

        // 응답
        public t8424OutBlock[]? t8424OutBlock { get; set; }
    }

    // t8436 : 주식종목조회 API용
    public record t8436InBlock(string gubun);
    public record t8436OutBlock(string hname, string shcode, string expcode, string etfgubun, int uplmtprice, int dnlmtprice, int jnilclose, string memedan, int recprice, string gubun, string bu12gubun, string spac_gubun, string filler);

    [Path("/stock/etc")]
    public class t8436 : TrBase
    {
        // 요청
        public t8436InBlock? t8436InBlock { get; set; }

        // 응답
        public t8436OutBlock[]? t8436OutBlock { get; set; }
    }

    // t1102 : 주식현재가(시세)조회
    public record t1102InBlock(string shcode);
    public record t1102OutBlock(string hname, int price, string sign, int change, double diff, long volume, int recprice, int avg, int uplmtprice, int dnlmtprice, long jnilvolume, long volumediff, int open, string opentime, int high, string hightime, int low, string lowtime, int high52w, string high52wdate, int low52w, string low52wdate, double exhratio, double per, double pbrx, long listing, int jkrate, string memedan, string offernocd1, string bidnocd1, string offerno1, string bidno1, int dvol1, int svol1, int dcha1, int scha1, double ddiff1, double sdiff1, string offernocd2, string bidnocd2, string offerno2, string bidno2, int dvol2, int svol2, int dcha2, int scha2, double ddiff2, double sdiff2, string offernocd3, string bidnocd3, string offerno3, string bidno3, int dvol3, int svol3, int dcha3, int scha3, double ddiff3, double sdiff3, string offernocd4, string bidnocd4, string offerno4, string bidno4, int dvol4, int svol4, int dcha4, int scha4, double ddiff4, double sdiff4, string offernocd5, string bidnocd5, string offerno5, string bidno5, int dvol5, int svol5, int dcha5, int scha5, double ddiff5, double sdiff5, long fwdvl, long ftradmdcha, double ftradmddiff, long fwsvl, long ftradmscha, double ftradmsdiff, double vol, string shcode, long value, long jvolume, int highyear, string highyeardate, int lowyear, string lowyeardate, int target, long capital, long abscnt, int parprice, string gsmm, int subprice, long total, string listdate, string name, long bfsales, long bfoperatingincome, long bfordinaryincome, long bfnetincome, double bfeps, string name2, long bfsales2, long bfoperatingincome2, long bfordinaryincome2, long bfnetincome2, double bfeps2, double salert, double opert, double ordrt, double netrt, double epsrt, string info1, string info2, string info3, string info4, string janginfo, double t_per, string tonghwa, long dval1, long sval1, long dval2, long sval2, long dval3, long sval3, long dval4, long sval4, long dval5, long sval5, int davg1, int savg1, int davg2, int savg2, int davg3, int savg3, int davg4, int savg4, int davg5, int savg5, long ftradmdval, long ftradmsval, int ftradmdvag, int ftradmsvag, string info5, string spac_gubun, int issueprice, string alloc_gubun, string alloc_text, string shterm_text, int svi_uplmtprice, int svi_dnlmtprice, string low_lqdt_gu, string abnormal_rise_gu, string lend_text, string ty_text);

    [Path("/stock/market-data")]
    public class t1102 : TrBase
    {
        // 요청
        public t1102InBlock? t1102InBlock { get; set; }

        // 응답
        public t1102OutBlock? t1102OutBlock { get; set; }
    }

    // t8410 : API전용주식챠트(일주월년)
    public record t8410InBlock(string shcode, string gubun, int qrycnt, string sdate, string edate, string cts_date, string comp_yn, string sujung);
    public record t8410OutBlock(string shcode, int jisiga, int jihigh, int jilow, int jiclose, long jivolume, int disiga, int dihigh, int dilow, int diclose, int highend, int lowend, string cts_date, string s_time, string e_time, string dshmin, int rec_count, int svi_uplmtprice, int svi_dnlmtprice);
    public record t8410OutBlock1(string date, long open, long high, long low, long close, long jdiff_vol, long value, long jongchk, double rate, long pricechk, long ratevalue, string sign);

    [Path("/stock/chart")]
    public class t8410 : TrBase
    {
        // 요청
        public t8410InBlock? t8410InBlock { get; set; }

        // 응답
        public t8410OutBlock? t8410OutBlock { get; set; }
        public t8410OutBlock1[]? t8410OutBlock1 { get; set; }
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

    // t8432 : 지수선물마스터조회API용
    public record t8432InBlock(string gubun);
    public record t8432OutBlock(string hname, string shcode, string expcode, double uplmtprice, double dnlmtprice, double jnilclose, double jnilhigh, double jnillow, double recprice);

    [Path("/futureoption/market-data")]
    public class t8432 : TrBase
    {
        // 요청
        public t8432InBlock? t8432InBlock { get; set; }

        // 응답
        public t8432OutBlock[]? t8432OutBlock { get; set; }
    }

    // t1463 : 거래대금상위
    public record t1463InBlock(string gubun, string jnilgubun, long jc_num, int sprice, int eprice, long volume, int idx, long jc_num2);
    public record t1463OutBlock(int idx);
    public record t1463OutBlock1(string hname, int price, string sign, int change, double diff, long volume, long value, long jnilvalue, double bef_diff, string shcode, string filler, long jnilvolume);

    [Path("/stock/high-item")]
    public class t1463 : TrBase
    {
        // 요청
        public t1463InBlock? t1463InBlock { get; set; }

        // 응답
        public t1463OutBlock? t1463OutBlock { get; set; }
        public t1463OutBlock1[]? t1463OutBlock1 { get; set; }
    }

    // t1866 : 서버저장조건리스트조회(API)
    public record t1866InBlock(string user_id, string gb, string group_name, string cont, string contkey);
    public record t1866OutBlock(int result_count, string cont, string contkey);
    public record t1866OutBlock1(string query_index, string group_name, string query_name);

    [Path("/stock/item-search")]
    public class t1866 : TrBase
    {
        // 요청
        public t1866InBlock? t1866InBlock { get; set; }

        // 응답
        public t1866OutBlock? t1866OutBlock { get; set; }
        public t1866OutBlock1[]? t1866OutBlock1 { get; set; }
    }

    // t1859 : 서버저장조건 조건검색
    public record t1859InBlock(string query_index);
    public record t1859OutBlock(int result_count, int result_time, string text);
    public record t1859OutBlock1(string shcode, string hname, int price, string sign, long change, double diff, long volume);

    [Path("/stock/item-search")]
    public class t1859 : TrBase
    {
        // 요청
        public t1859InBlock? t1859InBlock { get; set; }

        // 응답
        public t1859OutBlock? t1859OutBlock { get; set; }
        public t1859OutBlock1[]? t1859OutBlock1 { get; set; }
    }

    // t1860 : 서버저장조건 실시간검색
    public record t1860InBlock(string sSysUserFlag, string sFlag, string sAlertNum, string query_index);
    public record t1860OutBlock(string sSysUserFlag, string sFlag, string sResultFlag, string sTime, string sAlertNum, string Msg);

    [Path("/stock/item-search")]
    public class t1860 : TrBase
    {
        // 요청
        public t1860InBlock? t1860InBlock { get; set; }

        // 응답
        public t1860OutBlock? t1860OutBlock { get; set; }
    }
    public record AFROutBlock(string gsCode, string gshname, string gsPrice, string gsSign, string gsChange, string gsChgRate, string gsVolume, string gsJobFlag);

    // S3_ : KOSPI체결
    public record S3_OutBlock(string chetime, string sign, int change, double drate, int price, string opentime, int open, string hightime, int high, string lowtime, int low, string cgubun, int cvolume, long volume, long value, long mdvolume, int mdchecnt, long msvolume, int mschecnt, double cpower, int w_avrg, int offerho, int bidho, string status, long jnilvolume, string shcode);

    // t9943 : 지수선물마스터조회API용
    public record t9943InBlock(string gubun);
    public record t9943OutBlock(string hname, string shcode, string expcode);

    [Path("/futureoption/market-data")]
    public class t9943 : TrBase
    {
        // 요청
        public t9943InBlock? t9943InBlock { get; set; }

        // 응답
        public t9943OutBlock[]? t9943OutBlock { get; set; }
    }

    // FC0 : KOSPI200선물체결(C0)
    public record FC0OutBlock(string chetime, string sign, double change, double drate, double price, double open, double high, double low, string cgubun, int cvolume, long volume, long value, long mdvolume, int mdchecnt, long msvolume, int mschecnt, double cpower, double offerho1, double bidho1, int openyak, double k200jisu, double theoryprice, double kasis, double sbasis, double ibasis, int openyakcha, string jgubun, long jnilvolume, string futcode);

    // t1602 : 시간대별투자자매매추이
    public record t1602InBlock(string market, string upcode, string gubun1, string gubun2, string cts_time, int cts_idx, int cnt, string gubun3);
    public record t1602OutBlock(string cts_time, string tjjcode_08, long ms_08, long md_08, long rate_08, long svolume_08, string jjcode_17, long ms_17, long md_17, long rate_17, long svolume_17, string jjcode_18, long ms_18, long md_18, long rate_18, long svolume_18, string jjcode_01, long ms_01, long md_01, long rate_01, long svolume_01, string jjcode_03, long ms_03, long md_03, long rate_03, long svolume_03, string jjcode_04, long ms_04, long md_04, long rate_04, long svolume_04, string jjcode_02, long ms_02, long md_02, long rate_02, long svolume_02, string jjcode_05, long ms_05, long md_05, long rate_05, long svolume_05, string jjcode_06, long ms_06, long md_06, long rate_06, long svolume_06, string jjcode_07, long ms_07, long md_07, long rate_07, long svolume_07, string jjcode_11, long ms_11, long md_11, long rate_11, long svolume_11, string jjcode_00, long ms_00, long md_00, long rate_00, long svolume_00);
    public record t1602OutBlock1(string time, long sv_08, long sv_17, long sv_18, long sv_01, long sv_03, long sv_04, long sv_02, long sv_05, long sv_06, long sv_07, long sv_11, long sv_00);

    [Path("/stock/investor")]
    public class t1602 : TrBase
    {
        // 요청
        public t1602InBlock? t1602InBlock { get; set; }

        // 응답
        public t1602OutBlock? t1602OutBlock { get; set; }
        public t1602OutBlock1[]? t1602OutBlock1 { get; set; }
    }

    // BM_ : 업종별투자자별매매현황
    public record BM_OutBlock(string tjjcode, string tjjtime, int msvolume, int mdvolume, int msvol, int p_msvol, int msvalue, int mdvalue, int msval, int p_msval, string upcode);
}
