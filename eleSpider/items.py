# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopListItem(scrapy.Item):
    # define the fields for your item here like:
    storeId = scrapy.Field()
    shopName = scrapy.Field()
    monthSales = scrapy.Field()
    shopScore = scrapy.Field()
    eleId = scrapy.Field()
    wid = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()


class ShopInfoItem(scrapy.Item):
    storeId = scrapy.Field()
    shopName = scrapy.Field()
    monthSales = scrapy.Field()
    shopScore = scrapy.Field()
    address = scrapy.Field()
    activity = scrapy.Field()
    coupon = scrapy.Field()
    category = scrapy.Field()
    categoryIds = scrapy.Field()
    city = scrapy.Field()



class DrugInfoItem(scrapy.Item):
    drug_name = scrapy.Field()
    sku = scrapy.Field()
    upc = scrapy.Field()
    sale = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    category = scrapy.Field()
