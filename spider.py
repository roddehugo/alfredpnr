from scrapy import Spider, Item, Field, FormRequest, Request
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose
import ipdb


def strip_word(x):
    return x.strip()

Strip = MapCompose(strip_word)


class Data(Item):
    firstname = Field()
    lastname = Field()
    email = Field()
    tel = Field()


class CheckMyTripSpider(Spider):
    name = 'checkmytrip'
    start_urls =
    post_urls = ['https://classic.checkmytrip.com%s']

    def parse(self, response):
        action = response.xpath('//form[@name="CMTLForm"]/@action').extract()
        if not action:
            yield Exception("Can't find CMTL Form")
        yield FormRequest(
            url=self.post_urls[0] % action[0],
            formdata={
                'DIRECT_RETRIEVE': 'true',
                'SESSION_ID': '',
                'REC_LOC': '2ebdwz',
                'DIRECT_RETRIEVE_LASTNAME': 'bourcier'
            },
            callback=self.parse_postdata)

    def parse_postdata(self, response):
        l = ItemLoader(item=Data(), response=response)

        firstname, lastname = response.xpath('//*[@id="pax2"]//span/text()').extract()[0].strip().split(' ')
        l.add_value('firstname', firstname, Strip)
        l.add_value('lastname', lastname, Strip)

        _, email, _, tel = response.xpath('//*[@id="pax1"]//table[2]//td//text()').extract()
        l.add_value('email', email, Strip)
        l.add_value('tel', tel, Strip)

        ipdb.set_trace()
        l.load_item()
