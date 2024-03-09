namespace CSharp;

internal class _02 : SampleBase
{
    public override async Task ActionImplement()
    {
        // [요청] t8424 : 전체업종
        t8424 tr_data = new()
        {
            t8424InBlock = new("1"),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t8424OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t8424OutBlock 데이터 처리
        print(tr_data.t8424OutBlock);
    }
}

// Output:
/*
t8424OutBlock[], Field Count = 2, Data Count = 57
| hname                | upcode |
|----------------------|--------|
| 종       합          | 001    |
| 대   형  주          | 002    |
| 중   형  주          | 003    |
| 소   형  주          | 004    |
| 음 식 료 업          | 005    |
| 섬 유 의 복          | 006    |
| 종 이 목 재          | 007    |
| 화       학          | 008    |
...
*/
