import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector

class ttspider(scrapy.Spider):
    name = 'prop'
    allowed_domains = ['proptiger.com']
        
    def start_requests(self):
        for i in range(1,500):
            link = f"https://proptiger.com/bangalore/all-builders?page={i}"
            yield scrapy.Request(url = link, callback=self.hrefs)
   
    def hrefs(self, response):
        for href in response.xpath('(//div[@class="builder-details-wrap"]/a[@class="no-ajaxy builder-name put-ellipsis js-b-card"])/@href').getall():
            A = f'https://proptiger.com{href}'

            yield scrapy.Request(A, callback=self.lelo)
    
    def lelo(self, response):

        for q in response.css('html'):

            yield{
                #'Dev_name': q.css('.blacklayer ~.heading::text').get(),
                'Total Projects': q.css('.three-points :nth-child(2) span::text').get(),
                'Ongoing Projects': q.css('.three-points :nth-child(3) span::text').get(),
                'breadcrumb': q.css('.js-breadcrumb-seo >div:first-child> span:last-child a span::text').get(),
                #'projects': q.css('.project-card-main-wrapper >div:nth-child(3)>div>div>a>span::text').getall(),
                #'location': q.css('.project-card-main-wrapper >div:nth-child(3)>div>div:nth-child(2)>div>span::text').getall(),
                #'City': q.css('.proj-address .loc + span').getall()
            }