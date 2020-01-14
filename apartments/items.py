# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApartmentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id     = scrapy.Field()
    url     = scrapy.Field()
    date_at = scrapy.Field()
    title   = scrapy.Field()
    attrs   = scrapy.Field()
    price   = scrapy.Field()

