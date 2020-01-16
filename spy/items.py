# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup
from scrapy.loader.processors import TakeFirst, MapCompose

def company_url_create(item):
    return f'https://hh.ru{item[0]}'


def salary_create(item):
    res = 0
    tmp = []
    for el in item:
        tmp.append(int(el))

    if len(tmp)>0:
        return int(sum(tmp)/len(tmp))
    else:
        return 0

def description_create(item):
    return ''.join(item)

def html_cleaner(item):
    return BeautifulSoup(''.join(item), "lxml").text



class SpyItem(scrapy.Item):
    # define the fields for your item here like:
    _id         = scrapy.Field()
    date_at     = scrapy.Field()
    title       = scrapy.Field(input_processor=html_cleaner,output_processor=TakeFirst())
    url         = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=description_create, output_processor=TakeFirst())
    salary      = scrapy.Field(input_processor=salary_create, output_processor=TakeFirst())
    company     = scrapy.Field(input_processor=html_cleaner, output_processor=TakeFirst())
    company_url = scrapy.Field(output_processor=company_url_create)
