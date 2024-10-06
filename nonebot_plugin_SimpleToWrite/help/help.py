import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from nonebot.adapters.onebot.v11 import Bot, MessageSegment,GroupMessageEvent, Message
from nonebot import on_command
from nonebot.params import CommandArg
import re
from pathlib import Path
import nonebot
from nonebot.log import logger

module_path: Path = Path(__file__).parent

def 生成图片(text, i:int):
    字体路径=f"{module_path}/HYWH-65W.ttf"
    size = i*0.25
    fig, ax = plt.subplots(figsize=(3.5, size))  # 调整画布大小
    font = FontProperties(fname=字体路径)
    ax.text(-0.1, 1.1, text, fontsize=9.5, verticalalignment='top', horizontalalignment='left', fontproperties=font)
    ax.text(1.1, 0, '【BY STES沐霖韵】', fontsize=14, verticalalignment='top', horizontalalignment='right', fontproperties=font)
    ax.axis('off')
    plt.savefig(f'{module_path}/help.png', dpi=120)
    
    
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
        if nonebot.get_driver().config.help_on_off:
            ans = nonebot.get_driver().config.help_on_off
    
        else:
            logger.opt(colors=True).warning(
            f"<yellow>help_on_off</yellow> : <green>教程开关</green> <red>未被配置！</red>"
            )
            return False
    except AttributeError:
        logger.opt(colors=True).warning(
            f"<yellow>help_on_off</yellow> : <green>教程开关</green> <red>未被配置！</red>"
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
    
def get_use_list():
    path = "dicpro.txt"
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read().replace('$', '&#36;')
    lines = s.split("\n")
    result = {}
    current_key = None
    current_list = []
    for line in lines:
        if line.strip():  # 检查行是否为空
            if re.match(r'^(?!&#36;).+$', line):  # 检测到新的键
                if current_key:
                    result[current_key] = current_list
                    type = None
                current_key = line
                current_list = []
            else:
                current_list.append(line)
    if current_key:
        result[current_key] = current_list
    return result

def get_help_list():
    path = "help.txt"
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    lines = s.split("\n")
    result = []
    for line in lines:
        data = line.split(" | ")
        help_list = [str(data[0]),str(data[1])]
        result.append(help_list)
    return result

def print_list(a,b):
    i = 0
    ans = ""
    for key in a:
        try:
            if b[i][0] == "yes":
                ans += f"    [{key}]    {b[i][1]}\n"
            else:
                pass
        except:
            logger.opt(colors=True).warning(
            f"<yellow>警告！</yellow> <green>有指令的相关备注未被配置</green> <red>可能会出现help菜单指令与备注不一致的情况</red>"
            )
            pass
        i += 1
    return ans, i



help = on_command('help',aliases={"菜单"})

@help.handle()
async def _(event: GroupMessageEvent):
    if 开放(event.group_id):
        data, i = print_list(get_use_list(),get_help_list())
        send = "欢迎使用指令助手,以下是选择开放使用的指令\n"+data+"发送指令即可使用"
        if nonebot.get_driver().config.help_type == 1:
            生成图片(send, i)
            await help.send(MessageSegment.reply(event.message_id)+MessageSegment.image(Path(f"{module_path}/help.png")))
        elif nonebot.get_driver().config.help_type == 0:
            await help.send(MessageSegment.reply(event.message_id)+send)
        else:
            await help.send(MessageSegment.reply(event.message_id)+send)
            logger.opt(colors=True).warning(
            f"<yellow>help_type</yellow> : <green>help菜单的样式</green> <red>未被配置！</red>"
            )