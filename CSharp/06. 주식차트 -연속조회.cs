namespace CSharp;

internal class _06 : SampleBase
{
    public override async Task ActionImplement()
    {
        // 주식차트조회 확장함수 호출 (삼성전자, 일봉, 1500개)
        var (ErrMsg, Datas) = await GetStockChartDataAsync("005930", "2", 1500
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

    public async Task<(string ErrMsg, t8410OutBlock1[] Datas)> GetStockChartDataAsync(string shcode, string gubun, int ReqCount = 500, int DelayTime = 1000
        , Action<int, int>? progress_action = null)
    {
        string cts_date = string.Empty;
        string tr_cont = "N";
        string tr_cont_key = string.Empty;
        int ReceivedCount = 0;

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
                t8410InBlock = new(shcode, gubun, _inner_req_count, "", "99999999", cts_date, "N", "Y"),
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
}

// Output:
/*
차트조회중... 1개 프레임, 500개 수신완료
차트조회중... 2개 프레임, 1000개 수신완료
차트조회중... 3개 프레임, 1500개 수신완료
t8410OutBlock1[], Field Count = 12, Data Count = 1500
| date     |  open |  high |   low | close | jdiff_vol |   value | jongchk | rate | pricechk | ratevalue | sign |
|----------|-------|-------|-------|-------|-----------|---------|---------|------|----------|-----------|------|
| 20180126 | 50500 | 50780 | 49840 | 50780 |  10350100 |  522485 |       0 |    0 |        0 |         0 | 2    |
| 20180129 | 51200 | 51480 | 50900 | 51220 |  11838800 |  606586 |       0 |    0 |        0 |         0 | 2    |
| 20180130 | 50440 | 50640 | 49780 | 49800 |  12284550 |  616154 |       0 |    0 |        0 |         0 | 5    |
| 20180131 | 50020 | 54140 | 49600 | 49900 |  64681300 | 3351453 |       0 |    0 |        0 |         0 | 2    |
| 20180201 | 50620 | 50960 | 49720 | 49820 |  27609450 | 1385573 |       0 |    0 |        0 |         0 | 5    |
| 20180202 | 49380 | 49400 | 47700 | 47700 |  29260350 | 1408721 |       0 |    0 |        0 |         0 | 5    |
| 20180205 | 46500 | 48320 | 46000 | 47920 |  28357900 | 1333663 |       0 |    0 |        0 |         0 | 2    |
| 20180206 | 46600 | 47920 | 46580 | 47420 |  19406450 |  913940 |       0 |    0 |        0 |         0 | 5    |
| 20180207 | 48240 | 48260 | 45800 | 45800 |  23448050 | 1097891 |       0 |    0 |        0 |         0 | 5    |
| 20180208 | 46120 | 46620 | 45980 | 46000 |  23251050 | 1075498 |       0 |    0 |        0 |         0 | 2    |
| 20180209 | 44440 | 45180 | 44420 | 44700 |  17465000 |  780791 |       0 |    0 |        0 |         0 | 5    |
| 20180212 | 45100 | 46320 | 45040 | 45720 |  15754950 |  719931 |       0 |    0 |        0 |         0 | 2    |
...
| 20240222 | 73800 | 73900 | 72700 | 73100 |  15188934 | 1110412 |       0 |    0 |        0 |         0 | 2    |
| 20240223 | 73600 | 74200 | 72900 | 72900 |  16060746 | 1177781 |       0 |    0 |        0 |         0 | 5    |
| 20240226 | 72300 | 73200 | 72200 | 72800 |  14549894 | 1059031 |       0 |    0 |        0 |         0 | 5    |
| 20240227 | 73100 | 73400 | 72700 | 72900 |  13050455 |  952221 |       0 |    0 |        0 |         0 | 2    |
| 20240228 | 72900 | 73900 | 72800 | 73200 |  11684297 |  858249 |       0 |    0 |        0 |         0 | 2    |
| 20240229 | 72600 | 73400 | 72000 | 73400 |  20502140 | 1494456 |       0 |    0 |        0 |         0 | 2    |
*/
