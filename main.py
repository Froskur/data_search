from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from spy import settings
from spy.spiders.head_hunter import HeadHunterSpider

if __name__ == '__main__':
        cr_settings = Settings()
        cr_settings.setmodule(settings)
        process = CrawlerProcess(settings=cr_settings)
        process.crawl(HeadHunterSpider)
        process.start()
