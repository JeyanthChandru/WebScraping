import scrapy
import numpy as np
import os
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
# from scrapy.utils.log import configure_logging
import pandas as pd
import matplotlib.pyplot as plt

namesList = np.array([])
locationList = np.array([])
londonLocation = {}
bayAreaLocation = {}

if os.path.isfile('Output.json'):
    os.system("rm Output.json")

class namesSpider(scrapy.Spider):
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
            # if loc == "London" or loc == "Silicon Valley":
            #     yield {
            #         'name': namesList[i],
            #         'location': locationList[i]
            #     }
            if loc == "London":
                londonLocation[namesList[i]] = loc
            elif loc == "Silicon Valley":
                bayAreaLocation[namesList[i]] = loc



# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()
d = runner.crawl(namesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
dfLondon = pd.DataFrame(list(londonLocation.items()), columns=['Name','Location'])
print(dfLondon)
dfBayArea = pd.DataFrame(list(bayAreaLocation.items()), columns=['Name', 'Location'])
print(dfBayArea)
labels = dfLondon['Location'][0], dfBayArea['Location'][0]
sizes = dfLondon.shape[0], dfBayArea.shape[0]
colors = ['blue', 'green']
patches, texts = plt.pie(sizes, labels = labels, colors = colors)
plt.legend(patches, labels, loc = 'best')
plt.axis('equal')
plt.show()
