from nonebot import require, on_command
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import nonebot
from .config import DEBUG, QWEATHER_APIKEY, QWEATHER_APITYPE, Config
from .clock import load_data_from_json, group_add, group_del, report_hour, report_minute
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.permission import SUPERUSER

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler

from nonebot_plugin_alconna import Alconna, Args, UniMessage, on_alconna

from .render_pic import render
from .weather_data import CityNotFoundError, ConfigError, Weather

__plugin_meta__ = PluginMetadata(
    name="和风天气",
    description="和风天气图片显示插件",
    usage="天气地名 / 地名天气",
    type="application",
    homepage="https://github.com/kexue-z/nonebot-plugin-heweather",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)

if DEBUG:
    logger.debug("将会保存图片到 weather.png")

weather = on_alconna(Alconna("/wea", Args["city", str]), block=True, priority=1)
weather.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
weather.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})
wea_add = on_command("wea_group_add", permission=SUPERUSER)
wea_del = on_command("wea_group_delete", permission=SUPERUSER)


@weather.handle()
async def _(matcher: Matcher, city: str):
    if QWEATHER_APIKEY is None or QWEATHER_APITYPE is None:
        raise ConfigError("请设置 qweather_apikey 和 qweather_apitype")

    w_data = Weather(city_name=city, api_key=QWEATHER_APIKEY, api_type=QWEATHER_APITYPE)
    try:
        await w_data.load_data()
    except CityNotFoundError:
        logger.warning(f"找不到城市: {city}")
        matcher.block = False
        await matcher.finish()

    img = await render(w_data)

    if DEBUG:
        debug_save_img(img)

    await UniMessage.image(raw=img).send()


@wea_add.handle()
async def _(event: GroupMessageEvent, arg=CommandArg()):
    gid: str = str(event.group_id)
    city: str = str(arg)
    group_add(gid, city)
    text = '添加天气播报\n群：' + gid + ' 城市：' + city
    msg = MessageSegment.text(text)
    await wea_add.finish(msg)


@wea_del.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    group_del(gid)
    text = '删除天气播报\n群：' + gid
    msg = MessageSegment.text(text)
    await wea_del.finish(msg)


def debug_save_img(img: bytes) -> None:
    from io import BytesIO

    from PIL import Image

    logger.debug("保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")


async def clock():
    data = load_data_from_json()
    for gid, city in data.items():
        if QWEATHER_APIKEY is None or QWEATHER_APITYPE is None:
            raise ConfigError("请设置 qweather_apikey 和 qweather_apitype")

        w_data = Weather(city_name=city, api_key=QWEATHER_APIKEY, api_type=QWEATHER_APITYPE)
        try:
            await w_data.load_data()
        except CityNotFoundError:
            logger.warning(f"找不到城市: {city}")

        img = await render(w_data)

        if DEBUG:
            debug_save_img(img)

        msg = MessageSegment.image(img)

        await nonebot.get_bot().call_api("send_msg", group_id=int(gid), message=msg)


scheduler.add_job(clock, "cron", hour=report_hour, minute=report_minute)
