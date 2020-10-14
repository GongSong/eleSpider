# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
import scrapy
import pymysql
from eleSpider.eleme import get_cookie, get_sign, update_status_code, getCookie, get_city

conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()
url = 'https://shopping.ele.me/h5/mtop.venus.shopcategoryservice.getcategorydetail/1.1/?'


class EleDruginfoSpider(scrapy.Spider):
    name = 'ele_druginfo'

    def start_requests(self):
        sql = 'select storeId,categoryIds from e_shop_info'
        cursor.execute(sql)
        all_info = cursor.fetchall()  # 获取e_shop_info中的storeId和categoryIds
        for shopinfo in all_info:
            storeId = shopinfo[0]
            sql1 = 'select lat, lng from ele_shop where storeId=' + '"' + storeId + '"'
            cursor.execute(sql1)
            lat_lng = cursor.fetchall()[0]
            lat = lat_lng[0]
            lng = lat_lng[1]
            cat2Ids = (shopinfo[1]).split(';')
            for cat2Id in cat2Ids:
                cat3Ids = cat2Id.split(',')
                for i in range(len(cat3Ids)):
                    cat3Id = cat3Ids[i]
                    cookie = get_cookie()
                    city_info = get_city(lat, lng, cookie)
                    city_id = city_info[1]
                    data = '{"storeId":' + '"' + storeId + '"' + ',"categoryIds":"[' + cat3Id + ']","type":1,"pn":1,"rn":20,"sortBy":"","isShowGuessLike":"0","isRankByAlg":"0","version":"1.1","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"cityId":'+str(city_id)+',"bizChannel":"mobile.antispider.default"}'
                    sign_t = get_sign(data, cookie)
                    sign = sign_t[0]
                    t = sign_t[1]
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                        'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600746916808&_preview_hash=16767&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E5997160818204947240&entry_from=&id=2233308144&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23724_16464%232616%237139%23349_16464%233304%2310639%23864%22%7D&rankType=&rank_id=cde52d4637bd420fa280fc1a08dc513c&refer=&spm=a2ogi.13893704.category-shopcard.d5&store_id=239785129&wid=2233308144',
                        'cookie': cookie
                    }
                    params = {
                        'jsv': '3.0.0',
                        'appKey': '12574478',
                        't': t,
                        'sign': sign,
                        'type': 'originaljson',
                        'valueType': 'original',
                        'isUseH5Request': 'true',
                        'api': 'mtop.venus.ShopCategoryService.getCategoryDetail',
                        'v': '1.1',
                        'windVaneOptions': '[object Object]',
                        'ttid': 'h5@pc_chrome_85.0.4183.102',
                        'data': data
                    }
                    meta = {'storeId': storeId, 'cat3Id': cat3Id, 'lat': lat, 'lng': lng}
                    yield scrapy.Request(url+urlencode(params), headers=headers, meta=meta)

    def parse(self, response, **kwargs):
        storeId = response.meta['storeId']
        cat3Id = response.meta['cat3Id']
        lat = response.meta['lat']
        lng = response.meta['lng']
        proxy = response.meta['proxy']
        result = json.loads(response.text)
        print(result)
        if result['ret'] == ["FAIL_SYS_USER_VALIDATE", "RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试"]:
            pass
        elif result['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期'] or result['ret'] == ['FAIL_SYS_TOKEN_ILLEGAL::非法令牌']:
            getCookie()
            EleDruginfoSpider.start_requests(self)
        else:
            foods = result['data']['data']['foods']
            for food in foods:
                name = food['name']
                eleSkuId = food['eleSkuId']
                upc = food['upc']
                monthSell = food['monthSell']
                currentPrice = food['currentPrice']
                originalPrice = food['originalPrice']
                if originalPrice == '':
                    originalPrice = '无'
                categoryIds = food['categoryIds']
                rankId = food['rankId']

            for i in range(1, 5):
                cookie = get_cookie()
                data = '{"storeId":' + '"' + storeId + '"' + ',"categoryIds":"[' + cat3Id + ']","type":1,"pn":' + str(
                    i) + ',"rn":20,"rankId":' + '"' + rankId + '"' + ',"sortBy":"","isShowGuessLike":"0","isRankByAlg":"0","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"cityId":13,"bizChannel":"mobile.antispider.default"}'
                sign_t = get_sign(data, cookie)
                sign = sign_t[0]
                t = sign_t[1]
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                    'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600746916808&_preview_hash=16767&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E5997160818204947240&entry_from=&id=2233308144&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23724_16464%232616%237139%23349_16464%233304%2310639%23864%22%7D&rankType=&rank_id=cde52d4637bd420fa280fc1a08dc513c&refer=&spm=a2ogi.13893704.category-shopcard.d5&store_id=239785129&wid=2233308144',
                    'cookie': cookie
                }
                params = {
                    'jsv': '3.0.0',
                    'appKey': '12574478',
                    't': t,
                    'sign': sign,
                    'type': 'originaljson',
                    'valueType': 'original',
                    'isUseH5Request': 'true',
                    'api': 'mtop.venus.ShopCategoryService.getCategoryDetail',
                    'v': '1.1',
                    'windVaneOptions': '[object Object]',
                    'ttid': 'h5@pc_chrome_85.0.4183.102',
                    'data': data
                }
                print('---------------------------------------------------')
                yield scrapy.Request(url+urlencode(params), headers=headers, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        result = json.loads(response.text)
        print(result)
        if result['ret'] == ["FAIL_SYS_USER_VALIDATE", "RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试"]:
            pass
        elif result['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期'] or result['ret'] == ['FAIL_SYS_TOKEN_ILLEGAL::非法令牌']:
            getCookie()
            EleDruginfoSpider.start_requests(self)
        else:
            res = result['data']['data']['foods']
            name = res['name']
            eleSkuId = res['eleSkuId']
            upc = res['upc']
            monthSell = res['monthSell']
            currentPrice = res['currentPrice']
            originalPrice = res['originalPrice']
            if originalPrice == '':
                originalPrice = '无'
            categoryIds = res['categoryIds']
            print(name, eleSkuId, upc, monthSell, currentPrice, originalPrice, categoryIds)