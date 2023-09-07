# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.utils.response import open_in_browser
# from scrapy_playwright.page import PageMethod
# from scrapy.selector import Selector
# import json
# import re
# from urllib.parse import urlencode
# import pandas as pd

# class ExcelizeSpider(scrapy.Spider):
#     name = "excelize"
#     allowed_domains = ["excelize.com"]

#     def start_requests(self):
#         df = pd.read_csv("excel2.csv")
#         urls = df['URL'].tolist()
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
     
#     def parse(self, response):
#         le = LinkExtractor()
#         for link in le.extract_links(response):
#             yield scrapy.Request(url=link.url, callback=self.parse)
#         yield {
#             'content': response.xpath('normalize-space(//body)').get().encode('ascii', 'ignore').decode(),
#         }


#the above code also works cheers :)    
                
import pandas as pd

df = pd.read_csv("excel2.csv")
urls = df['URL'].tolist()

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import json
import re
from urllib.parse import urlencode


class Scrap_content_excel_dfSpider(scrapy.Spider):
    name = "scrap_content_excel_df"
    allowed_domains = ["excelize.com"]
    
    start_urls = urls
     
    def parse(self, response):
        
        html = response.text
        
        body = response.css('.header').getall()
    
        shody = response.css('.FooterBGImage').getall()
        for text in body:
            html = html.replace(text, '')
        for text in shody:
            html = html.replace(text, '')

        # Now, `html` contains the total response text without the elements matching the given xpath expressions

            yield {
                'content': response.xpath('normalize-space(//body)').get().encode('ascii', 'ignore').decode(),
            }    

            
       