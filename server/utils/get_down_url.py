# _*_ coding:utf-8 _*_
# Copyright (C) 2025-2025 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2025/1/7 下午9:10
# @Author: shiyi0x7f
import requests
import time
from loguru import logger
try:
    from .load_host import HOST
except ImportError:
    from load_host import HOST
try:
    from .db_sqlalchemy import MySQLDatabaseManager
except ImportError:
    from db_sqlalchemy import MySQLDatabaseManager
def get_remix_key_id()->tuple:
    logger.info("随机取remix_key")
    db = MySQLDatabaseManager()
    data = db.get_one()
    remix_key = data['remix_key']
    remix_id = data['remix_id']
    num = data['num']
    return remix_key,remix_id,num

def get_downurl_from_api(bookid,hashid,remix_key=None,remix_id=None):
    if remix_key is None or remix_id is None:
        remix_key,remix_id,num = get_remix_key_id()
    url = f'https://{HOST}/eapi/book/{bookid}/{hashid}/file'
    cookies = {
        "remix_userid": str(remix_id),
        "remix_userkey": remix_key,
    }
    headers = {
        'host': HOST,
        'source': 'android',
        'android-app-language': 'zh',
        'android-app-version': '1.11.4',
        'appversion': '1.11.4',
        'android-os-version': '7.1.2',
        'android-mobile-version': 'SM-G9810',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'okhttp/3.12.13'
    }
    start = time.time()
    res = {}
    resp = requests.get(url, cookies=cookies,headers=headers,timeout=10)
    try:
        # 发送 GET 请求
        data = resp.json().get('file', {})
        allow = data.get('allowDownload', False)
        if allow:
            logger.success(f"获取下载链接成功, 耗时 {time.time() - start:.2f}s")
            download_url = data['downloadLink'].replace("Z-Library", "O-lib")
            res['status'] = 1  # 正常
            res['durl'] = download_url
        else:
            res['status'] = 0  # 不允许下载
    except Exception as e:
        logger.error(f"获取下载链接失败，{e}")
        res['status'] = -1  # 未知错误
    finally:
        resp.close()
    return res
#{'success': 1, 'file': {'downloadLink': 'https://dln1.fcdn.sk/books-files/_collection/userbooks/9d570951b254da14f97f162e20c39ab6cfdd2680d5a9efb5a653e8ac8563fc73/redirection?filename=%E6%96%B0%E7%A7%91%E5%AD%A6%E6%BC%AB%E6%B8%B8%E6%8C%87%E5%8D%97%EF%BC%8860%E5%B9%B4%E7%BB%8F%E5%85%B8%E7%A7%91%E6%99%AE%E6%9C%9F%E5%88%8A%E3%80%8A%E6%96%B0%E7%A7%91%E5%AD%A6%E5%AE%B6%E3%80%8B%E5%87%BA%E5%93%81%EF%BC%8C%E7%89%9B%E6%B4%A5%E5%89%91%E6%A1%A5%E7%AD%89%E4%B8%80%E7%BA%BF%E5%AD%A6%E8%80%85%E6%92%B0%E5%86%99%EF%BC%8C%E6%B7%B1%E5%85%A5%E4%BA%86%E8%A7%A38%E5%A4%A7%E6%9C%AA%E6%9D%A5%E6%A0%B8%E5%BF%83%E5%AD%A6%E7%A7%91%E3%80%82%E8%84%91%E7%A7%91%E5%AD%A6%E3%80%81%E7%B2%92%E5%AD%90%E7%89%A9%E7%90%86%E3%80%81%E7%94%9F%E5%91%BD%E8%BF%9B%E5%8C%96%E3%80%81%E6%95%B0%E5%AD%A6...%20%28Z-Library%29.epub&md5=DqKH7gQcLOaaaeiMWZslag&expires=1736256550', 'description': '新科学漫游指南（60年经典科普期刊《新科学家》出品，牛_ (Z-Library)', 'author': '[英]《新科学家》杂志', 'extension': 'epub', 'allowDownload': True}}
#下载链接{"success":1,"file":{"allowDownload":false,"disallowDownloadMessage":"我们感谢您对新知识的渴望，但您的每日<span style=\"color:var(--red-35);\">10 下载<\/span>量今天已经达到了上限 :( 你可以等待<span style=\"color:var(--red-35);\">7 hours 58 minutes<\/span>下载计数器刷新，或者通过捐款增加你的上限。谢谢您使用Z-Library!"}}
if __name__ == '__main__':
    bookid="16858130"
    hashid="0e670a"
    remix_id="34306086"
    remix_key="61a007840f1f5be1b50ccd95b23f8b21"
    durl = get_downurl_from_api(bookid,hashid,remix_key,remix_id)
    print(durl)