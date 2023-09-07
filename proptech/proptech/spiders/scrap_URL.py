import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class Scrap_URLSpider(CrawlSpider):
    name = 'scrap_URL'
    allowed_domains = ['excelize.com']
    start_urls = ['https://excelize.com']

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        
        html = response.text
        
        body = response.css('.header').getall()
    
        shody = response.css('.FooterBGImage').getall()
        for text in body:
            html = html.replace(text, '')
        for text in shody:
            html = html.replace(text, '')

        # Now, `html` contains the total response text without the elements matching the given xpath expressions
        
        email_found = False
        
        # emails = re.findall(r'(?:project|Project)\s?(?:Management|management)', html)
        emails = re.findall(r'[Bb]im', html)
        for email in emails:
            if not email_found:
                yield {
                    'URL': response.url,
                    # 'content': response.xpath('normalize-space(//body)').get(),
                    'Email': email
                }
                email_found = True
            else:
                break
