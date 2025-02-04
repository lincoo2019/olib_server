# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/11/2 上午8:36
# @Author: shiyi0x7f
import os
from pydantic import BaseModel
from typing import Union,Optional
from fastapi import APIRouter,Request,Depends
from loguru import logger
from ..utils import get_downurl_from_api
class DownloadQuery(BaseModel):
    bookid: Union[str,int]
    hashid: str
    remix_key: Optional[str] = None
    remix_id: Optional[str] = None
    source: Optional[str] = None

router = APIRouter()
@router.post("/getdownurl",tags=["getdownurl"])
async def get_down_url(query: DownloadQuery,request: Request):
    logger.info(f"server:{query} {request.client.host}")
    book_id = query.bookid
    hash_id = query.hashid
    source = query.source
    if not book_id or not hash_id:
        res = {'status':'-1','error':'未传入必要信息'}
        return  res
    remix_key = query.remix_key
    remix_id = query.remix_id
    logger.info(f"下载传入参数:{query}")
    res = get_downurl_from_api(book_id,hash_id,remix_key,remix_id)
    return res

if __name__ == '__main__':
    get_downurl_from_api("123","456")
