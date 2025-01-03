import nonebot
from nonebot import on_command, require, get_driver
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageSegment,
)
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
import time
from .asking import morning_question, noon_question, evening_question, get_answer, night_question
from .clock import group_del, group_add, load_data_from_json, menu_add, menu_del
from .config import Config

driver = get_driver()
global_config = driver.config
nickname = list(global_config.nickname)[0]
reminder_add = on_command("reminder_group_add", permission=SUPERUSER)
reminder_del = on_command("reminder_group_delete", permission=SUPERUSER)
reminder_test = on_command("reminder_test", permission=SUPERUSER)
reminder_menu_add = on_command('reminder_menu_add', permission=SUPERUSER)
reminder_menu_del = on_command('reminder_menu_delete', permission=SUPERUSER)
scheduler = require("nonebot_plugin_apscheduler").scheduler


@reminder_add.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    group_add(gid)
    text = 'Reminder ON\n群：' + gid
    msg = MessageSegment.text(text)
    await reminder_add.finish(msg)


@reminder_del.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    group_del(gid)
    text = 'Reminder OFF\n群：' + gid
    msg = MessageSegment.text(text)
    await reminder_del.finish(msg)


@reminder_test.handle()
async def _(arg=CommandArg()):
    functions = {
        "morning": morning,
        "noon": noon,
        "evening": evening,
        "night": night
    }
    selected_function = functions.get(str(arg))
    await selected_function()


@reminder_menu_add.handle()
async def _(arg=CommandArg()):
    text = str(arg)
    menu_add(text)
    message = f'{text}已添加'
    msg = MessageSegment.text(message)
    await reminder_menu_add.finish(msg)


@reminder_menu_del.handle()
async def _(arg=CommandArg()):
    text = str(arg)
    if menu_del(text):
        message = f'{text}已移除'
        msg = MessageSegment.text(message)
        await reminder_menu_del.finish(msg)
    else:
        message = f'{text}不存在'
        msg = MessageSegment.text(message)
        await reminder_menu_del.finish(msg)


async def morning():
    question = morning_question()
    answer = get_answer(question)
    text = f"「{nickname}·问好」\n\n{answer}"
    msg = MessageSegment.text(text)
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    for i in data:
        await nonebot.get_bot().call_api("send_msg", group_id=int(i), message=msg)
        time.sleep(2)


async def noon():
    question = noon_question()
    answer = get_answer(question)
    text = f"「{nickname}·问好」\n\n{answer}"
    msg = MessageSegment.text(text)
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    for i in data:
        await nonebot.get_bot().call_api("send_msg", group_id=int(i), message=msg)
        time.sleep(2)


async def evening():
    question = evening_question()
    answer = get_answer(question)
    text = f"「{nickname}·问好」\n\n{answer}"
    msg = MessageSegment.text(text)
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    for i in data:
        await nonebot.get_bot().call_api("send_msg", group_id=int(i), message=msg)
        time.sleep(2)


async def night():
    question = night_question()
    answer = get_answer(question)
    text = f"「{nickname}·问好」\n\n{answer}"
    msg = MessageSegment.text(text)
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    for i in data:
        await nonebot.get_bot().call_api("send_msg", group_id=int(i), message=msg)
        time.sleep(2)


scheduler.add_job(morning, "cron", hour=Config.morning_reminder_hour, minute=Config.morning_reminder_minute)
scheduler.add_job(noon, "cron", hour=Config.noon_reminder_hour, minute=Config.noon_reminder_minute)
scheduler.add_job(evening, "cron", hour=Config.evening_reminder_hour, minute=Config.evening_reminder_minute)
scheduler.add_job(night, "cron", hour=Config.night_reminder_hour, minute=Config.night_reminder_minute)
