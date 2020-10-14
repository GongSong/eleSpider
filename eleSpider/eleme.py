import pandas as pd
import js2py
import re
import time
import pymysql
import requests
import json
from selenium import webdriver


conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()


# 获取sign
def get_sign(data, cookie):
    t = str(int(time.time() * 1000))
    token = re.findall('_m_h5_tk=(.*?);', cookie)[0].split('_')[0]  # 获取token
    appkey = '12574478'
    js = js2py.EvalJs()
    with open('D:\项目\工作项目\eleSpider\eleSpider\sign.js', 'r', encoding='utf-8') as r:
        js.execute(r.read())  # 运行js
    return js.getSign(token, t, appkey, data), t


# 产生新的cookie，存到数据库
def getCookie():
    t = str(int(time.time() * 1000))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path='D:\Program Files\ChromDriver\chromedriver.exe')
    url = 'https://h5.ele.me/newretail/p/channel/?channel=health'
    browser.get(url)  # 进入的界面
    cookie = browser.get_cookies()  # 获取当前页面的cookie
    strr = ''
    for c in cookie:
        strr += c['name']
        strr += '='
        strr += c['value']
        strr += ';'
    # print(strr)
    _m_h5_tk_enc = strr.split(';')[0].split('=')[1]
    _m_h5_tk = strr.split(';')[1].split('=')[1]
    cookie = 'cna=zIsAF+OMsUICAd9o/mdmySxs; UM_distinctid=1739e9386c6234-029f5a3bfae845-b7a1334-100200-1739e9386c74d1; ubt_ssid=fyrpuhmnxaw10yt40sq9pq1pws038rke_2020-07-30; ut_ubt_ssid=8bu84th7w8c2eo4l2m2e9cgjxn1znigx_2020-07-30; _utrace=45c29aa7585f4244a1e31f2910491180_2020-07-30; track_id=1596166389|c61a4407a51c10f46971be50d4a1201994f05d0bd8ce102c83|c1c90a99d43cdf98f8d04f43ab22a393; tzyy=2b9fb9a1cc65124204de5a5b6009b4c8; USERID=1337276074; UTUSER=1337276074; ZDS=1.0|1596792661|g6ezodhvu+KfrBwCbuaD2GRD6I0vPoypctKeqzvk6sZJr6RAx2RAIGSZMRchZwfoxpJRoEb3wdz99tSZwFHBjA==; t=7e9350427d383a90c931c49d90517ea3; xlly_s=1; _samesite_flag_=true; cookie2=1b03a96aa1728fc0016acb260086ae2d; _tb_token_=be893e08e817; csg=bd3ff3c1; t_eleuc4=id4=0%40BA%2FvuHCrrRj3aoscK7vMf5SYaOj1x1zmzAbOfA%3D%3D; munb=2205056384466; SID=DwAAAABPtTaq6AACAACkz9KCmEuMUwTGZcLmQ0tNpzOYFs8-7Or04yJl; _m_h5_tk=' + _m_h5_tk + '; _m_h5_tk_enc=' + _m_h5_tk_enc + '; nr_security_map_key=67cb9e8a-5492-40bd-839a-27398227ba21; l=eBOZuHrPOz_TpbXYBOfwnurza77tLIRfguPzaNbMiOCP9t1p5fJfWZrXW-L9CnGVHsMXR3uV-FgLBgDvqyCSnxv9-LJYMJM-ndC..; tfstk=c-IlBFxr3a8W7aYc5ut5CPVUkFzAZKHyNFLV0iqV_l4X3QSVit0q7SEKNI5lv21..; isg=BKamDjUAxVBwOZH1kNQ4k4E-9xwoh-pB80bIvpBNMEkDE0Yt-Bf8Uajqaw-fu-JZ; _orbit_h5_utils_channel_=mobile.antispider.default.' + t
    # print(cookie)
    sql = 'update get_cookie set cookie=%s' % ('"' + cookie + '"')
    cursor.execute(sql)
    conn.commit()
    browser.quit()
# getCookie()

# 获取定位坐标,需要读取文件
def get_local():
    df = pd.read_csv(r'D:\\项目\\工作项目\\locations.csv')
    lngs = list(df.iloc[0:, 1])
    lats = list(df.iloc[0:, 2])
    sql = 'select flag from get_cookie'
    cursor.execute(sql)
    flag = int(cursor.fetchone()[0])
    return lngs, lats, flag


# 从数据库取得cookie
def get_cookie():
    sql = 'select cookie from get_cookie'
    cursor.execute(sql)
    cookie = cursor.fetchone()[0]
    conn.commit()
    return cookie


def get_id():
    sql = 'select storeId, eleId, wid, lat, lng from ele_shop'
    cursor.execute(sql)
    all_info = cursor.fetchall()
    conn.commit()
    sql1 = 'select shop_index from get_cookie'
    cursor.execute(sql1)
    shop_index = cursor.fetchone()[0]
    conn.commit()
    return all_info, shop_index


# 更新获取详细信息的爬取点
def update_shopindex(shop_index):
    sql = 'update get_cookie set shop_index=%s' % (shop_index)
    cursor.execute(sql)
    conn.commit()
    
    
def update_flag(index):
    sql = 'update get_cookie set flag=%s' % ('"' + str(index) + '"')
    cursor.execute(sql)
    conn.commit()


# 获取城市信息
def get_city(lat, lng, cookie):
    city_url = 'https://h5.ele.me/restapi/bgs/division/get_division_by_location?latitude=' + str(lat) + '&longitude=' + str(lng)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'cookie': cookie
    }
    result = requests.get(city_url, headers=headers, ).text
    if result == '{"message":"行政区划不存在","name":"DIVISION_NOT_FOUND"}':
        pass
    else:
        res = json.loads(result)
        print(res)
        city = res['city']['name']
        id = res['city']['id']
        return city, id


# 存储代理
def save_proxy():
    url = 'http://webapi.http.zhimacangku.com/getip?num=30&type=2&pro=0&city=0&yys=0&port=11&time=3&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
    response = requests.get(url)
    result = json.loads(response.text)['data']
    print(result)
    if result == '':
        pass
    else:
        for index, one_ip in enumerate(result):
            ip = one_ip['ip']
            port = one_ip['port']
            proxy = str(ip) + ':' + str(port)
            print(proxy)
            sql = 'update proxies set proxy='+'"'+proxy+'"'+','+'status_code = 1 where id={}'.format(index+1)
            print(sql)
            cursor.execute(sql)
            # sql = 'insert into proxies(proxy, status_code) values (%s,%s)'
            # cursor.execute(sql, (proxy, status_code))
            conn.commit()
# save_proxy()

# 获取状态码为1的代理IP
def get_proxy():
    sql = 'select proxy from proxies where status_code=1'
    cursor.execute(sql)
    proxies = cursor.fetchall()
    conn.commit()
    # print(len(proxies))
    if len(proxies) == 0:
        save_proxy()
        sql = 'select proxy from proxies where status_code=1'
        cursor.execute(sql)
        proxies = cursor.fetchall()
        conn.commit()
    return proxies


# 更新代理IP的状态，1为可用，0不可用
def update_status_code(proxy):
    proxy = proxy.split('//')[1]
    sql = 'update proxies set status_code=0 where proxy='+'"'+proxy+'"'
    cursor.execute(sql)
    conn.commit()
