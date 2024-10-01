<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-SimpleToWrite

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-template.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-template">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-template.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

这是一个 nonebot2.v11的词库插件，仅响应群聊事件


## 📖 介绍

面向小白的词库插件，目的是减少编写代码的时间和难度
特点：语言精简
    无需重启nb和reload即可实现功能热重载
缺点：目前仅能实现一些简单的逻辑运行，但随着更新肯定会慢慢削减

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    暂无

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

注：一定要在机器人的项目目录（.env文件同级目录）下创建一个名为dicpro.txt的文件


## 🎉 使用
### 函数表
| 函数 | 说明 |
|:-----:|:----:|
| $sendat 参数$ | 艾特指定QQ的对象，参数说明：填写QQ为艾特触发指令的人，填写QQ号则为艾特指定的人（暂时无法与get里面拿值） |
| $sendreply 参数$ | 回复指令消息，参数说明：随便填，因为目前能力有限，暂时只能回复指令 |
| $sendtext 字符串$ | 发送字符串，参数说明：随便填可用\n进行提行（暂时无法从get里面拿值） |
| $sendurlimage 网络图片链接$ | 发送网络图片，参数说明：网络链接暂时不能解析带空格的（暂时无法从get里面拿值） |
| $sendfileimage 本地图片路径$ | 发送本地图片，参数说明：支持\\和/暂时无法支持其他类型的（暂时无法从get里面拿值） |
| $senduserimage 参数$ | 发送QQ对象的头像，参数说明：填写QQ为触发指令的人的头像，填写QQ号为指定QQ头像。（暂时无法从get里面拿值） |
| $test 指令参数$ | 在线执行函数，参数说明：必须写入非正则括号的字符串指令，配合正则括号一起使用，部分函数无法通过test函数执行。 |
| $asif 比较式$ | 当比较式的逻辑成立时，执行asif后面的函数（不成立则会跳过当前asif所跟的函数），参数说明：目前支持了可以从get里面拿值的比较式有not in|in|==|!= （暂时不支持and和or） 因为在解析逻辑里面有不完整的类型修正所以在写比较试的时候还请注意两边的类型是否一样。特殊说明：当比较式为else时，当前asif后面的函数无条件执行，直到下一个asif不成立为止|
| $sendemojilike n$ | 发送表情表态，参数说明：n为表情id。 （bug，消息定位有时定位到非指令消息上了）|
| $gettext n$ | 发送正则括号的内容，参数说明：n为0时指第一个正则括号的内容。后续：会作为一个正式的get类型，而不是单纯的发送，所以当前为特殊的非get函数 |
| $getgroupid 参数$ | 获取触发指令的群的群号，参数说明：任意。（可被拿值，也可直接发送） |
| $getuserid 参数$ | 获取触发指令的人的QQ号，参数说明：任意。（可被拿值，也可直接发送） |

### 效果图
![4cad3b976d43a88d37ed7a0a087543ca](https://github.com/user-attachments/assets/3d71b761-2058-44cd-97a2-3458226354a8)
![49b421ffc1d4e9eaad65cf636fb7f259](https://github.com/user-attachments/assets/8cf52c9c-708a-4525-948c-00c2706c73f8)
![a4e3e63add3c93dc1fbe12e46aaa63fe](https://github.com/user-attachments/assets/8f664444-8a94-4107-a22e-9385397071ea)
![194bf3d8414fa72dee372a208ee73b9d](https://github.com/user-attachments/assets/d1a1861a-17ee-462d-89c2-c5955cea3376)
![3d146e4948b16de1cc78f0a0b8859aba](https://github.com/user-attachments/assets/48deaaa7-5391-46c3-8a61-d85c220749b7)
