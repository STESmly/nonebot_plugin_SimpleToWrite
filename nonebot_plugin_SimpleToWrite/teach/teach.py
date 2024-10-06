import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from nonebot.adapters.onebot.v11 import Bot, MessageSegment,GroupMessageEvent, Message
from nonebot import on_command
from nonebot.params import CommandArg
import os
from difflib import SequenceMatcher
from pypinyin import pinyin, Style
from pathlib import Path
import nonebot, math
from nonebot.log import logger

try:
    if nonebot.get_driver().config.allowed_groups:
        logger.opt(colors=True).success(
        f"<yellow>allowed_groups</yellow> : <green>被允许使用教程大全的群聊</green> <blue>初始化成功</blue>"
        )
    
    else:
        logger.opt(colors=True).warning(
        f"<yellow>allowed_groups</yellow> : <green>被允许使用教程大全的群聊</green> <red>未被配置！</red>"
        )
except AttributeError:
    logger.opt(colors=True).warning(
        f"<yellow>allowed_groups</yellow> : <green>被允许使用教程大全的群聊</green> <red>未被配置！</red>"
        )

module_path: Path = Path(__file__).parent

def 生成图片(text):
    字体路径=f"{module_path}/HYWH-65W.ttf"
    fig, ax = plt.subplots(figsize=(6, 3.8))  # 调整画布大小
    font = FontProperties(fname=字体路径)
    ax.text(-0.1, 1.1, text, fontsize=9.5, verticalalignment='top', horizontalalignment='left', fontproperties=font)
    ax.text(1.1, 0, '【BY STES沐霖韵】', fontsize=14, verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.axis('off')
    plt.savefig(f'{module_path}/菜单.png', dpi=120)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def divide_and_round(a):
    result = a / 10
    if result < 1:
        return 1
    else:
        return math.ceil(result)

def find_folders_with_keyword(path, keyword):
    result = []
    i = 0
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                i += 1
                dir_pinyin = pinyin(dir, style=Style.TONE3, heteronym=False)
                keyword_pinyin = pinyin(keyword, style=Style.TONE3, heteronym=False)
                if keyword in dir or similar(dir_pinyin[0], keyword_pinyin[0]) > 0.4 or similar(dir, keyword) > 0.4:
                    result.append((i, dir))
            break
        if not result:
            return "暂时没有该文件"
        else:
            return result
    else:
        return "暂时没有文件"
    
def find_folders(path):
    result = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            return dirs
    else:
        return "无"
    
def 开放(群号):
    try:
        if nonebot.get_driver().config.allowed_groups:
            file = nonebot.get_driver().config.allowed_groups
    
        else:
            logger.opt(colors=True).warning(
            f"<yellow>allowed_groups</yellow> : <green>被允许使用教程大全的群聊</green> <red>未被配置！</red>"
            )
            return False
    except AttributeError:
        logger.opt(colors=True).warning(
            f"<yellow>allowed_groups</yellow> : <green>被允许使用教程大全的群聊</green> <red>未被配置！</red>"
            )
        return False
    try:
        if nonebot.get_driver().config.teach_on_off:
            ans = nonebot.get_driver().config.teach_on_off
    
        else:
            logger.opt(colors=True).warning(
            f"<yellow>teach_on_off</yellow> : <green>教程开关</green> <red>未被配置！</red>"
            )
            return False
    except AttributeError:
        logger.opt(colors=True).warning(
            f"<yellow>teach_on_off</yellow> : <green>教程开关</green> <red>未被配置！</red>"
            )
        return False
    
    if str(群号) in file and ans == 1:
        return True
    else:
        return False
    
async def privatemassagefix(event, message):
    """
    用于修正人机合一的私聊发送对象\n
    不使用这个判断的话会导致在私聊人机合一时使用默认的xx.send会导致返回消息一直发送到对bot自身的私聊窗口里面\n
    :param event: 事件对象
    :param message: 发送的消息
    """
    (bot,) = nonebot.get_bots().values()
    if event.target_id:
        return await bot.send_private_msg(user_id=event.target_id,message=message)
    else:
        return await bot.send_private_msg(user_id=event.user_id,message=message)

查询 = on_command("查询")
大全 = on_command('教程大全',aliases={"教程","机器人","部署"})
解释 = on_command("解释")
下一页 = on_command("下一页")
上一页 = on_command("上一页")

@查询.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    if 开放(event.group_id):
        path = f"{module_path}/教学文件"
        keyword = str(args)
        data = find_folders_with_keyword(path=path,keyword=keyword)
        send_data = "欢迎使用《NoneBot2教程大全》,以下是查询到的相似的结果\n\n"
        try:
            for key, value in data:
                send_data += f"【{key}】：{value}\n"
            send_data += f"\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            生成图片(send_data)
            await 查询.send(MessageSegment.image(Path(f"{module_path}/菜单.png"))+MessageSegment.at(event.user_id))
        except:
            await 查询.send(data)

@大全.handle()
async def _(event:GroupMessageEvent):
    if 开放(event.group_id):
        path = f"{module_path}/教学文件"
        paper = f"{module_path}/大全翻页/{event.user_id}.txt"
        data = find_folders(path=path)
        send_data = "欢迎使用《NoneBot2教程大全》\n\n"
        总页数 = divide_and_round(len(data))
        if data == "无":
            await 大全.send("暂时没有教程")
        else:
            if os.path.exists(paper):
                with open(paper, "r", encoding="utf-8") as f:
                    页数 = int(f.read())
                for i in range((页数-1)*10, 页数*10):
                    if i >= len(data):
                        break
                    else:
                        send_data += f"【{i+1}】：{data[i]}\n"
                send_data += f"\n当前页数：第{str(页数)}页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            else:
                with open(paper, "w", encoding="utf-8") as f:
                    f.write(str(1))
                for i in range(0, 10):
                    if i >= len(data):
                        break
                    else:
                        send_data += f"【{i}】：{data[i]}\n"
                send_data += f"\n当前页数：第1页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            生成图片(send_data)
            await 查询.send(MessageSegment.image(Path(f"{module_path}/菜单.png"))+MessageSegment.at(event.user_id))

@解释.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    if 开放(event.group_id):
        ans = str(event.get_message()).strip()
        ans = ans.strip('解释')
        try:
            ans = int(ans)-1
            path = f"{module_path}/教学文件"
            try:
                data = find_folders(path=path)
                path_data1 = f"{module_path}/教学文件/{data[ans]}/文字.txt"
                path_data2 = f"{module_path}/教学文件/{data[ans]}/图.jpg"
                if os.path.exists(path_data1) and os.path.exists(path_data2):
                    with open(path_data1,"r",encoding="utf-8") as f:
                        send_msg = f.read()
                    messages = [
                        {"type": "node",
                         "data": {
                             "name": "STES沐霖韵",
                             "uin": "3549337307",
                             "content": [
                                 {"type": "text",
                                  "data": {
                                      "text": send_msg
                                      }
                                    }
                                ]
                            }
                        }
                    ]
                    await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=messages)
                    await 查询.send(MessageSegment.image(Path(path_data2))+MessageSegment.at(event.user_id))
                elif os.path.exists(path_data1):
                    with open(path_data1,"r",encoding="utf-8") as f:
                        send_msg = f.read()
                    messages = [
                        {"type": "node",
                         "data": {
                             "name": "STES沐霖韵",
                             "uin": "3549337307",
                             "content": [
                                 {"type": "text",
                                  "data": {
                                      "text": send_msg
                                      }
                                    }
                                ]
                            }
                        }
                    ]
                    await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=messages)
                    await 查询.send("暂无配图"+MessageSegment.at(event.user_id))
            except IndexError:
                await 解释.send(Message('请确保输入的序号在有效范围内！'))
        except TypeError:
            await 解释.send("请确保序号为阿拉伯数字")

