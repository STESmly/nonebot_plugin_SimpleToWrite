<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-SimpleToWrite

_✨ NoneBot 插件描述 ✨_

这是一个 onebot.v11的词库插件，兼b站直播间弹幕监听插件

## 特别鸣谢

- [blivedm](https://github.com/xfgryujk/blivedm)项目的灵感来源以及部分实现的参考

## 📖 介绍

词库插件方面：

面向小白的词库插件,目的是减少编写代码的时间和难度 特点:语言精简 无需重启nb和reload即可实
现功能热重载 缺点:目前仅能实现一些简单的逻辑运行,但随着更新肯定会慢慢削减

支持自开发函数，只要不跳脱当前解析框架一般都能成功解析并做出对应的反馈

b站直播间弹幕监听方面：

通过ws连接b站直播间，监听弹幕
具体使用方法和配置见下面的配置和使用例子

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_SimpleToWrite

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_SimpleToWrite
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_SimpleToWrite"]

</details>

## ⚙️ 配置

注:一定要在机器人的项目目录(.env文件同级目录)下创建一个名为dicpro.txt的文件 因为消息接收
的逻辑还不够完善(因为只写了接收字符串的)所以在日常使用中日志会经常出现报错的情况(这点
我也注意到了，下次更新的时候尽量减少日志的报错量)

建议日志等级：IFNO


什么？函数表看不懂？
放心，自从0.1.2版本之后我会做教程放在项目里面，也可以被指令响应

请在.env文件里面这样配置

```bash
COMMAND_START=["/",""]

help_type=0  ##0为文字 1为图片

teach_on_off=1 ##是否开启教程功能1是开，其他为关闭

help_on_off=1 ##是否开启帮助功能1是开，其他为关闭

allowed_groups=["能触发教程的指令的群号"]

bililiveid=[b站直播间id] 
bilitoken=  ##这里填一个已登录账号的cookie的SESSDATA字段的值。不填也可以连接，但是收到弹幕的用户名会打码，UID会变成0
bililivedown=on ##是否开启b站直播间弹幕监听功能，on为开启，其他为关闭
bilidmj=on ##是否开启b站直播间弹幕显示器，on为开启，其他为关闭
loadws= ##是否开启websocket功能，默认为ws://127.0.0.1:8000/onebot/v11/ws

```

## 如何使用b站弹幕功能

在.env文件里面配置好之后，在你自己的py文件里面这样使用ws
以默认的ws://127.0.0.1:8000/onebot/v11/ws为例

```bash
from aiohttp import web
import threading
import nonebot

async def websocket_handler(request):  ##千万别在这里使用async def websocket_handler(request,bot: Bot):不然会导致报错无法连接
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        reout = msg.data
        tes = json.loads(msg.data)
        send = tes["message"]
        (bot,) = nonebot.get_bots().values()
        await bot.send_private_msg(user_id=12335, message=send)

    return ws

def run_app():
    app = web.Application()
    app.router.add_get("/onebot/v11/ws", websocket_handler)
    web.run_app(app, host="127.0.0.1", port=8000,print=None)

# 在主线程中创建一个子线程，防止卡住nb进程（或者用py单独运行个.py文件也行）
thread = threading.Thread(target=run_app)
thread.start()

```

参数说明
```bash
{
    "user_id": int, 
    "nickname": str,
    "message": str,
    "room_id": int,
    "type": str, ##仅支持普通消息（message）和醒目留言（super_chat）
    "price":int
}

```

| 指令 | 类型 | 别名 | 说明 |
|:-----:|:----:|:----:|:----:|
| 教程大全 | command | 教程，机器人 | 呼出教程菜单和列表 |
| 查询 | command | 无 | 模糊匹配，查询相似的结果 |
| 解释 | 同 | 无 | 输入序号，查询对应结果 |
| 上一页/下一页 | 同 | 无 | 顾名思义，就是翻页的 |
| help | 同 | 菜单 | 显示被允许显示的指令 |

## 如何使用help菜单

在机器人项目根目录下创建一个名为help.txt（和dicpro.txt同级）的文件：

如果你dicpro.txt文件里面是这样的：

```bash
指令1
$sendtext 这是接收到指令1后的发送$
  
指令2
$sendreply 0$
$sendat QQ$
$senduserimage$

指令3
$getgroupid 0$
```

那么help.txt文件里面应该是这样的：

```bash
yes | 发送文本   ##后面的就是备注，前面的是yes就显示，no就不显示
no | none
yes | 群号
```

那么help的效果就是这样的：
```bash
欢迎使用指令助手,以下是选择开放使用的指令
    [指令1]    发送文本
    [指令3]    群号
发送指令即可使用
```

## 🎉 使用
### 函数表

![ffa338865205732fbc217b0c277640a4](https://github.com/user-attachments/assets/58811893-93a0-4af3-8ddc-14f58f8668b0)

有新函数请往插件自带的教程大全里面看

### 词库格式
```bash
指令1
$sendtext 这是接收到指令1后的发送$
  
指令2
$sendreply 0$
$sendat QQ$
$senduserimage QQ$
```

### 效果图
![4cad3b976d43a88d37ed7a0a087543ca](https://github.com/user-attachments/assets/ec2dd919-aa85-4a11-9326-801ab99fd579)
![49b421ffc1d4e9eaad65cf636fb7f259](https://github.com/user-attachments/assets/89569d6f-d6b3-45d3-afba-c83db5dd38de)
![a4e3e63add3c93dc1fbe12e46aaa63fe](https://github.com/user-attachments/assets/eb4f1192-4434-4cd2-a652-5623b32aa04c)
![194bf3d8414fa72dee372a208ee73b9d](https://github.com/user-attachments/assets/163d704c-243b-4104-a7be-79e7f4a7b4df)
![3d146e4948b16de1cc78f0a0b8859aba](https://github.com/user-attachments/assets/09982c19-6c80-4a25-9023-85fb39b01951)
