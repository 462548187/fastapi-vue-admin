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


# @issue_router.get('/issue_lists', name="任务列表")
# async def issue_lists(db: Session = Depends(get_db), current_user: User = Depends(check_perm('/menu/menu_lists'))):
#     # 查询一级菜单
#     menu_list = []
#     all_menus = db.query(Menu).all()
#     parent_menus = db.query(Menu).filter(Menu.parent_id == 0).all()
#     all_parent_ids = [menu.parent_id for menu in db.query(Menu.parent_id).distinct().all()]
#     for parent_menu in parent_menus:
#         # 递归获得子菜单
#         parent_menu_dict = {"menu_id": str(parent_menu.menu_id), "menu_name": parent_menu.menu_name}
#         if parent_menu.menu_id in all_parent_ids:
#             parent_menu_dict["children"] = get_menus(parent_menu.menu_id, all_menus, all_parent_ids)
#         menu_list.append(parent_menu_dict)
#     return JSONResponse({"menus": menu_list})


@issue_router.put('/add_issue', name="新增任务")
async def add_issue(issue: IssueBase, request: Request, db: Session = Depends(get_db),
                   current_user: User = Depends(check_perm('/issue/add_issue'))):
    # 确认任务不存在
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


# @menu_router.post('/edit_menu', name="修改菜单")
# async def edit_menu(menu: MenuBase, request: Request, db: Session = Depends(get_db),
#                     current_user: User = Depends(check_perm('/menu/edit_menu'))):
#     # 确认menu不存在
#     old_menu = db.query(Menu).filter(Menu.menu_id == int(menu.menu_id)).first()
#     if not old_menu:
#         raise HTTPException(status_code=406, detail="要修改的菜单不存在")
#     # 确认菜单是否重复
#     old_record = deepcopy(old_menu)
#     if menu.menu_name != old_menu.menu_name:
#         if db.query(Menu).filter(Menu.menu_name == menu.menu_name).first():
#             raise HTTPException(status_code=406, detail="菜单名已存在")
#     if menu.menu_flag != old_menu.menu_flag:
#         if db.query(Menu).filter(Menu.menu_flag == menu.menu_flag).first():
#             raise HTTPException(status_code=406, detail="菜单标识已存在")
#     old_menu.menu_name = menu.menu_name
#     old_menu.menu_flag = menu.menu_flag
#     old_menu.parent_id = int(menu.parent_id)
#     new_record = deepcopy(old_menu)
#     db.add(old_menu)
#     db.commit()
#     Record.create_operate_record(username=current_user.username, old_object=old_record, new_object=new_record,
#                                  ip=request.client.host)
#     return {"message": "菜单修改成功"}
#
#
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

