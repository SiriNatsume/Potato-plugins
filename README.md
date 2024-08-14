<div align="center">
     <img alt="potato_avatar.jpg" height="200" src="https://github.com/Hydrogens2/Potato-plugins/raw/main/potato_avatar.jpg" width="200"/>
</div>

<h1 align="center">Potato</h1>

## 前言
这里是Potato 的一些插件，适用于 onebot11，部分也适配 red、satori，~~我也不知道我之前写的什么东西。~~
## 插件列表
- **potato_heweather_report**
  - 需要 onebot v11 协议适配器，原插件可多协议适配。
  - 实现定时的天气播报及查询，可以分群开关并配置查询城市，使用[和风天气 api](https://console.qweather.com/) 。
  - 修改自插件 [nonebot-plugin-heweather](https://github.com/kexue-z/nonebot-plugin-heweather) ，加入了定时播报功能，感谢。
- **potato_reminder_new**
  - 需要 onebot v11 协议适配器，但可快速更改为 red 。
  - 实现对当天节假日信息的获取，并将信息组织成问句向 [Spark](https://www.xfyun.cn/) 模型获取回答，感谢讯飞的巨量免费 tokens 。
  - 实现午餐播报的餐单添加。
- **[nonebot_plugin_fortune](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)**
  - 需要 onebot v11 协议适配器。
  - 实现简单的抽签，并保证每日只能抽一次。
  - 使用时请确认环境 pillow 库版本小于9.5.0，否则将出现无任何日志报错，建议使用9.1.0。
  - 原插件已不再维护。
- **potato_read_60s**
  - 需要 onebot v11 协议适配器，但可快速更改为 red 。
  - 实现每日定时的新闻播报，实现开启群组的动态添加。
  - 源api有时不稳定，使用时请注意及时更新缓存图的绝对路径。
  - 修改自更加古早版本的 [nonebot-plugin-60s](https://github.com/techotaku39/nonebot-plugin-60s) ，感谢。
  - 原插件已不再维护。
- **[nonebot_plugin_sticker_saver](https://github.com/colasama/nonebot-plugin-sticker-saver)**
  - 需要 onebot v11 协议适配器。
  - 一款很简单的，用于保存已经不提供保存选项的 QQ 表情包的 Nonebot 插件。
  - 添加了群聊白名单功能。
- **potato_plugin_ncm**
  - 需要 onebot v11 协议适配器。
  - 实现定时播报音乐，并可动态添加曲目。
  - 使用 [pyncm](https://pypi.org/project/pyncm)，适用于 Python 3 的网易云音乐 API 。
  - 关于 API 的引出直接参考~~抄~~自 [nonebot_plugin_ncm](https://github.com/kitUIN/nonebot-plugin-ncm)，感谢。
  - nonebot_plugin_ncm 已不再维护。
## 更新日志
- 2024.07.04
  - potato_reminder_new 增加午餐播报的菜单功能。
  - ~~尝试修复了 Potato 天天吃沙拉的问题。~~
- 2024.07.23
  - 修正 readme 中对 [nonebot_plugin_fortune](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune) 的 pillow 库版本建议。
  - 添加插件 [nonebot_plugin_sticker_saver](https://github.com/colasama/nonebot-plugin-sticker-saver) 。
- 2024.08.13
  - 添加插件 potato_plugin_ncm 。
- 2024.08.14
  - 修复插件 potato_plugin_ncm 的若干问题。
## ToDo
- [x] 修复 Potato 天天喝热牛奶的问题。
- [ ] 实现每日二次元新闻。~~但是我连 api 都没找到啊😇~~
- [ ] 每日抽签自定义 DLC 。
- [ ] ~~恢复包括对称等表情包功能。~~
- [ ] ~~编写 help 菜单。~~

## 其他
~~面向社区编程跟面向ai编程真是互联网最伟大的发明~~🥰

祝你愉快 :)