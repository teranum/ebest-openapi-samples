using eBEST.OpenApi;

namespace CSharp;

internal class _26 : SampleBase
{
    public override async Task ActionImplement()
    {
        var shcode = await GetInputAsync("해외선물 종목코드를 입력하세요:");
        var str_ncnt = await GetInputAsync("N분주기를 입력하세요(1, 3, 5, 10, 15, 30, 45, 60, ...):");
        int.TryParse(str_ncnt, out int ncnt);
        var str_readcnt = await GetInputAsync("요청건수를 입력하세요(100, 500, 1000, ...):");
        int.TryParse(str_readcnt, out int readcnt);

        // 해외선물 분 차트 데이터 조회용 함수 호출
        var (ErrMsg, Datas) = await GetWorldFutureMinuteChartData(api, shcode, ncnt, readcnt
            , progress_action: (frameCount, receivedCount) =>
            {
                print($"차트조회중... {frameCount}개 프레임, {receivedCount}개 수신완료");
            });
        if (ErrMsg.Length > 0)
        {
            print($"차트조회 오류: {ErrMsg}");
        }
        print(Datas);
    }

    /// <summary>
    /// 해외선물 분차트 조회함수
    /// </summary>
    /// <param name="api">api</param>
    /// <param name="shcode">해외선물 종목코드</param>
    /// <param name="ncnt">분 주기</param>
    /// <param name="ReqCount">데이터 요청개수</param>
    /// <param name="DelayTime">요청간 딜레이 시간(ms), 기본값:1000ms</param>
    /// <param name="progress_action">프레임 수신시 콜백함수 (Param인자: 수신된 프레임수, 수신된 데이터 길이 합)</param>
    /// <returns></returns>
    public static async Task<(string ErrMsg, o3123OutBlock1[] Datas)> GetWorldFutureMinuteChartData(EBestOpenApi api, string shcode, int ncnt, int ReqCount = 500, int DelayTime = 1000
        , Action<int, int>? progress_action = null)
    {
        string cts_date = string.Empty;
        string cts_time = string.Empty;
        string tr_cont = "N";
        string tr_cont_key = string.Empty;
        int ReceivedCount = 0;

        string errMsg = string.Empty;
        List<o3123OutBlock1[]> DataFrames = [];
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

            // [요청] o3123 : 해외선물옵션차트(분)-API용
            o3123 tr_data = new()
            {
                o3123InBlock = new("F", shcode, ncnt, _inner_req_count, cts_date, cts_time),
            };
            await api.GetTRData(tr_data);
            if (tr_data.o3123OutBlock is null)
            {
                // 오류 처리
                errMsg = tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage;
                break;
            }

            // tr_data.o3123OutBlock 데이터 처리
            if (tr_data.o3123OutBlock1 == null)
            {
                break;
            }

            DataFrames.Insert(0, tr_data.o3123OutBlock1); // 연속조회된 과거 데이터를 앞에 추가
            ReceivedCount += tr_data.o3123OutBlock1.Length;
            if (progress_action != null) progress_action(DataFrames.Count, ReceivedCount);

            cts_date = tr_data.o3123OutBlock.cts_date;
            cts_time = tr_data.o3123OutBlock.cts_time;
            tr_cont = tr_data.tr_cont;
            tr_cont_key = tr_data.tr_cont_key;
            if (!tr_cont.Equals("Y")) break;
            if (ReceivedCount >= ReqCount) break;
            await Task.Delay(DelayTime);
        }

        return (errMsg, DataFrames.SelectMany(x => x).ToArray());
    }
}

// Output:
/*
해외선물 종목코드를 입력하세요:HSIH24
N분주기를 입력하세요(1, 3, 5, 10, 15, 30, 45, 60, ...):5
요청건수를 입력하세요(100, 500, 1000, ...):1000
차트조회중... 1개 프레임, 500개 수신완료
차트조회중... 2개 프레임, 1000개 수신완료
o3123OutBlock1[], Field Count = 7, Data Count = 1000
| date     | time   |  open |  high |   low | close | volume |
|----------|--------|-------|-------|-------|-------|--------|
| 20240308 | 175500 | 16372 | 16372 | 16357 | 16360 |     65 |
| 20240308 | 175000 | 16361 | 16373 | 16356 | 16373 |    107 |
| 20240308 | 174500 | 16386 | 16392 | 16347 | 16353 |    650 |
| 20240308 | 174000 | 16369 | 16471 | 16362 | 16384 |   1789 |
...
| 20240306 | 011500 | 16141 | 16151 | 16140 | 16150 |     82 |
| 20240306 | 011000 | 16148 | 16148 | 16129 | 16140 |    170 |
| 20240306 | 010500 | 16143 | 16150 | 16143 | 16148 |     81 |
| 20240306 | 010000 | 16133 | 16144 | 16133 | 16143 |     43 |
| 20240306 | 005500 | 16140 | 16141 | 16131 | 16134 |     99 |
| 20240306 | 005000 | 16140 | 16144 | 16135 | 16141 |    135 |
*/
