using eBEST.OpenApi;

namespace CSharp;

internal class _06 : SampleBase
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

        // 주식차트조회 확장함수 호출 (삼성전자, 일봉, 500개)
        var (ErrMsg, Datas) = await GetStockChartDataAsync(api, "005930", CandleGubun.일, 500
            , progress_action: (frameCount, receivedCount) =>
        {
            print($"차트조회중... {frameCount}개 프레임 중 {receivedCount}개 수신완료");
        });
        if (ErrMsg.Length > 0)
        {
            print($"차트조회 오류: {ErrMsg}");
        }
        print(Datas);
    }

    public static async Task<(string ErrMsg, t8410OutBlock1[] Datas)> GetStockChartDataAsync(EBestOpenApi api, string shcode, CandleGubun gubun, int ReqCount = 500, int DelayTime = 1000
        , Action<int, int>? progress_action = null)
    {
        if (gubun < CandleGubun.일 || gubun > CandleGubun.년)
        {
            return ("잘못된 캔들구분, 현재 샘플코드는 분/틱을 지원하지 않습니다.", []);
        }

        string cts_date = string.Empty;
        string tr_cont = "N";
        string tr_cont_key = string.Empty;
        int ReceivedCount = 0;

        string str_gubun = gubun switch
        {
            CandleGubun.분 => "0",
            CandleGubun.틱 => "1",
            CandleGubun.일 => "2",
            CandleGubun.주 => "3",
            CandleGubun.월 => "4",
            CandleGubun.년 => "5",
            _ => "2",
        };

        string errMsg = string.Empty;
        List<t8410OutBlock1[]> DataFrames = [];
        while (true)
        {
            const int MaxCountPerFrame = 500; // 한번 조회할때 최대 500개까지 조회가능
            int _inner_req_count;
            if (ReqCount <= 0) _inner_req_count = MaxCountPerFrame;
            else
            {
                _inner_req_count = ReqCount - ReceivedCount;
                if (_inner_req_count <= 0) break;
                if (_inner_req_count > MaxCountPerFrame) _inner_req_count = MaxCountPerFrame;
            }
            t8410 tr_data = new()
            {
                t8410InBlock = new(shcode, str_gubun, _inner_req_count, "", "99999999", cts_date, "N", "Y"),
                tr_cont = tr_cont,
                tr_cont_key = tr_cont_key,
            };
            await api.GetTRData(tr_data);
            if (tr_data.t8410OutBlock is null)
            {
                errMsg = tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage;
                break;
            }

            if (tr_data.t8410OutBlock1 == null)
            {
                break;
            }

            DataFrames.Insert(0, tr_data.t8410OutBlock1); // 연속조회된 과거 데이터를 앞에 추가
            ReceivedCount += tr_data.t8410OutBlock1.Length;
            if (progress_action != null) progress_action(DataFrames.Count, ReceivedCount);

            cts_date = tr_data.t8410OutBlock.cts_date;
            tr_cont = tr_data.tr_cont;
            tr_cont_key = tr_data.tr_cont_key;
            if (!tr_cont.Equals("Y")) break;
            if (ReceivedCount >= ReqCount) break;
            await Task.Delay(DelayTime);
        }

        return (errMsg, DataFrames.SelectMany(x => x).ToArray());
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
}
