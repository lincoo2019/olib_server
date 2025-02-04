# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/11/1 下午11:15
# @Author: shiyi0x7f
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import SQLAlchemyError
from random import choice
from loguru import logger
from pydantic import BaseModel

class AccountSchema(BaseModel):
    remix_id: int
    remix_key: str
    num: int

    class Config:
        from_attributes = True

# 数据库模型基类
Base = declarative_base()

# SQLAlchemy 数据库引擎
DATABASE_URL = "db_src" #此处不可直接使用，请自建数据库
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)


class OlibAccount(Base):
    __tablename__ = "tb_name"
    remix_id = Column(Integer, primary_key=True, index=True)
    remix_key = Column(String(50))
    num = Column(Integer)


class MySQLDatabaseManager:
    def __init__(self):
        self.db = SessionLocal()

    def get_one(self):
        try:
            result = self.db.query(OlibAccount).filter(OlibAccount.num > 0).all()
            if result:
                account = choice(result)
                return AccountSchema.from_orm(account).dict()
            else:
                logger.info("No available account with num > 0")
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving account: {e}")
            self.db.rollback()
        return None

    def get_all(self):
        try:
            return self.db.query(OlibAccount).all()
        except SQLAlchemyError as e:
            logger.error(
                f"Error fetching all accounts: {e}")
            self.db.rollback()
        return []

    def update_num(self, remix_id, n):
        try:
            # 更新num字段
            account = self.db.query(OlibAccount).filter(OlibAccount.remix_id == remix_id).one_or_none()
            if account:
                account.num = n
                self.db.commit()
                logger.info(f"Updated remix_id {remix_id} with num {n}")
            else:
                logger.warning(f"Account with remix_id {remix_id} not found")
        except SQLAlchemyError as e:
            logger.error(f"Error updating account: {e}")
            self.db.rollback()

    def __del__(self):
        self.db.close()


# 使用示例
if __name__ == "__main__":
    db_manager = MySQLDatabaseManager()
    key = db_manager.get_one()
    print(key)