@上一页.handle()
async def _(event:GroupMessageEvent):
    if 开放(event.group_id):
        path = f"{module_path}/教学文件"
        paper = f"{module_path}/大全翻页/{event.user_id}.txt"
        data = find_folders(path=path)
        send_data = "欢迎使用《NoneBot2教程大全》\n\n"
        总页数 = divide_and_round(len(data))
        if data == "无":
            await 大全.send("暂时没有教程")
        else:
            if os.path.exists(paper):
                try:
                    with open(paper, "r", encoding="utf-8") as f:
                        页数 = int(f.read())
                    for i in range((页数-2)*10, (页数-1)*10):
                        if i >= len(data):
                            break
                        else:
                            send_data += f"【{i+1}】：{data[i]}\n"
                    with open(paper, "w", encoding="utf-8") as f:
                        f.write(str(页数-1))
                    send_data += f"\n当前页数：第{str(页数-1)}页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
                except IndexError:
                    with open(paper, "w", encoding="utf-8") as f:
                        f.write(str(总页数))
                    for i in range((总页数-1)*10, 总页数*10):
                        if i >= len(data):
                            break
                        else:
                            send_data += f"【{i+1}】：{data[i]}\n"
                    send_data += f"\n当前页数：第{总页数}页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            else:
                with open(paper, "w", encoding="utf-8") as f:
                    页数 = f.write(str(1))
                for i in range(0, 10):
                    if i >= len(data):
                        break
                    else:
                        send_data += f"【{i+1}】：{data[i]}\n"
                send_data += f"\n当前页数：第{str(页数)}页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            生成图片(send_data)
            await 查询.send(MessageSegment.image(Path(f"{module_path}/菜单.png"))+MessageSegment.at(event.user_id))

@下一页.handle()
async def _(event:GroupMessageEvent):
    if 开放(event.group_id):
        path = f"{module_path}/教学文件"
        paper = f"{module_path}/大全翻页/{event.user_id}.txt"
        data = find_folders(path=path)
        send_data = "欢迎使用《NoneBot2教程大全》\n\n"
        总页数 = divide_and_round(len(data))
        if data == "无":
            await 大全.send("暂时没有教程")
        else:
            if os.path.exists(paper):
                with open(paper, "r", encoding="utf-8") as f:
                    页数 = int(f.read())
                if 页数 < 总页数:
                    for i in range(页数*10, (页数+1)*10):
                        if i >= len(data):
                            break
                        else:
                            send_data += f"【{i+1}】：{data[i]}\n"
                    with open(paper, "w", encoding="utf-8") as f:
                        f.write(str(页数+1))
                    send_data += f"\n当前页数：第{str(页数+1)}页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
                else:
                    with open(paper, "w", encoding="utf-8") as f:
                        f.write(str(1))
                    for i in range(0, 10):
                        if i >= len(data):
                            break
                        else:
                            send_data += f"【{i+1}】：{data[i]}\n"
                    send_data += f"\n当前页数：第1页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            else:
                with open(paper, "w", encoding="utf-8") as f:
                    f.write(str(1))
                for i in range(0, 10):
                    if i >= len(data):
                        break
                    else:
                        send_data += f"【{i+1}】：{data[i]}\n"
                send_data += f"\n当前页数：第1页/共{总页数}页\n\nTip：\n【上一页\下一页】\n【解释 序号】\n【查询 函数/效果/方法】(例：查询 Message 或 查询 发送图片 等)"
            生成图片(send_data)
            await 查询.send(MessageSegment.image(Path(f"{module_path}/菜单.png"))+MessageSegment.at(event.user_id))