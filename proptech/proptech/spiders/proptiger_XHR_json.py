import scrapy
import json
from datetime import datetime
import re

def is_possession_date_valid(date_str):
    """
    Checks if the possession date is from the year 2025 onwards.
    It uses regex to find a two-digit year (e.g., '25, '28) and handles the century.
    """
    if not date_str:
        return False
    
    match = re.search(r"'(\d{2})", date_str)
    if match:
        year_str = match.group(1)
        year = int(year_str)
        
        # Handle century: years 00-68 are 20xx, 69-99 are 19xx
        if 0 <= year <= 68:
            full_year = 2000 + year
        else:
            full_year = 1900 + year
            
        return full_year >= 2025
    
    return False

class PropTigerAllBuildersSpider(scrapy.Spider):
    name = "prop_tiger_all_builders"
    allowed_domains = ["proptiger.com"]
    builder_urls_seen = set()
    
    def start_requests(self):
        cities = ["mumbai"]
        for city in cities:
            yield scrapy.Request(
                url=f"https://www.proptiger.com/{city}/all-builders?page=1",
                callback=self.parse_city_page,
                meta={'city': city, 'page': 1}
            )

    def parse_city_page(self, response):
        # Extract developer URLs
        developer_links = response.css('div.b-card .builder-name::attr(href)').getall()
        if not developer_links:
            return

        for link in developer_links:
            developer_url = response.urljoin(link)
            if developer_url not in self.builder_urls_seen:
                self.builder_urls_seen.add(developer_url)
                yield scrapy.Request(url=developer_url, callback=self.parse_developer_page)

        # Handle pagination
        city = response.meta['city']
        page = response.meta['page']
        if page < 7:  # Limit to first 7 pages for testing
            next_page_url = f"https://www.proptiger.com/{city}/all-builders?page={page + 1}"
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_city_page,
                meta={'city': city, 'page': page + 1}
            )

    def parse_developer_page(self, response):
        # This is the same as the parse method in the previous spider
        for project in response.css('section.project-card-main-wrapper'):
            possession_date = project.css('.possession-wrap span::text').get()
            if is_possession_date_valid(possession_date):
                print(f"Found a valid project: {project.css('.proj-name span::text').get()}")
                config_script = project.css('script[type="text/x-config"]::text').get()
                config_data = json.loads(config_script) if config_script else {}
                yield {
                    'name': project.css('.proj-name span::text').get(),
                    'city_name': config_data.get('cityName'),
                    'possession_date': possession_date
                }
            else:
                print(f"Filtered out project: {project.css('.proj-name span::text').get()} with possession date: {possession_date}")

        # Start the XHR requests
        # Extracting entityId and other params from the URL
        # This is a bit of a hack, a more robust solution would be to extract this from the page
        url_parts = response.url.split('/')[-1].split('-')
        entity_id = url_parts[-1]
        group_name = "-".join(url_parts[:-1])
        
        yield self._make_xhr_request(16, group_name, entity_id)

    def _make_xhr_request(self, start_index, group_name, entity_id):
        return scrapy.Request(
            url=f"https://www.proptiger.com/xhr/{group_name}-{entity_id}?startIndex={start_index}&entityType=builder&entityId={entity_id}&format=json",
            callback=self.parse_xhr,
            meta={'start_index': start_index, 'group_name': group_name, 'entity_id': entity_id}
        )

    def parse_xhr(self, response):
        html_content = response.text
        if not html_content:
            return

        selector = scrapy.Selector(text=html_content)
        
        projects = selector.css('section.project-card-main-wrapper')
        if not projects:
            return

        for project in projects:
            possession_date = project.css('.possession-wrap span::text').get()
            if is_possession_date_valid(possession_date):
                print(f"Found a valid project: {project.css('.proj-name span::text').get()}")
                config_script = project.css('script[type="text/x-config"]::text').get()
                config_data = json.loads(config_script) if config_script else {}
                yield {
                    'name': project.css('.proj-name span::text').get(),
                    'city_name': config_data.get('cityName'),
                    'possession_date': possession_date
                }
            else:
                print(f"Filtered out project: {project.css('.proj-name span::text').get()} with possession date: {possession_date}")

        start_index = response.meta['start_index'] + 15
        group_name = response.meta['group_name']
        entity_id = response.meta['entity_id']
        yield self._make_xhr_request(start_index, group_name, entity_id)