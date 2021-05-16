# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  issue.py
@Description    :  
@CreateTime     :  2021/5/16 6:30 下午
------------------------------------
@ModifyTime     :  
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IssueBase(BaseModel):
    issue_name: str
    business: str
    issue_type: Optional[str] = None
    issue_priority: Optional[str] = None
    issue_description: Optional[str] = None
    issue_participant: Optional[str] = None
    is_active: Optional[str] = None
    test_time: datetime
    return_time: datetime
    online_time: datetime
    issue_remarks: Optional[str] = None
    issue_id: Optional[str] = None
