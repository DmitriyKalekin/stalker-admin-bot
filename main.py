import asyncio
from aiohttp import web, ClientSession
# from aiohttp.web import AccessLogger
import aiomysql
# from api.jobs import jobs_loop
import ssl
from app.routes import setup_routes
from app.telebot import Telebot
# from app.jobs import jobs_loop
from config import get_config
import ujson
# import random
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def shutdown(app):
    if app["session"] is not None:
        await app["session"].close()
    if app["conn"] is not None:
        app["conn"].close()        
    await app.shutdown()


async def init(loop):
    cfg = get_config()
    app = web.Application(loop=loop)
    app["loop"] = loop
    app["jobs"] = []
    app["cfg"] = cfg
    app["session"] = ClientSession(loop=loop, json_serialize=ujson.dumps)  # TODO: можно полностью поместить только в телебота
    app.telebot = Telebot(cfg.URL, app["session"])
    app["conn"] = await aiomysql.connect(
        host=app["cfg"].MYSQL_HOST, port=app["cfg"].MYSQL_PORT,
        user=app["cfg"].MYSQL_USER, password=app["cfg"].MYSQL_PASS,
        db=app["cfg"].MYSQL_DBNM, loop=app["loop"], autocommit=True
    )
    setup_routes(app)
    app.on_cleanup.append(shutdown)
    return app


def main():
    cfg = get_config()
    ssl_ctx = None
    if cfg.ENV != "Local":
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain('/etc/ssl/eva-bot.ru/flask.pem', '/etc/ssl/eva-bot.ru/certificate.key')
    loop = asyncio.get_event_loop()
    try:
        # asyncio.ensure_future(jobs_loop())
        web.run_app(init(loop), host=cfg.HOST, port=cfg.PORT, ssl_context=ssl_ctx, reuse_port=cfg.REUSE_PORT)
    except (SystemExit, KeyboardInterrupt):
        print('Stopping service...')
    loop.close()


if __name__ == "__main__":
    main()

