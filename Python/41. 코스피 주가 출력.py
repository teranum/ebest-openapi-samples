import asyncio
import ebest
from common import *
import matplotlib.pyplot as plot
from app_keys import appkey, appsecretkey

'''
코스피 종합지수 일봉 데이터를 불러올수 있을 때까지 불러온 후 차트(종가라인)로 출력
'''
async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    print("전체 코스피 일봉데이터를 불러온 후 차트(종가라인)로 출력합니다.")

    cts_date = ""
    tr_cont = "N"
    tr_cont_key = "0"
    req_count = 0
    all_data = []
    cont_is_Y = True
    while cont_is_Y:
        req_count += 1
        print(f"요청횟수: {req_count}")
        # [요청] t8419 : 업종챠트(일주월)
        request = {
            "t8419InBlock": {
                "shcode": "001",
                "gubun": "2",
                "qrycnt": 500,
                "sdate": "",
                "edate": "99999999",
                "cts_date": cts_date,
                "comp_yn": "N",
            },
        }
        response = await api.request("t8419", request, tr_cont = tr_cont, tr_cont_key = tr_cont_key)
        tr_cont = response.tr_cont;
        tr_cont_key = response.tr_cont_key;
        cts_date = response.body["t8419OutBlock"]["cts_date"];
        if not response:
           print(f"요청실패: {api.last_message}")
           break
        all_data = response.body["t8419OutBlock1"] + all_data
        await asyncio.sleep(1)
        cont_is_Y =  tr_cont == "Y"
        pass

    print_table(all_data)
    close = [float(x['close']) for x in all_data]
    plot.plot(close)
    plot.show()
    
    await api.close()



asyncio.run(main())


# Output:
"""
전체 코스피 일봉데이터를 불러온 후 차트(종가라인)로 출력합니다.
요청횟수: 1
요청횟수: 2
요청횟수: 3
요청횟수: 4
요청횟수: 5
요청횟수: 6
요청횟수: 7
요청횟수: 8
요청횟수: 9
요청횟수: 10
요청횟수: 11
요청횟수: 12
요청횟수: 13
요청횟수: 14
요청횟수: 15
요청횟수: 16
요청횟수: 17
요청횟수: 18
요청횟수: 19
요청횟수: 20
Row Count = 9122
+----------+---------+---------+---------+---------+-----------+----------+
|   date   |   open  |   high  |   low   |  close  | jdiff_vol |  value   |
+----------+---------+---------+---------+---------+-----------+----------+
| 19890126 |  858.47 |  861.52 |  858.47 |  861.46 |    7834   |  186388  |
| 19890127 |  861.66 |  873.92 |  861.66 |  873.92 |    9906   |  233314  |
| 19890128 |  873.81 |  873.81 |  869.47 |  869.74 |    6112   |  142683  |
...
| 20240223 | 2681.03 | 2694.80 | 2665.21 | 2667.70 |   415376  | 10282074 |
| 20240226 | 2657.35 | 2659.60 | 2629.78 | 2647.08 |   531661  | 10950641 |
| 20240227 | 2654.76 | 2654.76 | 2619.38 | 2625.05 |   574302  | 12634502 |
| 20240228 | 2629.11 | 2657.32 | 2623.15 | 2652.29 |   421553  | 10266443 |
| 20240229 | 2643.48 | 2647.56 | 2628.62 | 2642.36 |   496064  | 12975398 |
+----------+---------+---------+---------+---------+-----------+----------+
차트출력
"""
