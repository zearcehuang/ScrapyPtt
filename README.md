# ScrapyPtt
# 參考網站(雖然有點錯) https://ithelp.ithome.com.tw/articles/10205050
#建立專案
scrapy startproject ptt

#建立spider
scrapy genspider PTTSpider ptt.cc

#執行
scrapy crawl PttSpider

#匯出CSV
scrapy crawl PttSpider -o ptt.csv

# 2023-01-10 11:39:43 更新

<h4>因ptt未保留舊檔, 改抓備份網站的方式</h4>

改為執行`pttbrain\test.py` 及 `pttbrain\test_goss.py`

```
python test.py
python test_goss.py
```
