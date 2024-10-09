<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-SimpleToWrite

_✨ NoneBot 插件描述 ✨_

这是一个 onebot.v11的词库插件

## 📖 介绍

面向小白的词库插件,目的是减少编写代码的时间和难度 特点:语言精简 无需重启nb和reload即可实
现功能热重载 缺点:目前仅能实现一些简单的逻辑运行,但随着更新肯定会慢慢削减

支持自开发函数，只要不跳脱当前解析框架一般都能成功解析并做出对应的反馈

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



### 更新日志
0.1.7
- 新增获取群昵称和用户昵称的函数

0.1.6
- 重新上传

0.1.5
- 新增获取target_id和self_id的函数
- 修复了0.1.4启动报错的问题（import没删完）
- 新增了戳一戳事件和入群通知事件的响应函数

0.1.4
- 修复了字体文件缺失的bug
- 修复了$sendtext 参数$在发送纯字符串时报错的bug
- 修复了异步函数不完整的bug
- 新增了help和查询指令列表的功能
- 新增了在.env文件中可选择开启或关闭help和教程功能的配置项

0.1.3
- 优化部分日志
- 新增获取消息id的函数
- 优化了部分代码
- 新增通过消息id撤回消息的函数

0.1.2
- 优化了部分传递参数的限制
- 新增教程功能

0.1.1
- 新增私聊消息接收
- 新增人机合一模式
- 优化部分日志
- 修复表情表态的bug