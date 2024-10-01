import re
from nonebot.adapters.onebot.v11 import MessageSegment,GroupMessageEvent,Event, PokeNotifyEvent, NotifyEvent
from nonebot import on_message, on_notice
from pathlib import Path
import nonebot
from nonebot.rule import is_type

from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_SimpleToWrite",
    description="本插件适用于零基础的小白向快速编写功能的插件",
    usage="在机器人的项目目录里面新建dicpro.txt，再根据github主页的使用教程进行编写",

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="{项目主页}",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

def test(a, event, data):
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
                if asif(param,event,data):
                    type = 1
                    pass
                else:
                    type = 0
                    pass
            else:
                if type == 1 or type == None:
                    ans += my_function(func_name, param, event,data)
                else:
                    pass
    return ans

def sendat(a, event, data):
    if a == "QQ":
        ans = MessageSegment.at(event.get_user_id())
    else:
        ans = MessageSegment.at(int(a))
    return ans

def sendreply(a, event, data):
    ans = MessageSegment.reply(event.message_id)
    return ans

def getgroupid(a, event, data):
    ans = event.group_id
    return ans

def getuserid(a, event, data):
    ans = event.user_id
    return ans

def sendtext(a, event, data):
    a = MessageSegment.text(a.replace('\\n', '\n'))
    return a

def gettext(a, event, data):
    result = list(data)
    a = MessageSegment.text(result[int(a)].replace('\\n', '\n'))
    return a

def sendurlimage(a, event, data):
    a = MessageSegment.image(a)
    return a

def sendfileimage(a, event, data):
    a = MessageSegment.image(Path(a))
    return a

def senduserimage(a, event, data):
    if a == "QQ":
        a = MessageSegment.image(f'http://q2.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=4')
    else:
        a = MessageSegment.image(f'http://q2.qlogo.cn/headimg_dl?dst_uin={a}&spec=4')
    return a

def is_single_quote(s):
    try:
        arr = eval(s)
        return len(arr) == 1 and isinstance(arr[0], str)
    except:
        return False

def is_double_quote(s):
    try:
        arr = eval(s)
        return len(arr) == 3 and all(isinstance(x, str) for x in arr)
    except:
        return False

def asif(s: str, event, data) -> bool:
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
                    first = my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = my_function(func_name, param, event,data)
                if is_single_quote(str(second)) or is_double_quote(str(second)):
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
                    first = my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = my_function(func_name, param, event,data)
                if is_single_quote(str(second)) or is_double_quote(str(second)):
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
                    first = my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = my_function(func_name, param, event,data)
                s = f"'{first}'=='{second}'"
                if bool(eval(s)):
                    return True
            elif match_4:
                first, second = match_4.groups()
                match_first = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',first)
                match_second = re.search(r'^&#36;(\w+)\s+(.+)&#36;$',second)
                if match_first:
                    func_name, param = match_first.groups()
                    first = my_function(func_name, param, event,data)
                if match_second:
                    func_name, param = match_second.groups()
                    second = my_function(func_name, param, event,data)
                s = f"'{first}'!='{second}'"
                if bool(eval(s)):
                    return True
        
        return bool(eval(s))
    except Exception as e:
        return False

def my_function(func, args, event, data):
    funcname = eval(func)
    return funcname(args, event, data)

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content
def parse_string(s,event,data):
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
                        if asif(param,event,data):
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

request = on_message(rule=is_type(GroupMessageEvent))
pokeevent=on_notice(rule=poke)

@request.handle()
async def _(event: GroupMessageEvent):
    if event.group_id == 809613000 or event.group_id == 512013169 or event.group_id == 905607644 or event.group_id == 924839357 or event.group_id==995225912:
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
                            if func_name == "sendemojilike":
                                (bot,) = nonebot.get_bots().values()
                                mid = event.message_id
                                await bot.call_api("set_msg_emoji_like",message_id=mid,emoji_id=int(param))
                                pass
                            else:
                                ans += my_function(func_name, param, event,data)
                    if ans != "":
                        await request.send(ans)
                    else:
                        pass

@pokeevent.handle()
async def _(event: NotifyEvent):
    if event.group_id == 809613000:
        file_path = 'dicpro.txt'

        s = parse_file(file_path)

        result = parse_string(s)
        if "[戳一戳]" in result:
            result = result["[戳一戳]"]
            ans = ""
            if len(result) != 0:
                for i in range(len(result)):
                    key = result[i]
                    match = re.search(r'^#(\w+)\s+(.+)#$', key)
                    data = ""
                    if match:
                        func_name, param = match.groups()
                        ans += my_function(func_name, param, event,data)
                await pokeevent.send(ans)