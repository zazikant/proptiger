import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector


class SimpleSpider(scrapy.Spider):
    
    name = "simple"
    allowed_domains = ["linkedin.com"]     

    
    def start_requests(self):
        
        login = "https://www.linkedin.com/uas/login"    
        
        yield scrapy.Request(url = login, callback=self.login_page, meta={"playwright": True, "playwright_include_page":True})
        
    async def login_page(self, response):
        
        page = response.meta['playwright_page']
        
        username_input = await page.querySelector('input#session_key')
        
        username_input.fill('zazikant@gmail.com')
        
        username_password = await page.querySelector('input#session_key')
        
        username_password.fill('Shashi@123')
        
        submit_button = await page.querySelector('input#session_key')
        
        submit_button.click()
        
        await page.close()