# -*- coding: utf-8 -*-
import scrapy
from clothes.items import ClothesItem
from clothes.items import ImageItem


class OwenSpider(scrapy.Spider):
    name = 'owen'
    
    allowed_domains = ['owen.vn']
    start_urls = ['https://owen.vn']

    def parse(self, response):
        category_urls = response.xpath("//ul[@class='groupmenu']/li[position()>=3 and position()<=5]/a/@href").getall()
        for url in category_urls:
            yield response.follow(url=url, callback=self.parse_item)

    def parse_item(self,response):
        item_urls = response.xpath("//a[@class='product photo product-item-photo']/@href").getall()
        for url in item_urls:
            yield response.follow(
                url = url,
                callback=self.parse_item_detail
            )

        next_page = response.xpath("(//a[@class='action  next'])[2]/@href").get()
        if next_page:
            yield response.follow(
               url = next_page,
               callback=self.parse_item
            )

    def parse_item_detail(self,response):
        clothes = ClothesItem()
        clothes["name"] =response.xpath("//h1[@class='page-title']/span/text()").get()
        clothes["price"]=self.normalize_price(response.xpath("(//span[@class='price'])[1]/text()").get())
        clothes["description"]=response.xpath("(//div[@class='description'])[1]/p/text()").getall()
        clothes["image_urls"] = response.xpath("//img[@class='no-sirv-lazy-load']/@src").get()
        
        yield clothes
        

    def normalize_price(self, value):
        return value.strip('\xa0₫')