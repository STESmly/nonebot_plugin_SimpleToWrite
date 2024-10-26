import nonebot
import tkinter as tk
import threading
from tkinter.font import Font
import asyncio
from nonebot.log import logger
import aiohttp


async def runload():
    global text, root
    root = tk.Tk()
    root.title("弹幕姬")
    customFont = Font(family="楷体", size=14,weight="bold")
    text = tk.Text(root, font=customFont)
    text.pack()
    root.geometry("400x400")
    root.attributes("-topmost", 1)
    root.mainloop()
def runload1():
    asyncio.run(runload())

try:
    if nonebot.get_driver().config.bililivedown == "on":
        allowedopen = False
        allowedws = False
        try:
            if nonebot.get_driver().config.bilidmj == "on":
                gui_thread = threading.Thread(target=runload1)
                gui_thread.start()
                allowedopen = True
                logger.opt(colors=True).success(
                f"<yellow>弹幕姬</yellow> <green>bilidmj</green> <blue>启动成功</blue>"
                )
            else:
                allowedopen = False
        except AttributeError:
            allowedopen = False
            logger.opt(colors=True).warning(
                f"<yellow>弹幕姬</yellow> <green>bilidmj</green> <red>未被配置！</red>"
                )
            
        try:
            if ws := nonebot.get_driver().config.loadws:
                allowedws = ws
                logger.opt(colors=True).success(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> : <blue>{ws}</blue> 已配置"
                )
            else:
                allowedws = False
                logger.opt(colors=True).warning(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> <red>未被配置！</red>"
                )
        except AttributeError:
            allowedws = False
            logger.opt(colors=True).warning(
                f"<yellow>事件响应地址</yellow> <green>loadws</green> <red>未被配置！</red>"
                )
except AttributeError:
    pass


async def send_data(event, msg,type):
    if allowedws != False:
        url = allowedws
    else:
        url = "ws://127.0.0.1:8000/onebot/v11/ws"
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            if hasattr(msg, 'price'):
                price = msg.price
            else:
                price = 0
            data = {"user_id": msg.uid, 
                    "nickname": f"{msg.uname}",
                    "message": f"{msg.msg}",
                    "room_id": event.room_id,
                    "type": type,
                    "price":price
                    }
            await ws.send_json(data)



async def send_ruler(event=None,msg=None,type=None):
    res = f"{msg.uname}：{msg.msg}"
    await send_data(event, msg, type)
    if allowedopen:
        text.insert(tk.END, res + "\n")
        text.yview_moveto(1)
        root.update()