# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  controller.py
@Description    :  
@CreateTime     :  2021/5/16 7:29 下午
------------------------------------
@ModifyTime     :  
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from models.issue.models import Issue
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from core.db import get_db
from apis.perm.controller import check_perm
from models.user.models import User
from schema.issue import IssueBase
from copy import deepcopy
from utils.Record import Record
from core.config import settings

issue_router = APIRouter()


@issue_router.get('/issue_lists', name="项目任务列表")
async def issue_lists(db: Session = Depends(get_db), current_user: User = Depends(check_perm('/issue/issue_lists'))):
    issue_lists = db.query(Issue).all()
    # TODO 未加分页和查询
    return issue_lists


@issue_router.put('/add_issue', name="新增项目任务")
async def add_issue(issue: IssueBase, request: Request, db: Session = Depends(get_db),
                   current_user: User = Depends(check_perm('/issue/add_issue'))):
    # 确认issue不存在
    old_issue = db.query(Issue).filter(and_(Issue.issue_name == issue.issue_name, Issue.business == issue.business)).first()
    if old_issue:
        raise HTTPException(status_code=406, detail="项目任务已存在")
    new_issue = Issue(
        issue_name=issue.issue_name,
        business=issue.business,
        issue_type=issue.issue_type,
        issue_priority= issue.issue_priority,
        issue_description=issue.issue_description,
        issue_participant=issue.issue_participant,
        issue_remarks=issue.issue_remarks)
    new_record = deepcopy(new_issue)
    db.add(new_issue)
    db.commit()
    Record.create_operate_record(username=current_user.username, new_object=new_record, ip=request.client.host)
    settings.logger.info(f"新增项目任务{issue.issue_name}")
    return {"message": "项目任务新增成功"}


@issue_router.post('/edit_issue', name="修改项目任务")
async def edit_issue(issue: IssueBase, request: Request, db: Session = Depends(get_db),
                    current_user: User = Depends(check_perm('/issue/edit_issue'))):
    # 确认issue不存在
    old_issue = db.query(Issue).filter(Issue.issue_id == int(issue.issue_id)).first()
    if not old_issue:
        raise HTTPException(status_code=406, detail="要修改的项目任务不存在")
    # 确认菜单是否重复
    old_record = deepcopy(old_issue)
    if issue.issue_name != old_issue.issue_name:
        if db.query(Issue).filter(Issue.issue_name == issue.issue_name).first():
            raise HTTPException(status_code=406, detail="项目任务名已存在")
    old_issue.issue_name = issue.issue_name
    old_issue.business = issue.business,
    old_issue.issue_type = issue.issue_type,
    old_issue.issue_priority = issue.issue_priority,
    old_issue.issue_description = issue.issue_description,
    old_issue.issue_participant = issue.issue_participant,
    old_issue.issue_remarks = issue.issue_remarks

    new_record = deepcopy(old_issue)
    db.add(old_issue)
    db.commit()
    Record.create_operate_record(username=current_user.username, old_object=old_record, new_object=new_record,
                                 ip=request.client.host)
    return {"message": "项目任务修改成功"}


# @menu_router.get('/get_menu_info', name="获取菜单详细信息")
# async def get_menu_info(menu_id: str, db: Session = Depends(get_db),
#                         current_user: User = Depends(check_perm('/menu/get_menu_info'))):
#     menu = db.query(Menu).filter(Menu.menu_id == int(menu_id)).first()
#     if not menu:
#         raise HTTPException(status_code=406, detail="没有此菜单")
#     return MenuBase(menu_id=menu_id, menu_name=menu.menu_name, menu_flag=menu.menu_flag, parent_id=str(menu.parent_id))
#
#
# def get_menus(parent_id, all_menus, all_parent_ids):
#     child_menus = []
#     child_menus_dicts = []
#     for menu in all_menus:
#         if menu.parent_id == parent_id:
#             child_menus.append(menu)
#     for child_menu in child_menus:
#         # 判断有没有子菜单
#         child_menus_dict = {"menu_id": str(child_menu.menu_id), "menu_name": child_menu.menu_name}
#         if child_menu.menu_id in all_parent_ids:
#             child_menus_dict["children"] = get_menus(child_menu.menu_id, all_menus, all_parent_ids)
#         child_menus_dicts.append(child_menus_dict)
#     if len(child_menus) == 0:
#         return
#     return child_menus_dicts

