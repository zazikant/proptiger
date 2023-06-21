import scrapy
import scraper_helper as sh

DEFAULT_REQUEST_HEADERS = sh.get_dict(
'''
Accept:
*/*
Accept-Encoding:
gzip, deflate, br
Accept-Language:
en-IN,en;q=0.9,mr-IN;q=0.8,mr;q=0.7,en-GB;q=0.6,en-US;q=0.5
Cache-Control:
no-cache
Cookie:
REFERER=www.google.com; Path=/; GA_SOURCE_ACTUAL=google; GA_MEDIUM_ACTUAL=organic; _gid=GA1.2.217601947.1687271656; _fbp=fb.1.1687271656674.568897063; USERCOUNTRY=India; HOME_CITY=18%2CMumbai; USER_FROM_PPC=FALSE; LANDING_PAGE="https://www.google.com/"; USER_FROM=google; USER_MEDIUM=organic; REF_URL="https://www.proptiger.com/"; XCP=7a7b76c7-15f1-48ba-93f3-8fa6e2f79b82; _gat=1; _ga_45CF08BPVN=GS1.1.1687273681.2.1.1687275650.0.0.0; _ga=GA1.1.2140534443.1687271656; USER_IP=10.0.9.153; _uetsid=88d4d0000f7711ee8eab317fbc595058; _uetvid=88d4d6f00f7711ee90a0f3ef9b3a892d; connect.sid=s%3AijhWefsHAyGD3OCzKkJguyfGdoeWRdG9.eHeCTZdiwL2B3UW3wiQvdblWR8lY9%2BhbZU2ggpbWFNs
Pragma:
no-cache
Referer:
https://www.proptiger.com/
Sec-Ch-Ua:
"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
Sec-Ch-Ua-Mobile:
?0
Sec-Ch-Ua-Platform:
"Windows"
Sec-Fetch-Dest:
empty
Sec-Fetch-Mode:
cors
Sec-Fetch-Site:
same-origin
User-Agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
X-Requested-With:
XMLHttpRequest
'''
)

url = "https://www.proptiger.com/{city}/all-builders?page={page}"
    
cities = ['mumbai', 'pune']
page_numbers = range(1, 10)

class ProtechSpider(scrapy.Spider):
    name = "protech"
    allowed_domains = ["proptiger.com"] 
  
    def start_requests(self):
        for city in cities:
            for page in page_numbers:
                formatted_url = url.format(city=city, page=page)
                yield scrapy.Request(formatted_url)

    def parse(self, response):
        
        yield{
            
            'Dev_name': response.css('.blacklayer ~.heading::text').get(),
            #'Total Projects': response.css('.three-points :nth-child(2) span::text').get(),
            #'Ongoing Projects': response.css('.three-points :nth-child(3) span::text').get()
        }
            
       
        