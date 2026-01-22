# -*- coding: utf-8 -*-
"""
Routes for lite service.
"""


def setup_routes(app):
    from .query_routes import setup_query_routes

    setup_query_routes(app)
