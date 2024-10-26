# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
import threading
from typing import *
from nonebot.log import logger
import nonebot

import aiohttp

from . import blivedm
from .blivedm.models import web as web_models
from .send_ruler import send_ruler
import threading


# 这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0

session: Optional[aiohttp.ClientSession] = None
    
async def main():
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()
def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)


async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_clients():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))

async def send(client, data, msgtype):
    if msgtype == "message":
        logger.opt(colors=True).success(
        f"<fg #551A8B>bilidmchat v0.0.1 </fg #551A8B>| [bililive.message]: Message from {data.uid}@[昵称:{data.uname} 房间号:{client.room_id}] '{data.msg}'"
        )
        await send_ruler(client, data, msgtype)
    elif msgtype == "gift":
        if data.coin_type == "gold":
            res = "金"
        elif data.coin_type == "silver":
            res = "银"
        logger.opt(colors=True).success(
        f"<fg #551A8B>bilidmchat v0.0.1 </fg #551A8B>| [bililive.gift]: gift from {data.uid}@[昵称:{data.uname} 房间号:{client.room_id} 价值:{res}瓜子x{data.total_coin}] <green>赠送了 {data.gift_name} x {data.num}</green>"
        )
    elif msgtype == "guard_buy":
        logger.opt(colors=True).success(
        f"<fg #551A8B>bilidmchat v0.0.1 </fg #551A8B>| [bililive.guard_buy]: guard_buy from {data.uid}@[昵称:{data.uname} 房间号:{client.room_id}] <yellow>购买了 {data.gift_name}</yellow>"
        )
    elif msgtype == "super_chat":
        logger.opt(colors=True).success(
        f"<fg #551A8B>bilidmchat v0.0.1 </fg #551A8B>| [bililive.superchat]: superchat from {data.uid}@[昵称:{data.uname} 房间号:{client.room_id} 价值:{data.price}RMB] <blue>醒目留言： {data.message}</blue>"
        )
        await send_ruler(client, data, msgtype)


class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        asyncio.create_task(send(client, message, msgtype="message"))

    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        asyncio.create_task(send(client, message, msgtype="gift"))

    def _on_buy_guard(self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage):
        asyncio.create_task(send(client, message, msgtype="guard_buy"))

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        asyncio.create_task(send(client, message, msgtype="super_chat"))

def run_main():
    asyncio.run(main())
try:
    if nonebot.get_driver().config.bililivedown == "on":
        thread1 = threading.Thread(target=run_main)
        thread1.start()

# 直播间ID的取值看直播间URL
        try:
            if nonebot.get_driver().config.bililiveid:
                TEST_ROOM_IDS = nonebot.get_driver().config.bililiveid
                logger.opt(colors=True).success(
                f"<yellow>监听直播间弹幕配置</yellow> <green>bililiveid</green> <blue>初始化成功</blue>"
                )
            
            else:
                TEST_ROOM_IDS=[]
                logger.opt(colors=True).warning(
                f"<yellow>监听直播间弹幕配置</yellow> <green>bililiveid</green> <red>未被配置！</red>"
                )
        except AttributeError:
            TEST_ROOM_IDS=[]
            logger.opt(colors=True).warning(
                f"<yellow>监听直播间弹幕配置</yellow> <green>bililiveid</green> <red>未被配置！</red>"
                )
            
        try:
            if nonebot.get_driver().config.bililiveid:
                SESSDATA = nonebot.get_driver().config.bilitoken
                logger.opt(colors=True).success(
                f"<yellow>b站账号配置</yellow> <green>bilitoken</green> <blue>初始化成功</blue>"
                )
            
            else:
                SESSDATA=""
                logger.opt(colors=True).warning(
                f"<yellow>b站账号配置</yellow> <green>bilitoken</green> <red>未被配置！</red>"
                )
        except AttributeError:
            SESSDATA=""
            logger.opt(colors=True).warning(
                f"<yellow>b站账号配置</yellow> <green>bilitoken</green> <red>未被配置！</red>"
                ) 
except AttributeError:
    pass