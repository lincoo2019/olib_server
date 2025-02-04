# _*_ coding:utf-8 _*_
# Copyright (C) 2025-2025 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2025/1/7 下午8:53
# @Author: shiyi0x7f
import requests
import time
from loguru import logger
from .load_host import HOST
def get_books_from_api(bookname,
                       languages=["Chinese"],
                       page=None,
                       extensions=None,
                       order=None,
                       limit="20",
                       e=None,
                       yearFrom=None,
                       yearTo=None):
    url = f'https://{HOST}/eapi/book/search'
    headers = {
    'host': HOST,
    'source': 'android',
    'android-app-language': 'zh',
    'android-app-version': '1.11.4',
    'appversion': '1.11.4',
    'android-os-version': '7.1.2',
    'android-mobile-version': 'SM-G9810',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'okhttp/3.12.13',
    }

    if "习近平" in bookname:
        return None

    data = {
        'message': bookname,
        'languages[]': languages,
        'extensions[]': extensions,
        'order': order,
        'limit': limit,
        'e': e,
        'page': page,
        'yearFrom': yearFrom,
        'yearTo': yearTo
    }
    start = time.time()
    resp = requests.post(url,headers=headers,data=data)
    try:
        da = resp.json()
        logger.success(f"搜索{bookname}成功,耗时{time.time() - start:.2f}s")
        return da
    except Exception as e:
        logger.error(f"搜索失败，{e}")
    finally:
        resp.close()#手动关闭连接

def main():
    key_ = '5dcc5da2ccd3f344c0c66a17c33349cf'
    id_ = '38713159'
    k2 = '093338da77fd99ba1fff8f147441d0fb'
    i2 = '38775874'
    k3 = 'b0a84197c4b5699bd660348c4028e488'
    i3 = '31232243'
    i4 = '36303628'
    k4 = '187e26e28b09c7898f52fd182bb77547'
    res = get_books_from_api(bookname='三体',page="3",extensions=['pdf'],languages=['chinese'],yearFrom="2022")
    print(res)
if __name__ == '__main__':
    main()