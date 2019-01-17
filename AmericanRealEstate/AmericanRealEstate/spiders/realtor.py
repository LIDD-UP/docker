# -*- coding: utf-8 -*-
import re

import scrapy
from urllib.parse import urljoin
import pandas as pd

from AmericanRealEstate.items import RealtorHouseInfoJsonItem
from AmericanRealEstate.settings import realtor_search_criteria


class RealtorSpider(scrapy.Spider):
    name = 'realtor'
    allowed_domains = ['realtor.com']

    start_urls = ['https://www.realtor.com/realestateandhomes-search/Adair-County_MO']

    custom_settings = {
        "ITEM_PIPELINES": {
            'AmericanRealEstate.pipelines.RealtorHouseInfoTestPipeline': 302,

        },
        # "LOG_FILE": "realtor_log.txt",
        # "LOG_LEVEL": 'INFO',

    }

    def parse(self, response):
        counties = realtor_search_criteria
        #     [
        #     # 'Monroe-County_NY',
        #     'Haines-County_AK',
        #     'Autauga-County_AL',
        #     'Bibb-County_AL',
        #     'Adair-County_MO',
        #     # '''
        #     # https://www.realtor.com/realestateandhomes-search/Autauga-County_AL
        #     # https://www.realtor.com/realestateandhomes-search/Bibb-County_AL
        #     # '''
        # ]
        for county in counties:
            # houses = response.css('ul.prop-list li.js-quick-view')
            # xpath
            houses = response.xpath("//ul[contains(@class,'prop-list')]/li[contains(@class,'js-quick-view')]")
            for house in houses:
                # css
                # detail_url = house.css('.photo-wrap a::attr(href)').extract_first()
                # xpath
                detail_url = house.xpath("//div[@class='photo-wrap ']/a/@href").extract_first()
                x = re.findall(r'(M\d{5}-\d{5})', detail_url)
                if len(x) != 0:
                    x = x[-1]
                    x = x.replace('-', '')
                    print(x)
                next_detail_page_url = 'https://www.realtor.com/property-overview/{}'.format(x)
                yield scrapy.Request(url=next_detail_page_url,callback=self.parse_content)

                #  / realestateandhomes - detail / 60 - Riverside - Blvd - Apt - 1112_New - York_NY_10069_M37676 - 31493
                # 以防数据接口消失只能用
                # true_detail_url = urljoin(realtor_index_website,detail_url)
                # print(true_detail_url)
                # https: // www.realtor.com / realestateandhomes - detail / 60 - Riverside - Blvd - Apt - 1112_New - York_NY_10069_M37676 - 31493
            # next_page_url = response.css('span.next a.next::attr(href)').extract_first()
            # xpath
            next_page_url = response.xpath("//span[@class='next ']/a[@class='next']/@href").extract_first()
            if next_page_url is not None:
                true_next_page_url = urljoin(response.url,next_page_url)
                yield scrapy.Request(url=true_next_page_url, callback=self.parse)
            next_county_url = 'https://www.realtor.com/realestateandhomes-search/{}'.format(county)
            yield scrapy.Request(url=next_county_url,callback=self.parse)

    def parse_content(self,response):
        realtor_house_info_item = RealtorHouseInfoJsonItem()
        realtor_house_info_item['houseData'] = response.text
        yield realtor_house_info_item

