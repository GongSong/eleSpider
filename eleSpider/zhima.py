import json
import pymysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
conn = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='shopinfo', charset='utf8')
cursor = conn.cursor()
sched = BlockingScheduler()


def save_proxy():
    url = 'http://webapi.http.zhimacangku.com/getip?num=49&type=2&pro=0&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
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



