import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import open_in_browser
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
import json
from urllib.parse import urlencode

class json_xhr_scrapSpider(scrapy.Spider):
    name = "json_xhr_scrap"
    allowed_domains = ["thebluebook.com"]

    def start_requests(self):
        login = "https://www.thebluebook.com/globalassets/api/public/getLocations.php?callback=jQuery11130704644806839229_1693550594612&maxRows=20&q=showpopularcities&showregionlist=0&_=1693550594613"
        yield scrapy.Request(url=login, callback=self.parse)
        
        
        #Below code is to yield only one key value pair

    # def parse(self, response):
    #     # Extracting the JSON object from the response text
    #     json_object = json.loads(response.text.split('(', 1)[1].rstrip(');'))

    #     # Extracting the value of the "region" key from all the JSON objects in the "data" list
    #     regions = [data['region'] for data in json_object['data']]

    #     for region_value in regions:
    #         yield {
    #             'region': region_value,
    #         }
    
        #Below code is to yield two key value pair
    
    # def parse(self, response):
    #     # Extracting the JSON object from the response text
    #     json_object = json.loads(response.text.split('(', 1)[1].rstrip(');'))

    # # Extracting the value of the "region" and "city" keys from all the JSON objects in the "data" list
    #     regions_and_cities = [{'region': data['region'], 'city': data['city']} for data in json_object['data']]

    #     for region_and_city in regions_and_cities:
    #         # Removing the double quotes from the region value
    #         region_and_city['region'] = region_and_city['region'].replace('"', '')

    #         yield region_and_city
    
    
        #Below code is to yield two key value pair with url    

    def parse(self, response):
        # Extracting the JSON object from the response text
        json_object = json.loads(response.text.split('(', 1)[1].rstrip(');'))

        # Extracting the value of the "region" and "city" keys from all the JSON objects in the "data" list
        regions_and_cities = [{'region': data['region'], 'city': data['city']} for data in json_object['data']]

        for region_and_city in regions_and_cities:
            # Removing the double quotes from the region value
            region_value = region_and_city['region'].replace('"', '')
            city_value = region_and_city['city'].replace(' ', '+')

            # Constructing the URL with the region and city values
            base_url = 'https://www.thebluebook.com/search.html?'
            query_params = {'region': region_value, 'searchsrc': 'thebluebook', 'searchTerm': 'Painting+Contractors', 'regionLabel': city_value}
            url = base_url + urlencode(query_params)

            yield {
                'url': url
            }

    
        
        
        
       