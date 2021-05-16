# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  models.py.py
@Description    :  
@CreateTime     :  2021/5/16 6:11 下午
------------------------------------
@ModifyTime     :  
"""
from models.base import Base
from sqlalchemy import Column, BigInteger, DateTime, String, Boolean
from datetime import datetime
from utils.snow_flake import generate_id


class Issue(Base):
    __tablename__ = "issue"
    __table_args__ = ({"comment": "任务表"})
    issue_id = Column(BigInteger, primary_key=True, index=True, default=generate_id, unique=True, comment="任务id")
    issue_name = Column(String(200), nullable=False, unique=True, comment="任务名称")
    business = Column(String(20), nullable=False, unique=True, comment="所属业务")
    issue_type = Column(String(200), nullable=False, unique=True, comment="任务类型")
    issue_priority = Column(String(20), nullable=False, unique=True, comment="任务优先级")
    issue_description = Column(String(200), nullable=False, unique=True, comment="任务描述")
    issue_participant = Column(String(200), nullable=False, unique=True, comment="任务参与人")
    is_active = Column(Boolean(), default=True, comment="是否完成")
    test_time = Column(DateTime(), default=datetime.now, comment="提测时间")
    return_time = Column(DateTime(), default=datetime.now, comment="回归时间")
    online_time = Column(DateTime(), default=datetime.now, comment="上线时间")
    issue_remarks = Column(String(255), nullable=False, unique=True, comment="备注")
    creat_time = Column(DateTime(), default=datetime.now, comment="创建时间")
    update_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now, comment="最后一次更新时间")

    def __repr__(self):
        return f"Issue:{self.issue_name}"
