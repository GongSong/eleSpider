# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
import scrapy
from eleSpider.eleme import get_id, get_sign, get_cookie, update_shopindex, get_city, getCookie, update_status_code
from eleSpider.items import ShopInfoItem


class EleShopinfoSpider(scrapy.Spider):
    name = 'ele_shopinfo'

    def start_requests(self):
        all_info = get_id()[0]
        shop_index = int(get_id()[1])
        for shop_index in range(shop_index, len(all_info)):
            update_shopindex(shop_index)
            one_shop = all_info[shop_index]
            storeId = one_shop[0]
            eleId = one_shop[1]
            wid = one_shop[2]
            lat = one_shop[3]
            lng = one_shop[4]
            cookie = get_cookie()
            city_info = get_city(lat, lng, cookie)
            city_id = city_info[1]
            city = city_info[0]
            data = '{"storeId":' + storeId + ',"wid":' + wid + ',"eleId":' + '"' + eleId + '"' + ',"itemId":"","sceneSugItemIds":"","venusAnchorType":0,"isShowGuessLike":0,"isRankByAlg":0,"isCatRankByAlg":0,"cityId":'+str(city_id)+',"coordsOnly":1,"livingShowChannel":"others","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + lat + ',"lng":' + lng + ',"latitude":' + lat + ',"longitude":' + lng + ',"bizChannel":"mobile.antispider.default"}'
            sign_t = get_sign(data, cookie)
            sign = sign_t[0]
            t = sign_t[1]
            url = 'https://shopping.ele.me/h5/mtop.venus.shopresourceservice.getshopresource/1.0/?'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                'referer': 'https://h5.ele.me/newretail/p/shop/?_from_nr_page=1600652627979&_preview_hash=41973&alsc_source=ut_source_name%5E%5E%E5%BA%97%E9%93%BA%E5%88%97%E8%A1%A8__ut_source_title%5E%5E%E7%B2%BE%E9%80%89__ut_source_describe%5E%5E%E6%8E%A8%E8%8D%90%E5%95%86%E5%AE%B6&cart_sku_ids=&display_refund_label=1&ele_id=E17914057671267804770&entry_from=&id=2233307755&item_id=&keyword=&mult_sku_ids=&newuser_page=0&o2o_search_rank_content=%7B%22tppBuckets%22%3A%2216464%230%23178969%230_16464%232397%236373%23999_16464%232616%237139%23329_16464%233304%2310639%23336%22%7D&rankType=&rank_id=3b71d5e37cec44da9be53f52a5972098&refer=&spm=a2ogi.13893704.category-shopcard.d1&store_id=239793058&wid=2233307755',
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
                'api': 'mtop.venus.ShopResourceService.getShopResource',
                'v': '1.0',
                'windVaneOptions': '[object Object]',
                'ttid': 'h5@pc_chrome_85.0.4183.102',
                'data': data
            }
            yield scrapy.Request(url=url+urlencode(params), headers=headers, meta={'city': city}, dont_filter=True)

    def parse(self, response, **kwargs):
        proxy = response.meta['proxy']
        city = response.meta['city']
        item = ShopInfoItem()
        result = json.loads(response.text)
        # print(result)
        if result['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期'] or result['ret'] == ['FAIL_SYS_TOKEN_ILLEGAL::非法令牌']:
            getCookie()
            pass
        elif result['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
            update_status_code(proxy)

        else:
            global catInfoList
            shopinfo = result['data']['data']['shopInfo']
            storeId = shopinfo['storeId']
            shopName = shopinfo['name']
            monthSales = shopinfo['monthSales']
            shopScore = shopinfo['shopScore']
            address = shopinfo['address']
            shopActivityAndCoupons = result['data']['data']['shopActivityAndCoupons']
            shopActivity = shopActivityAndCoupons['shopActivity']['shopActivityList']
            activity = ''
            for ac in shopActivity:
                activity += ac['msg'] + ';'
            shopCoupons = shopActivityAndCoupons['shopCoupons']['couponDetailList']
            coupons = ''
            for coupon in shopCoupons:
                amount = coupon['amount']
                infoDesc = coupon['infoDesc']
                m = amount + '元券' + infoDesc
                coupons += m + ';'
            cats = ''
            cat1ids = ''
            error = 0
            try:
                catInfoList = result['data']['data']['shopCategoryInfo']['catInfoList']
            except:
                error = 1
            if error == 0:
                for catinfo in catInfoList:
                    if catinfo['name'] == '单品活动' or catinfo['name'] == '满减活动' or catinfo['name'] == '热销爆款':
                        pass
                    elif '喜迎双节' in catinfo['name'] or '日常必备' in catinfo['name'] or '预防过敏' in catinfo['name']:
                        pass
                    else:
                        if '❤' in catinfo['name'] or '🌟' in catinfo['name'] or '💏' in catinfo['name'] or '🤢' in catinfo['name'] or '🌡️' in catinfo['name'] or '💊' in catinfo['name'] or '👩‍💼' in catinfo['name']:
                            pass
                        else:
                            cats += catinfo['name'] + ';'
                        cat1ids += str(catinfo['cat2Ids']) + ';'
            item['storeId'] = storeId
            item['shopName'] = shopName
            item['monthSales'] = monthSales
            item['shopScore'] = shopScore
            item['address'] = address
            item['activity'] = activity
            item['coupon'] = coupons
            item['category'] = cats
            item['categoryIds'] = cat1ids
            item['city'] = city
            yield item