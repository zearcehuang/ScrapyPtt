# ScrapyPtt
#建立專案
scrapy startproject ptt

#建立spider
scrapy genspider PTTSpider ptt.cc

#執行
scrapy crawl PttSpider

#匯出CSV
scrapy crawl ptt -o ptt.csv
