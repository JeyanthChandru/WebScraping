import scrapy
import numpy as np

namesList = np.array([])
locationList = np.array([])
londonLocation = {}
bayAreaLocation = {}

class QuotesSpider(scrapy.Spider):
    name = "names"

    def start_requests(self):
        urls = [
            'https://www.kennet.com/who-we-are/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        namesList = response.css('h3.line.listheader a::text').extract()
        locationList = response.css('span.location::text').extract()
        for i, loc in enumerate(locationList):
            if loc == "London":
                londonLocation[namesList[i]] = loc
            elif loc == "Silicon Valley":
                bayAreaLocation[namesList[i]] = loc
        print(londonLocation, bayAreaLocation)

