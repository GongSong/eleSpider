# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


class ShopListPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'ele_shoplist':
            print(item)
            storeId = item['storeId']
            shopName = item['shopName']
            monthSales = item['monthSales']
            shopScore = item['shopScore']
            eleId = item['eleId']
            wid = item['wid']
            lat = item['lat']
            lng = item['lng']
            sql = 'insert into ele_shop(storeId, shopName, eleId, monthSales, shopScore, wid, lat, lng)values (%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                cursor.execute(sql, (str(storeId), shopName, str(eleId), str(monthSales), shopScore, wid, str(lat), str(lng)))
                conn.commit()
            except:
                pass


class ShopInfoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'ele_shopinfo':
            print(item)
            storeId = item['storeId']
            shopName = item['shopName']
            monthSales = item['monthSales']
            shopScore = item['shopScore']
            address = item['address']
            activity = item['activity']
            coupons = item['coupon']
            cats = item['category']
            cat1ids = item['categoryIds']
            city = item['city']
            try:
                sql = 'insert into e_shop_info(storeId, shopName, monthSales, shopScore, address, activity, coupon, category, categoryIds, city)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (str(storeId), shopName, str(monthSales), str(shopScore), address, activity, coupons, str(cats), cat1ids,city))
                conn.commit()
            except:
                pass


class DrugInfoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'ele_druginfo':
            drug_name = item['']
            sku = item['']
            upc = item['']
            sale = item['']
            price = item['']
            original_price = item['']
            category = item['']
            sql = 'insert into ele_drug_info (drug_name, sku, upc, sale, price, original_price, category) values (%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (drug_name, str(sku), str(upc), str(sale), str(price), str(original_price), category))
            conn.commit()