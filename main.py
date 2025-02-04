import random
import uvicorn
import json
from math import ceil
from loguru import logger
from fastapi import FastAPI, Request,Depends, HTTPException,Response,status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from server.routers import router_get_books,router_get_down_url


app = FastAPI(
    title="Olib Minipogram API",
    version="1.0.1",
    description="一个用于Olib小程序的API接口",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问，可以根据需要指定特定来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    client_ip = request.client.host  # 获取客户端 IP
    return JSONResponse(
        status_code=404,
        content={
            "message": "You got it!",
            "your_ip": client_ip
        }
    )


#routers
app.include_router(router_get_books.router)
app.include_router(router_get_down_url.router)

@app.get("/")
async def root():
    return {"message": " Shiyi0x7f Make the world better!"}


@app.get("/OlibServer")
async def OlibServer():
    with open("OlibServer.json", "r", encoding="utf8") as f:
        json_data = json.load(f)
    return json_data

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000,reload=True)
