import scrapy
import requests
from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.utils.markup import remove_tags

class NewsSpider(scrapy.Spider) :
    name = 'cna'

    start_urls = [
        "https://www.channelnewsasia.com/news/singapore"
    ]

    def parse(self, response) :
        top_links = []
        for link in response.xpath("//div[@class='grid__col-4']"):
            root = 'https://www.channelnewsasia.com'
            temp = root + link.xpath(".//div/a/@href").extract_first()
            top_links.append(temp)
            # yield {
            #     'link' : temp
            # }
            yield scrapy.Request(temp, callback=self.getText)
        
    def getText(self, response) :
        if response.xpath(".//div[@class='c-rte--article']/p/text()").extract() != "":
            yield {
                'headlines' : response.xpath(".//h1[@class='article__title']/text()").extract_first(),
                'body' : response.xpath(".//div[@class='c-rte--article']/p/text()").extract(),
                'link' : response
            }


        # next page
        # next_page = response.xpath("").extract_first()
        # if next_page is not None:
        #     next_page_link = response.urljoin(next_page)
        #     yield scrapy.requests(url=next_page_link, callback=self.parse)
        # 'headlines' : response.xpath(".//h1[@class='article__title']/text()").extract_first(),

        
