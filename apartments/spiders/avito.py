# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlparse,parse_qs
from apartments.items import ApartmentsItem
from datetime import datetime
from bs4 import BeautifulSoup

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry']

    def parse(self, response):
        #Получим собсвтенно апартаменты со страницы
        appartaments = response.xpath('//div[contains(@class,"item__line")]//a[contains(@class,"snippet-link")]/@href').extract()

        #Просто будем добавлять +1 e тому "p" в урл, который есть
        u = urlparse(response.url)
        params = parse_qs(u.query)
        page = 2
        if 'p' in params:
            page = int(params['p'][0])+1

        next_page = f'{u.path}?p={page}'
        if next_page:
            yield response.follow(next_page,callback=self.parse)


        for item in appartaments:
            yield response.follow(item,callback=self.appartaments_parse)


    def appartaments_parse(self, response):
        attrs_name = response.xpath(
            '//div[contains(@class,"item-view-content-left")]//div[contains(@class,"item-view-block")]//li[contains(@class,"item-params-list-item")]/span/text()').extract()

        attrs_value = response.xpath(
            '//div[contains(@class,"item-view-content-left")]//div[contains(@class,"item-view-block")]//li[contains(@class,"item-params-list-item")]').extract()

        # так как перед SPAN есть пробел, то мы вытаскиваем два значения, вместо одного вот этим:
        # response.xpath('//div[contains(@class,"item-view-content-left")]//div[contains(@class,"item-view-block")]//li[contains(@class,"item-params-list-item")]/text()').extract()
        #[' ', '1 ', ' ', '6 ', ' ', 'кирпичный ', ' ', '1-комнатные ', ' ', '46\xa0м² ', ' ', '26\xa0м² ', ' ','12\xa0м² ']
        # в xpath как взять содержимое без тега я с ходу не нашел

        item_attrs = {}
        for i in range(len(attrs_name)):
            #print(attrs_value[i])
            tag = BeautifulSoup(attrs_value[i], 'html')
            item_attrs[attrs_name[i]] = str(tag.li.span.next_sibling)


        yield ApartmentsItem(
            url=response.url,
            date_at = datetime.now(),
            title = response.xpath('//div[contains(@class,"item-view-content-left")]//h1[contains(@class,"title-info-title")]/span/text()').extract_first(),
            attrs = item_attrs,
            price = response.xpath('//div[contains(@class,"item-view")]//div[contains(@class,"item-price")]//span[contains(@class,"js-item-price")]/@content').extract_first(),
        )




