import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaparserItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q-{kwargs.get("search")}/']

    def pages(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.pages)

        for link in response.xpath("//a[@class='product-card__img-link']//@href"):
            yield response.follow(link, callback=self.parse_object)


    def parse_object(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaparserItem(), response=response)
        loader.add_xpath('name', "//a[(@class='product-card__name ga-product-card-name')]//text()")
        loader.add_xpath('name', "//div[(@class='product-card__name ga-product-card-name')]//text()")
        loader.add_xpath('price', "//span[(@class='price')]//text()")
        loader.add_xpath('photos', "//div[@class='js-zoom-container']//img/@src")
        loader.add_xpath('_id', "//span[@itemprop='sku']/text()")
        loader.add_value('link', response.url)
        yield loader.load_item()



