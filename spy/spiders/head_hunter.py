# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from spy.items import SpyItem
from datetime import datetime

class HeadHunterSpider(scrapy.Spider):
    name = 'head_hunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&items_on_page=50&no_magic=true&page=1']

    def parse(self, response):

        #response.xpath('//div[contains(@data-qa,"vacancy-serp__vacancy")]//div[contains(@class,"resume-search-item__name")]//a/@href').extract()
        for url in response.xpath(
                '//div[contains(@data-qa,"vacancy-serp__vacancy")]//div[contains(@class,"resume-search-item__name")]//a/@href'):
            yield response.follow(url, callback=self.parser_one_vacansia)

        #Проверим наличие кнопки "дальше", и если она есть то мы переходим по ней
        next_page = response.xpath('//div[contains(@data-qa,"pager-block")]//a[contains(@class,"HH-Pager-Controls-Next")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page,callback=self.parse)


    def parser_one_vacansia(self, response):
        item = ItemLoader(SpyItem(),response)
        item.add_value('date_at',datetime.now())


        #item.add_xpath('title', '//h1[contains(@data-qa,"vacancy-title")]/span/text()')
        #Пришлось брать так, потому как надежнее... были вакансии со SPAN, были без
        item.add_xpath('title', '//h1[contains(@data-qa,"vacancy-title")]')
        item.add_value('url', response.url)
        item.add_xpath('description', '//div[contains(@data-qa,"vacancy-description")]/*')
        item.add_xpath('salary', '//div[contains(@class,"vacancy-title")]//meta[contains(@itemprop,"Value")]/@content')
        item.add_xpath('company', '//div[contains(@class,"vacancy-company")]//a[contains(@class,"vacancy-company-name")]/span[contains(@itemprop,"name")]')
        item.add_xpath('company_url',
                       '//div[contains(@class,"vacancy-company")]//a[contains(@class,"vacancy-company-name")]/@href')
        #print(1)
        yield item.load_item()
