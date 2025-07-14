import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector

db_config = {
    'user': 'root',  
    'password': '123456',  
    'host': 'localhost', 
    'database': 't2',  
    'raise_on_warnings': True
}

lst = []
cookies = {
    'BIDUPSID': '93C1B5EA02DC27053ED445E53CA741FA',
    'PSTM': '1734347078',
    'BAIDUID': '93C1B5EA02DC27053ED703EDF07318AA:SL=0:NR=10:FG=1',
    'MAWEBCUID': 'web_CzThllQPLijHTYvnXUXRgPhpkGQIkObXVrXurQazcnfxyBbXeV',
    'H_PS_PSSID': '62325_63148_63324_63724_63274_63798_63881_63904_63902_63925_63949_63947_63957_63995',
    'H_WISE_SIDS': '62325_63148_63324_63724_63274_63798_63881_63904_63902_63925_63949_63947_63957_63995',
    'BDUSS': 'lBU3V1cFBsOXhYWjhjfjRkNnVIbFlRQktCdmdkdEVWTTRHSDk4U1JVLS05NVpvSVFBQUFBJCQAAAAAAAAAAAEAAADg6ZDzeWFueXVkb25nOTMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL5qb2i-am9oYn',
    'BDUSS_BFESS': 'lBU3V1cFBsOXhYWjhjfjRkNnVIbFlRQktCdmdkdEVWTTRHSDk4U1JVLS05NVpvSVFBQUFBJCQAAAAAAAAAAAEAAADg6ZDzeWFueXVkb25nOTMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL5qb2i-am9oYn',
    'BAIDUID_BFESS': '93C1B5EA02DC27053ED703EDF07318AA:SL=0:NR=10:FG=1',
    'BA_HECTOR': 'a50g8424000l2l2h802l8gak252g8g1k6uute25',
    'ZFY': 'pzaYfoRorLjkLgTPf8eQQkrZIGOA2v2Rt:ABASW91L:BY:C',
    'BDRCVFR[1-SbtEwcKEn]': 'mk3SLVN4HKm',
    'BDRCVFR[15YPCB2dH__]': 'I67x6TjHwwYf0',
    'delPer': '0',
    'PSINO': '3',
    'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
    'H_WISE_SIDS_BFESS': '62325_63148_63324_63724_63274_63798_63881_63904_63902_63925_63949_63947_63957_63995',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://top.baidu.com/board?platform=pc&sa=pcindex_entry',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'tab': 'realtime',
}

response = requests.get('https://top.baidu.com/board', params=params, cookies=cookies, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')
sj_lst = soup.select('.category-wrap_iQLoo')
for m in sj_lst[0:10]:
    data = {}
    data['热搜话题'] = m.select('.c-single-text-ellipsis')[0].text.strip()
    data['热搜值'] = m.select('.hot-index_1Bl1a')[0].text.strip()
    lst.append(data)

result = pd.DataFrame(lst)
result.to_excel('百度热搜.xlsx', index=None)


try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS baidu_hot_search (
        id INT AUTO_INCREMENT PRIMARY KEY,
        hot_topic VARCHAR(255),
        hot_value VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

    for index, row in result.iterrows():
        insert_query = "INSERT INTO baidu_hot_search (hot_topic, hot_value) VALUES (%s, %s)"
        values = (row['热搜话题'], row['热搜值'])
        cursor.execute(insert_query, values)

    conn.commit()
    print("数据已成功插入 MySQL 数据库。")

except mysql.connector.Error as err:
    print(f"数据库错误: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("数据库连接已关闭。")
