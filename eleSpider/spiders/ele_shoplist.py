from urllib.parse import urlencode
import scrapy
import json
import time
import random
from eleSpider.eleme import get_local, update_flag, get_cookie, get_sign, getCookie, update_status_code, get_city
from eleSpider.items import ShopListItem

url = 'https://shopping.ele.me/h5/mtop.hasee.channellistservice.getchannellist/1.0/?'


class EleShoplistSpider(scrapy.Spider):
    name = 'ele_shoplist'
    break_point = 0

    def start_requests(self):
        lngs = get_local()[0]
        lats = get_local()[1]
        flag = get_local()[2]
        for index in range(flag, len(lats)):
            update_flag(index)
            self.break_point = 0
            lng = lngs[index]
            lat = lats[index]
            print(lng, lat, '---------------------定位', index)
            for i in range(1, 6):
                if self.break_point == 1:
                    continue
                cookie = get_cookie()
                headers = {
                    'referer': 'https://h5.ele.me/newretail/p/channel/?channel=health',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                    'cookie': cookie
                }
                city_info = get_city(lat, lng, cookie)
                city_id = city_info[1]
                city = city_info[0]
                data = '{"channel":"health","searchType":1,"sortBy":"INTELLIGENCE","pn":' + str(i) + ',"rn":20,"fromPage":"channel","brandFolding":true,"userId":0,"fromalipay":0,"terminal":999,"tag":1,"windowType":"3","deviceId":"0723323F3646423A90E1C91113521372|1596167996969","lat":' + str(lat) + ',"lng":' + str(lng) + ',"latitude":' + str(lat) + ',"longitude":' + str(lng) + ',"cityId":'+str(city_id)+',"bizChannel":"mobile.antispider.default"}'
                sign_t = get_sign(data, cookie)
                sign = sign_t[0]
                t = sign_t[1]
                params = {
                    'jsv': '3.0.0',
                    'appKey': '12574478',
                    't': t,
                    'sign': sign,
                    'type': 'originaljson',
                    'valueType': 'original',
                    'isUseH5Request': 'true',
                    'api': 'mtop.hasee.ChannelListService.getChannelList',
                    'v': '1.0',
                    'windVaneOptions': '[object Object]',
                    'ttid': 'h5@pc_chrome_86.0.4240.75',
                    'data': data
                }
                position = str(lng) + '-' + str(lat)
                time.sleep(random.randint(1, 3))
                yield scrapy.Request(url+urlencode(params), meta={'position': position, 'pn': i, 'data': data}, headers=headers, dont_filter=False)

    def parse(self, response, **kwargs):
        position = response.meta['position']
        data = response.meta['data']
        lng = position.split('-')[0]
        lat = position.split('-')[1]
        proxy = response.meta['proxy']
        item = ShopListItem()
        res = json.loads(response.text)
        print(res)
        if res['ret'] == ['FAIL_SYS_TOKEN_EXOIRED::令牌过期'] or res['ret'] == ['FAIL_SYS_TOKEN_ILLEGAL::非法令牌']:
            getCookie()
            pass
        elif res['data'] == {'errorCode': '0', 'errorDesc': '成功'}:
            self.break_point = 1
            pass
        elif res['ret'] == ['FAIL_SYS_USER_VALIDATE', 'RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试']:
            update_status_code(proxy)
            re_try(data)

        else:
            shop_list = res['data']['data']['shoplist']
            for shop in shop_list:
                shopName = shop['name']
                eleId = shop['eleId']
                monthSales = shop['monthSales']
                wid = shop['wid']
                try:
                    shopScore = shop['shopScore']
                except:
                    shopScore = '无'
                storeId = shop['storeId']
                if '眼镜' in shopName or '成人' in shopName or '趣' in shopName or '优品' in shopName or '口腔' in shopName or '体检' in shopName or '色' in shopName:
                    pass
                else:
                    # print(shopName, eleId, monthSales, wid, shopScore, storeId)

                    item['storeId'] = storeId
                    item['shopName'] = shopName
                    item['monthSales'] = monthSales
                    item['shopScore'] = shopScore
                    item['eleId'] = eleId
                    item['wid'] = wid
                    item['lat'] = lat
                    item['lng'] = lng
                    yield item


# 重发请求
def re_try(data):
    cookie = get_cookie()
    headers = {
        'referer': 'https://h5.ele.me/newretail/p/channel/?channel=health',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'cookie': cookie
    }
    data = data
    sign_t = get_sign(data, cookie)
    sign = sign_t[0]
    t = sign_t[1]
    params = {
        'jsv': '3.0.0',
        'appKey': '12574478',
        't': t,
        'sign': sign,
        'type': 'originaljson',
        'valueType': 'original',
        'isUseH5Request': 'true',
        'api': 'mtop.hasee.ChannelListService.getChannelList',
        'v': '1.0',
        'windVaneOptions': '[object Object]',
        'ttid': 'h5@pc_chrome_85.0.4183.102',
        'data': data
    }
    res = scrapy.Request(url+urlencode(params), headers=headers, )