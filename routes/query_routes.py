# -*- coding: utf-8 -*-
"""
Query routes (lite).
Only exposes /query/{path}.
"""
import random
import time
import aiohttp
from aiohttp import web
from middlewares import jsondump, wj
from load_config import config
from mlog import logger
from utils import is_valid_url


routes = web.RouteTableDef()


@jsondump
@routes.view(r"/query/{path}")
async def geturl(request):
    path = request.match_info["path"]

    appth = request.app.get("appth", {})
    bappth = request.app.get("bappth", {})

    if path not in appth and path not in bappth:
        return wj({"code": 102, "msg": "不是支持的查询类型"})

    if path not in config.risk_avoidance.allow_type:
        return wj({"code": 102, "msg": "不是支持的查询类型"})

    if request.method == "GET":
        appname = request.query.get("search")
        page_num = request.query.get("pageNum")
        page_size = request.query.get("pageSize")
        proxy = request.query.get("proxy")
        use_proxy = request.query.get("use_proxy", "false").lower() == "true"
    else:
        data = await request.json()
        appname = data.get("search")
        page_num = data.get("pageNum")
        page_size = data.get("pageSize")
        proxy = data.get("proxy")
        use_proxy = bool(data.get("use_proxy", False))

    if not appname:
        return wj({"code": 101, "msg": "参数错误,请指定search参数"})

    if any(appname.endswith(suffix) for suffix in config.risk_avoidance.prohibit_suffix):
        return wj({"code": 405, "message": "不允许的查询内容"})

    start_time = time.time()
    logger.info(
        f"query start path={path} search={appname} pageNum={page_num} "
        f"pageSize={page_size} use_proxy={use_proxy} proxy={proxy}"
    )

    if proxy is not None:
        proxy_url = proxy
        if proxy and not proxy.startswith("http://") and not proxy.startswith("https://"):
            proxy_url = f"http://{proxy}"

        for _ in range(config.captcha.retry_times):
            data = await appth.get(path)(appname, page_num, page_size, proxy=proxy_url)
            if data.get("code", 500) == 200:
                logger.info(
                    f"query done path={path} search={appname} code=200 "
                    f"cost={time.time() - start_time:.2f}s"
                )
                return wj(data)
            if data.get("message", "") == "当前访问已被创宇盾拦截":
                logger.warning("当前访问已被创宇盾拦截")
                return wj(data)
        return wj(data)

    for _ in range(config.captcha.retry_times):
        proxy_url = None

        if use_proxy:
            if config.proxy.local_ipv6_pool.enable:
                proxy_url = ""
            elif config.proxy.tunnel.url and is_valid_url(config.proxy.tunnel.url):
                proxy_url = config.proxy.tunnel.url
                logger.info(f"使用隧道代理：{proxy_url}")
            elif config.proxy.extra_api.url and is_valid_url(config.proxy.extra_api.url):
                timeout = aiohttp.ClientTimeout(total=config.system.http_client_timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(config.proxy.extra_api.url) as req:
                        res = await req.text()
                        proxy_url = f"http://{random.choice(res.split()).strip()}"
                logger.info(f"从代理接口获取代理：{proxy_url}")
            elif config.proxy.extra_api.url:
                logger.error(f"代理接口地址无效：{config.proxy.extra_api.url}")
                return wj({"code": 500, "message": "代理接口地址无效"})
        else:
            logger.info("用户选择不使用代理")

        if path in appth:
            data = await appth.get(path)(appname, page_num, page_size, proxy=proxy_url)
        else:
            data = await bappth.get(path)(appname, proxy=proxy_url)

        if data.get("code", 500) == 200:
            logger.info(
                f"query done path={path} search={appname} code=200 "
                f"cost={time.time() - start_time:.2f}s"
            )
            return wj(data)
        if data.get("message", "") == "当前访问已被创宇盾拦截":
            logger.warning("当前访问已被创宇盾拦截")
            return wj(data)

    logger.warning(
        f"query failed path={path} search={appname} code={data.get('code')} "
        f"cost={time.time() - start_time:.2f}s message={data.get('message')}"
    )
    return wj(data)


def setup_query_routes(app):
    app.add_routes(routes)
