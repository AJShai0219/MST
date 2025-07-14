import pandas as pd
import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 't2',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

sj = []
lst = []
lst2 = []
error = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'cookie': '''bid=YVa7DVvFNso; douban-fav-remind=1; ll="118175"; __utmz=223695111.1735198502.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_id.100001.4cf6=85acdaf22b29ca94.1735198502.; __yadk_uid=ABUQsSfEnIt5aNhVkoFArrh1KIK5Ie7A; _vwo_uuid_v2=D51873C7B84F5C17D18109879BCBD6FDA|754ba65b119eacb2a77df4763a4fb020; dbcl2="220615150:1ffeh8MoEq4"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.22061; __utmz=30149280.1737293938.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1738936559%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fq%3D%E5%A5%BD%E4%B9%85%E4%B8%8D%E8%A7%81%EF%BC%8C%E6%AD%A6%E6%B1%89%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.115172887.1735198492.1737293938.1738936560.4; __utmb=30149280.0.10.1738936560; __utma=223695111.846969415.1735198502.1735198502.1738936560.2; __utmb=223695111.0.10.1738936560; ck=OP_5; __utmc=30149280; __utmc=223695111; frodotk_db="5af29bf5f03ccbfb10d7d3e1d0b663f1"'''
}
for page in [0, 25, 50, 75]:
    url0 = 'https://movie.douban.com/top250?start={}&filter='.format(page)
    html0 = requests.get(url=url0, headers=headers)
    soup0 = BeautifulSoup(html0.text, 'lxml')
    sj_lst0 = soup0.select('.info .hd a')
    for m in sj_lst0:
        sj.append(m['href'].split('/')[4])

for sid in tqdm(sj):
    try:
        url = 'https://movie.douban.com/subject/{}/'.format(sid)
        for p in range(10):
            html = requests.get(url=url, headers=headers, timeout=5)
            if html.status_code == 200:
                break
            time.sleep(1)
        soup = BeautifulSoup(html.text, 'lxml')
        data = {}
        data['电影链接'] = url
        data['名称'] = soup.select('#content h1')[0].text.strip().split('\n')[0]
        try:
            data['年份'] = int(soup.select('#content h1')[0].text.strip().split('\n')[1].replace('(', '').replace(')', ''))
        except:
            pass
        data['评分'] = float(soup.select('.ll.rating_num')[0].text)
        data['评价人数'] = int(soup.select('.rating_people')[0].text.replace('人评价', '').strip())
        text = soup.select('#info')[0].text.strip().split('\n')
        for m in text:
            try:
                sname = m.split(':')[0].strip()
                svalue = m.split(':')[1].strip()
                data[sname] = svalue
            except:
                pass
        lst2.append(data)
        print(data)
    except:
        error.append(sid)
        print('error')

for sid in tqdm(error):
    try:
        url = 'https://movie.douban.com/subject/{}/'.format(sid)
        for p in range(10):
            html = requests.get(url=url, headers=headers, timeout=5)
            if html.status_code == 200:
                break
            time.sleep(1)
        soup = BeautifulSoup(html.text, 'lxml')
        data = {}
        data['电影链接'] = url
        data['名称'] = soup.select('#content h1')[0].text.strip()
        data['评分'] = float(soup.select('.ll.rating_num')[0].text)
        data['评价人数'] = int(soup.select('.rating_people')[0].text.replace('人评价', '').strip())
        text = soup.select('#info')[0].text.strip().split('\n')
        for m in text:
            try:
                sname = m.split(':')[0].strip()
                svalue = m.split(':')[1].strip()
                data[sname] = svalue
            except:
                pass
        lst2.append(data)
    except:
        print('error')

result = pd.DataFrame(lst2)


def f(x):
    try:
        ls = []
        ls2 = x.split('/')
        for m in ls2:
            ls.append(m.strip())
        return '/'.join(ls)
    except:
        pass


def f2(x):
    try:
        ls = []
        ls2 = x.split('/')
        for m in ls2[0:4]:
            ls.append(m.strip())
        return '/'.join(ls)
    except:
        pass


result['导演'] = result['导演'].apply(f)
result['编剧'] = result['编剧'].apply(f)
result['主演'] = result['主演'].apply(f)
result['类型'] = result['类型'].apply(f)
result['制片国家/地区'] = result['制片国家/地区'].apply(f)
result['语言'] = result['语言'].apply(f)
result['又名'] = result['又名'].apply(f)
result['主演前四个'] = result['主演'].apply(f2)

result.to_excel('豆瓣信息.xlsx', index=None)

try:
    connection = pymysql.connect(**DB_CONFIG)
    with connection.cursor() as cursor:
        columns = ', '.join([f'`{col}` TEXT' for col in result.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS douban_movies ({columns})"
        cursor.execute(create_table_query)

        for _, row in result.iterrows():
            values = ', '.join([f"'{str(val).replace('\\', '\\\\').replace("'", "\\'")}'" for val in row])
            insert_query = f"INSERT INTO douban_movies ({', '.join([f'`{col}`' for col in result.columns])}) VALUES ({values})"
            cursor.execute(insert_query)

    connection.commit()
    print("数据已成功写入 MySQL 数据库。")
except pymysql.Error as e:
    print(f"写入 MySQL 数据库时出现错误: {e}")
finally:
    if connection:
        connection.close()
