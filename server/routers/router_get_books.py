# _*_ coding:utf-8 _*_
# Copyright (C) 2025-2025 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2025/1/7 下午8:52
# @Author: shiyi0x7f
from loguru import logger
from fastapi import APIRouter,Request,Depends
from pydantic import BaseModel
from typing import List, Optional,Union
from ..utils import get_books_from_api

router = APIRouter()

# 定义请求体模型
class BookQuery(BaseModel):
    bookname: str
    languages: Optional[Union[List[str], str]] = ["Chinese"]
    page: Optional[Union[str,int]] = None
    extensions: Optional[Union[List[str], str]] = None
    order: Optional[str] = None
    limit: Optional[str] = "100"
    e: Optional[str] = None
    yearFrom: Optional[str] = None
    yearTo: Optional[str] = None

@router.post('/getbooks',tags=['query'])
async def get_books(query: BookQuery, request: Request):
    bookname = query.bookname
    languages = query.languages
    extensions = query.extensions
    order = query.order
    limit = query.limit
    e = query.e
    page = query.page
    yearFrom = query.yearFrom
    yearTo = query.yearTo
    logger.info(f"搜索{query}")
    res = get_books_from_api(bookname,languages,page,extensions,order,limit,e,yearFrom,yearTo)
    return res

