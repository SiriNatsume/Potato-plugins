# Potato-plugins
## 前言
Potato的一些插件，适用于onebot11，部分也适配red、satori，~~我也不知道我之前写的什么东西。~~
## 插件列表
- **potato_heweather_report**
  - 需要onebot v11协议适配器，原插件可多协议适配。
  - 实现定时的天气播报及查询，可以分群开关并配置查询城市，使用[和风天气api](https://console.qweather.com/)。
  - 修改自插件[nonebot-plugin-heweather](https://github.com/kexue-z/nonebot-plugin-heweather)，加入了定时播报功能，感谢大佬的轮子。
- **potato_reminder_new**
  - 需要onebot v11协议适配器，但可快速更改为red。
  - 实现对当天节假日信息的获取，并将信息组织成问句向[Spark](https://www.xfyun.cn/)模型获取回答，感谢讯飞的巨量免费tokens.
  - 实现午餐播报的餐单添加。
- **[nonebot_plugin_fortune](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)**
  - 需要onebot v11协议适配器。
  - 实现简单的抽签，并保证每日只能抽一次。
  - 使用时请确认环境pillow库版本小于9.5.0，否则将出现无任何日志报错。
  - 原插件已不再维护。
- **potato_read_60s**
  - 需要onebot v11协议适配器，但可快速更改为red。
  - 实现每日定时的新闻播报，实现开启群组的动态添加。
  - 源api有时不稳定，使用时请注意及时更新缓存图的绝对路径。
  - 修改自更加古早版本的[nonebot-plugin-60s](https://github.com/techotaku39/nonebot-plugin-60s)，感谢大佬的轮子。
  - 原插件已不再维护。
## 其他
~~面向社区编程跟面向ai编程真是互联网最伟大的发明~~🥰

祝你愉快 :)