# Discussion on Aug 9th

## Implementation plan

1. Screenshot the statellite imagery from 50000 lat long lacations in 2017, 2019, 2021
2. Use a pretrained model to run segmentation/object detection on the satellite imagery
3. Train a model to compare the segmentation of 2017, 2019, 2021 at the same location to output a single scalar as the probability of finding illegal factory expansion.


## 國土利用監測整合資訊網
- https://landchg.tcd.gov.tw/Module/RWD/Web/Default.aspx

## Crowdsourcing data v.s. 農委會 50000 筆資料點位差異
- 6000 筆資料是比對2017,2020農委會的資料之間的差異，來生成點位
- 至於 2017 或是更久之前的點位，是沒有經過確認的資料
- Current result: 100~200 illegal factory expansion / 6000 data points, around 3-5% illegal factory identification
- 照道理現在這些點位，應該都會pass給地方區公所去確認，但那個確認是不是很嚴謹 這個不確定 因為也沒有相關裁罰紀錄
- 農委會釋出的疑似工廠點位都有一個「合法」的用途，這部份需要經濟部才能檢查，目前data不包含這個資料


## Satellite imagery 紅外線 and RGB data
- 可見光波段不是最適合判斷有沒有建物的範圍
- 有沒有可能拿到紅外線資料？Google earth engine 解析度太差
- 中央大學圖資是從法國衛星
- 目前使用的圖資：https://livingatlas.arcgis.com/wayback/#active=13851&ext=-115.36279,36.02694,-115.23421,36.10104
- 福衛 not available
