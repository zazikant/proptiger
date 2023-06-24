import scrapy


class APySpider(scrapy.Spider):
    name = 'a.py'
    allowed_domains = ['www.thebluebook.com/']
    start_urls = ['https://www.thebluebook.com/products/bluesearchtechnology/search-companies.html?group=Concrete&tab=1']

    def parse(self, response):
        pass
