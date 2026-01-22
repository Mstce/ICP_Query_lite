# -*- coding: utf-8 -*-
"""
Lite ICP query service: query endpoints only.
"""
from aiohttp import web
from load_config import config
from mlog import logger
from ymicp import beian
from routes import setup_routes
from middlewares import options_middleware


def create_app():
    app = web.Application()

    icp = beian()
    app["icp"] = icp
    app["appth"] = {
        "web": icp.ymWeb,
        "app": icp.ymApp,
        "mapp": icp.ymMiniApp,
        "kapp": icp.ymKuaiApp,
    }
    app["bappth"] = {
        "bweb": icp.bymWeb,
        "bapp": icp.bymApp,
        "bmapp": icp.bymMiniApp,
        "bkapp": icp.bymKuaiApp,
    }

    setup_routes(app)
    app.middlewares.append(options_middleware)
    return app


def main():
    app = create_app()
    logger.info(
        f"lite service start - host={config.system.host} port={config.system.port}"
    )
    web.run_app(app, host=config.system.host, port=config.system.port)


if __name__ == "__main__":
    main()
