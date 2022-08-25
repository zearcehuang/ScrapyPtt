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
