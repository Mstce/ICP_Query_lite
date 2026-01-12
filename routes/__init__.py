# -*- coding: utf-8 -*-
"""
路由模块
仅包含查询API路由
"""
from aiohttp import web


def setup_routes(app):
    """设置所有路由"""
    from .query_routes import setup_query_routes

    # 注册查询路由
    setup_query_routes(app)

