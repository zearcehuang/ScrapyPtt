import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'ptt_movie'

    def start_requests(self):
       yield scrapy.Request("https://www.ptt.cc/bbs/movie/index.html", headers = {'User-Agent': 'Mozilla/5.0'}, callback=self.parse)

    def parse_article(self, response):
        pass
    