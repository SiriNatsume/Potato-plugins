import requests
from .config import Config
from nonebot import require, on_command
from nonebot.permission import SUPERUSER
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from .clock import load_data_from_json, group_add, group_del, report_hour, report_minute

# global_config = nonebot.get_driver().config
# nonebot.logger.info("global_config:{}".format(global_config))
# plugin_config = Config(**global_config.dict())
# nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler

news_add = on_command("news_group_add", permission=SUPERUSER)
news_del = on_command("news_group_delete", permission=SUPERUSER)


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())  # 去除imageUrl可能存在的不可见字符


async def read60s():
    msg = await suijitu()
    data = load_data_from_json()
    for qq_group in data:
        await nonebot.get_bot().call_api("send_msg", group_id=int(qq_group), message=msg)  # MessageEvent可以使用CQ发图片


async def suijitu():
    try:
        url = "https://api.2xb.cn/zaob"  # 备用网址
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        r = requests.get(lst, verify=False)
        with open("temp.jpeg", "wb") as f:
            f.write(r.content)
        msg = MessageSegment.text("今日份新闻") + MessageSegment.image("file:///home/ubuntu/test/temp.jpeg")
        return msg

    except:
        url = "https://api.iyk0.com/60s"
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        r = requests.get(lst)
        with open("temp.jpeg", "wb") as f:
            f.write(r.content)
        msg = MessageSegment.text("今日份新闻") + MessageSegment.image("file:///home/ubuntu/test/temp.jpeg")
        return msg


@news_add.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    group_add(gid)
    text = '添加新闻播报\n群：' + gid
    msg = MessageSegment.text(text)
    await news_add.finish(msg)


@news_del.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    group_del(gid)
    text = '删除新闻播报\n群：' + gid
    msg = MessageSegment.text(text)
    await news_del.finish(msg)


scheduler.add_job(read60s, "cron", hour=report_hour, minute=report_minute)

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='60s读世界',
    description='早八新闻播报',
    usage='如有需要可联系管理员开启'
)

if __name__ == "__main__":
    suijitu()
