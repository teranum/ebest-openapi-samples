namespace CSharp;

internal class _10 : SampleBase
{
    public override async Task ActionImplement()
    {
        // [요청] t1866 : 서버저장조건리스트조회(API)
        t1866 tr_data = new()
        {
            t1866InBlock = new(Secret.UserId, "0", "", "0", ""),
        };
        await api.GetTRData(tr_data);
        if (tr_data.t1866OutBlock is null)
        {
            // 오류 처리
            print(tr_data.rsp_cd.Length > 0 ? $"{tr_data.rsp_cd}-{tr_data.rsp_msg}" : api.LastErrorMessage);
            return;
        }

        // tr_data.t1866OutBlock 데이터 처리
        print(tr_data.t1866OutBlock);
        print(tr_data.t1866OutBlock1);
    }
}

// Output:
/*
t1866OutBlock, Field Count = 3
| Key          | Value |
|--------------|-------|
| result_count | 1     |
| cont         |       |
| contkey      |       |

t1866OutBlock1[], Field Count = 3, Data Count = 1
| query_index  | group_name | query_name |
|--------------|------------|------------|
| XXXXXXXX0001 | 나의전략   | 조건전략   |
 
* */
