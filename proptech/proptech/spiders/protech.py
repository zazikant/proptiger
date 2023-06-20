import scrapy


class ProtechSpider(scrapy.Spider):
    name = "protech"
    allowed_domains = ["fddf"]
    start_urls = ["https://fddf"]

    def parse(self, response):
        pass
