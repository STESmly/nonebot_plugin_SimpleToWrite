import re
from nonebot.adapters.onebot.v11 import MessageSegment,GroupMessageEvent,Event, PokeNotifyEvent, NotifyEvent, PrivateMessageEvent, PrivateMessageEvent, GroupIncreaseNoticeEvent
from nonebot import on_message, on_notice
from pathlib import Path
import nonebot
from nonebot.rule import is_type
from nonebot.plugin import PluginMetadata
from typing import Literal, Type, TypeVar
from nonebot.adapters.onebot.v11 import Adapter
from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.matcher import current_event, current_bot
from .teach import teach
import httpx

__plugin_meta__ = PluginMetadata(
    name="简易编写词库",
    description="适用于零基础的小白向快速编写功能的词库语言插件",
    usage="在机器人的项目目录里面新建dicpro.txt，再根据github主页的使用教程进行编写",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/STESmly/nonebot_plugin_SimpleToWrite",
    # 发布必填。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

logger.opt(colors=True).success(
        f"<yellow>欢迎使用</yellow> <green>简易词库</green> <yellow>插件</yellow> <red>加入开发或反馈bug既可以提issue，也可以联系我</red> QQ：<blue>3791398858</blue>"
        )

Event_T = TypeVar("Event_T", bound=Type[Event])


def register_event(event: Event_T) -> Event_T:
    Adapter.add_custom_model(event)
    logger.opt(colors=True).trace(
        f"Custom event <e>{event.__qualname__!r}</e> registered from module <g>{event.__class__.__module__!r}</g>"
    )
    return event


@register_event
class GroupMessageSentEvent(GroupMessageEvent):
    """群聊消息里自己发送的消息"""

    post_type: Literal["message_sent"]
    message_type: Literal["group"]

    @overrides(Event)
    def get_type(self) -> str:
        """伪装成message类型。"""
        return "message"
    
@register_event
class PrivateMessageSentEvent(PrivateMessageEvent):
    """私聊消息里自己发送的消息"""


    post_type: Literal["message_sent"]
    message_type: Literal["private"]

    @overrides(Event)
    def get_type(self) -> str:
        """伪装成message类型。"""
        return "message"
    
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

async def test(a, event, data):
    """
    用于执行函数\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    qua = str(event.get_message()).strip(a)
    qua = qua.replace("$", "&#36;")
    lines = qua.split("\n")
    ans = ""
    type = None
    for line in lines:
        match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', line)
        if match:
            func_name, param = match.groups()
            if func_name == "test":
                ans = "禁止套娃"
                break
            if func_name == "asif":
                if await asif(param,event,data):
                    type = 1
                    pass
                else:
                    type = 0
                    pass
            else:
                if type == 1 or type == None:
                    ans += await my_function(func_name, param, event,data)
                else:
                    pass
    return ans

async def sendat(a, event, data):
    """
    用于执行艾特对象\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    if a == "QQ":
        ans = MessageSegment.at(event.get_user_id())
    else:
        ans = MessageSegment.at(int(a))
    return ans

async def sendreply(a, event, data):
    """
    用于执行回复指令\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    ans = MessageSegment.reply(event.message_id)
    return ans

async def senddletemsg(a, event, data):
    """
    用于撤回消息\n
    :param a: 传入消息id
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',a)
    if match:
        func_name, param = match.groups()
        mid = await my_function(func_name, param, event,data)
        try:
            await current_bot.get().delete_msg(message_id=mid)
            return None
        except nonebot.adapters.onebot.v11.exception.ActionFailed as e:
            logger.opt(colors=True).error(
            f"<yellow>错误！</yellow> <blue>无法撤回</blue> <red>可能是机器人无管理员或群主权限</red>"
            )
    else:
        logger.opt(colors=True).error(
        f"<yellow>错误！</yellow> <red>无法识别的获取消息id的函数</red> <blue>{a}</blue>"
        )

async def getmsgid(a, event, data):
    """
    用于得到触发指令的消息id\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    ans = event.message_id
    return str(ans)

async def getreplyid(a, event, data):
    """
    用于得到指令回复的消息的消息id\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    ans = event.reply.message_id
    return str(ans)

async def getgroupid(a, event, data):
    """
    用于得到触发指令的群号\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    try:
        ans = event.group_id
        return ans
    except AttributeError:
        logger.opt(colors=True).info(
        f"<yellow>错误！</yellow> <red>私聊无法获取群号！</red>"
        )
        return '0' 

def getuserid(a, event, data):
    """
    用于得到触发指令的QQ号\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    ans = event.user_id
    return str(ans)

async def getselfid(a, event, data):
    ans = event.self_id
    return str(ans)

async def gettargetid(a, event, data):
    try:
        ans = event.target_id
        return str(ans)
    except AttributeError:
        return None

async def sendemojilike(a, event, data):
    mid = current_event.get().message_id
    (bot,) = nonebot.get_bots().values()
    await bot.call_api("set_msg_emoji_like",message_id=mid,emoji_id=int(a))
    return None

async def sendtext(a, event, data):
    """
    用于执行发送字符串\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    get_data = re.findall(r'(.*)%&#36;(.*)&#36;%(.*)',a)
    if get_data:
        result = ["&#36;"+str(x)+"&#36;" for x in get_data[0] if x in get_data[0]]
        ans = ''
        for value in result:
            match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',value)
            if match:
                func_name, param = match.groups()
                first = await my_function(func_name, param, event,data)
                ans += first
            else:
                ans += value.replace('&#36;', '')
    else:
        ans = a
    a = MessageSegment.text(ans.replace('\\n', '\n'))
    return a

async def gettext(a, event, data):
    """
    用于得到正则括号里面的内容\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    result = list(data)
    if len(result) != 0:
        try:
            a = MessageSegment.text(result[int(a)].replace('\\n', '\n'))
            return str(a)
        except IndexError:
            logger.opt(colors=True).error(
            f"<yellow>异常！</yellow><blue>意外的读取: </blue><red>$gettext {a}$</red>  <green>似乎没有返回值</green>"
            )
            return False
    else:
        logger.opt(colors=True).error(
        f"<yellow>异常！</yellow><blue>意外的读取: </blue><red>$gettext {a}$</red>  <green>似乎没有返回值</green>"
        )
        return False
    
async def getusername(a, event, data):
    """
    用于得到用户名\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    (bot,) = nonebot.get_bots().values()
    if a !="QQ":
        try:
            result = await bot.get_group_member_info(group_id=event.group_id,user_id=a)
            name = result['card']
            if len(str(name)) == 0:
                name = result['nickname']
            return name
        except nonebot.adapters.onebot.v11.exception.ActionFailed:
            logger.opt(colors=True).error(
            f"<yellow>错误！</yellow> <blue>无法获取</blue> <red>群成员</red> {a} <red>不存在</red>"
            )
            return None
    else:
        result = await bot.get_group_member_info(group_id=event.group_id,user_id=event.user_id)
        name = result['card']
        if len(str(name)) == 0:
            name = result['nickname']
        return name

async def getgroupname(a, event, data):
    """
    用于得到群名\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    (bot,) = nonebot.get_bots().values()
    result = await bot.get_group_info(group_id=event.group_id)
    name = result['group_name']
    return name

async def geturl(a, event, data):
    """
    用于得到url\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    qua = a.split(" ")
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(qua[0])
        if len(qua) > 1:
            r = r.json()
            key_list = qua[1].split("@")
            for i in range(1,len(key_list) if len(key_list) >= 1 else 0):
                try:
                    r= r[int(key_list[i])]
                except:
                    r = r[key_list[i]]
        try:
            return r.text
        except AttributeError:
            return str(r)
    except httpx.ConnectTimeout:
        logger.opt(colors=True).error(
        f"<yellow>异常！</yellow>对链接：<blue>{qua[0]}</blue><red> 的请求超时</red>  <green>请稍后再试</green>"
        )
    
async def sendurlimage(a, event, data):
    """
    用于执行发送网络图片\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',a)
    if match:
        func_name, param = match.groups()
        a = await my_function(func_name, param, event,data)
    a = MessageSegment.image(a)
    return a

async def sendfileimage(a, event, data):
    """
    用于执行发送本地图片\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    a = MessageSegment.image(Path(a))
    return a

async def senduserimage(a, event, data):
    """
    用于执行发送用户头像\n
    :param a: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    if a == "QQ":
        a = MessageSegment.image(f'http://q2.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=4')
    else:
        a = MessageSegment.image(f'http://q2.qlogo.cn/headimg_dl?dst_uin={a}&spec=4')
    return a


def is_quote(s):
    """
    用于判断list是为[1,2]还是['1','2']方便进行参数自动修正\n
    :param s: 传入$函数 参数$里面的参数
    """
    arr = eval(s)
    if all(isinstance(x, str) for x in arr):
        return True
    else:
        logger.opt(colors=True).info(
        f"<yellow>错误！</yellow>参数：<blue>{s}</blue><red> 似乎未进行元素统一</red> 请以 <green>[1,2]</green> 或 <green>['1','2']</green> 的形式传入参数"
        )
        return False

async def asif(s: str, event, data) -> bool:
    """
    用于执行if判断\n
    :param s: 传入$asif 比较式$里面的比较式
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    if s == "else":
        return True
    try:
        first_match = re.search(r'(.+)\s+and\s+(.+)', s)
        cecond_match = re.search(r'(.+)\s+or\s+(.+)', s)
        if first_match:
            pass
        if cecond_match:
            pass
        else:
            match_1 = re.search(r'(.+)\s+not\s+in\s+(.+)', s)
            match_2 = re.search(r'(.+)\s+in\s+(.+)', s)
            match_3 = re.search(r'(.+)\s+==\s+(.+)', s)
            match_4 = re.search(r'(.+)\s+!=\s+(.+)', s)
            match_5 = re.search(r'(.+)\s+>=\s+(.+)', s)
            match_6 = re.search(r'(.+)\s+<=\s+(.+)', s)
            match_7 = re.search(r'(.+)\s+>\s+(.+)', s)
            match_8 = re.search(r'(.+)\s+<\s+(.+)', s)
            if match_1:
                first, second = match_1.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                if is_quote(str(second)):
                    match = re.search(r"'(.+)'", first)
                    if match:
                        pass
                    else:
                        s = s.replace(first, f"'{first}'",1)
            elif match_2:
                first, second = match_2.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                if is_quote(str(second)):
                    match = re.search(r"'(.+)'", first)
                    if match:
                        pass
                    else:
                        s = s.replace(first, f"'{first}'",1)
            elif match_3:
                first, second = match_3.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"'{first}'=='{second}'"
                if bool(eval(s)):
                    return True
            elif match_4:
                first, second = match_4.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"'{first}'!='{second}'"
                if bool(eval(s)):
                    return True
            elif match_5:
                first, second = match_5.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"{first}>={second}"
            elif match_6:
                first, second = match_6.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"{first}<={second}"
            elif match_7:
                first, second = match_7.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"{first}>{second}"
            elif match_8:
                first, second = match_8.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = await my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = await my_function(func_name, param, event,data)
                s = f"{first}<{second}"
        return bool(eval(s))
    except Exception as e:
        return False

async def my_function(func, args, event, data):
    """
    用于解析并执行词库里面的执行函数\n
    :param func: 函数名
    :param args: 传入$函数 参数$里面的参数
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    try:
        funcname = eval(func)
        return await funcname(args, event, data)
    except NameError:
        logger.opt(colors=True).info(
        f"<yellow>错误！</yellow> <blue>{func}</blue><red> 函数未被定义</red>"
        )
        pass

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
async def parse_string(s,event,data):
    """
    用于解析文件，将文件解析成json\n
    :param s: 文件内容
    :param event: 事件对象
    :param data: 传入正则匹配到的字符串
    """
    lines = s.split("\n")
    result = {}
    current_key = None
    current_list = []
    type = None

    for line in lines:
        if line.strip():  # 检查行是否为空
            if re.match(r'^(?!&#36;).+$', line):  # 检测到新的键
                if current_key:
                    result[current_key] = current_list
                    type = None
                current_key = line
                current_list = []
            else:
                match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', line)
                if match:
                    func_name, param = match.groups()
                    if func_name == "asif":
                        if await asif(param,event,data):
                            type = 1
                            pass
                        else:
                            type = 0
                            pass
                    else:
                        if type == 1 or type == None:
                            current_list.append(line)
                        else:
                            pass

    if current_key:
        result[current_key] = current_list

    return result

def poke(event: Event):
    return isinstance(event, PokeNotifyEvent)

def groupadd(event: Event):
    return isinstance(event, GroupIncreaseNoticeEvent)

grouprequest = on_message(rule=is_type(GroupMessageEvent))
privaterequest = on_message(rule=is_type(PrivateMessageEvent))
pokeevent=on_notice(rule=poke)
groupaddevent=on_notice(rule=groupadd)

@grouprequest.handle()
async def _(event: GroupMessageEvent):
    qua = str(event.get_message()).strip().replace('\n','\\n')
    file_path = 'dicpro.txt'
    s = parse_file(file_path)
    s = s.replace('$', '&#36;')
    result = parse_string(s,event,qua)
    for key in result:
        match_data = re.search(rf'^{key}$', qua)
        if match_data:
            result = result[key]
            data = match_data.groups()
            ans = ""
            if len(result) != 0:
                for i in range(len(result)):
                    key = result[i]
                    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', key)
                    if match:
                        func_name, param = match.groups()
                        getanstype = await my_function(func_name, param, event,data)
                        if getanstype:
                            ans += getanstype
                if ans != "":
                    await grouprequest.send(ans)
                else:
                    pass

@privaterequest.handle()
async def _(event: PrivateMessageEvent):
    qua = str(event.get_message()).strip()
    file_path = 'dicpro.txt'
    s = parse_file(file_path)
    s = s.replace('$', '&#36;')
    result = parse_string(s,event,qua)
    for key in result:
        match_data = re.search(rf'^{key}$', qua)
        if match_data:
            result = result[key]
            data = match_data.groups()
            ans = ""
            if len(result) != 0:
                for i in range(len(result)):
                    key = result[i]
                    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', key)
                    if match:
                        func_name, param = match.groups()
                        getanstype = await my_function(func_name, param, event,data)
                        if getanstype:
                            ans += getanstype
                if ans != "":
                    await privatemassagefix(event, ans)
                else:
                    pass

@pokeevent.handle()
async def _(event: NotifyEvent):
    if event.group_id == 809613000:
        file_path = 'dicpro.txt'

        s = parse_file(file_path)
        s = s.replace('$', '&#36;')

        result = await parse_string(s,event,data=None)
        if "[戳一戳]" in result:
            result = result["[戳一戳]"]
            ans = ""
            if len(result) != 0:
                for i in range(len(result)):
                    key = result[i]
                    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', key)
                    data = ""
                    if match:
                        func_name, param = match.groups()
                        ans += await my_function(func_name, param, event,data)
                await pokeevent.send(ans)

@groupaddevent.handle()
async def _(event: GroupIncreaseNoticeEvent):
    if event.group_id == 809613000:
        file_path = 'dicpro.txt'

        s = parse_file(file_path)
        s = s.replace('$', '&#36;')

        result = await parse_string(s,event,data=None)
        if "[入群通知]" in result:
            result = result["[入群通知]"]
            ans = ""
            if len(result) != 0:
                for i in range(len(result)):
                    key = result[i]
                    match = re.search(r'^&#36;(\w+)\s+(.+)&#36;$', key)
                    data = ""
                    if match:
                        func_name, param = match.groups()
                        ans += await my_function(func_name, param, event,data)
                await pokeevent.send(ans)