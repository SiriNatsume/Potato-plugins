#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import time
from typing import Union
import nonebot
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import GROUP_ADMIN
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
from .config import Config
from .data_source import (nncm, load_data_from_json, save_data_to_json, get_date, make_music_card, group_add, group_del,
                          load_data_from_json_for_group)
from nonebot.adapters.onebot.v11 import (Message, Bot,
                                         MessageSegment,
                                         GroupMessageEvent,
                                         PrivateMessageEvent,
                                         ActionFailed)

# 触发器
search = on_command("ncm", priority=2, block=False)
delete = on_command('ncm_delete', aliases={'ncm_del'}, priority=2, block=False)
show = on_command('ncm_list', aliases={'ncm_ls'}, priority=2, block=False)
ncm_group_add = on_command('ncm_group_add', priority=2, block=False, permission=SUPERUSER | GROUP_ADMIN)
ncm_group_delete = on_command('ncm_group_delete', aliases={'ncm_group_del'}, priority=2, block=False,
                              permission=SUPERUSER | GROUP_ADMIN)
ncm_test = on_command('ncm_test', priority=2, block=False, permission=SUPERUSER)
scheduler = require("nonebot_plugin_apscheduler").scheduler

# 全局变量
_id: int = 0
nickname: str = 'default'
music_name: str = 'default'
control: bool = True
lock = asyncio.Lock()
pathway: str = Config.ncm_pathway
limit: int = Config.limit - 1
potato_group: int = Config.potato_group
timeout: int = Config.timeout


# 获取曲目信息
@search.handle()
async def search_receive(bot: Bot,
                         event: Union[GroupMessageEvent, PrivateMessageEvent], matcher: Matcher,
                         args: Message = CommandArg()):
    # 白名单
    uid = event.user_id
    gid = event.group_id
    if gid != potato_group:
        await search.finish()

    # 保证会话不并发
    global control
    if not control:
        msg = f'上一会话正在进行，请等待其结束 😊  '
        await search.finish(MessageSegment.text(msg) + MessageSegment.at(uid))

    # 前置识别曲库是否已满
    data = load_data_from_json(pathway)
    if data['count'] > limit:
        date: str = get_date()
        msg = f'\n{date}起{limit + 1}天内播报容量已满，请于今日播报结束后再尝试添加'
        await search.finish(MessageSegment.at(uid) + MessageSegment.text(msg))

    async with lock:
        global nickname
        global _id
        global music_name

        key = args.extract_plain_text()
        # 获取音乐id、推荐人名称
        nickname = event.sender.nickname
        # 直接识别nid
        if key.replace(" ", "").isdigit():
            _id = int(key.replace(" ", ""))
        # 通过音乐名称获取nid
        else:
            _id = await nncm.search_song(keyword=args.extract_plain_text(), limit=1)
        # 不优雅地返回消息
        if not control:
            msg = f'上一会话正在进行，请等待其结束 😊  '
            await search.finish(MessageSegment.text(msg) + MessageSegment.at(uid))

        # 获取音乐名称
        try:
            res = nncm.get_info(_id=_id)
            music_name = res['songs'][0]['name']
        except:
            msg = f'\napi 回应查询失败，请稍后再试'
            await search.finish(MessageSegment.at(uid) + MessageSegment.text(msg))

        # 上锁
        control = False
        msg = f"\n识别音乐id为{_id}"
        await bot.send(event=event, message=Message(MessageSegment.at(uid) + MessageSegment.text(msg)))

        try:
            # 尝试发送卡片
            try:
                # 尝试生成自定义卡片
                music_card = make_music_card(_id, nickname)
                await bot.send(event=event, message=Message(music_card))
            except ActionFailed:
                # 失败后生成网易云卡片
                await bot.send(event=event, message=Message(MessageSegment.music(type_="163", id_=_id)))
            # 启动超时检查
            asyncio.create_task(timeout_handler(matcher, uid))
        except:
            # 失败后重置进程锁，并返回错误信息
            msg = f'音乐卡片发送超时，请稍后重试'
            control = True
            await search.finish(MessageSegment.text(msg))


# 确认并保存曲目信息
@search.got("confirm", prompt="请确认识别是否正确\n1: 正确；0: 错误\n确认后该曲目将被加入播报")
async def receive_song(bot: Bot, matcher: Matcher,
                       event: Union[GroupMessageEvent, PrivateMessageEvent],
                       confirm: str = ArgPlainText()
                       ):
    global _id
    global pathway
    global control
    uid = event.user_id

    async with lock:

        msg = f'参数获取失败'
        if confirm == '1':
            msg = write_music_list()
        elif confirm == '0':
            msg = f'已终止添加，为获取精准结果，请直接搜索音乐id'
        else:
            await search.reject(f'参数不合法，请重新输入')

        # 解锁进程
        control = True

        await asyncio.gather(search.finish(MessageSegment.text(msg)))


@delete.handle()
async def _(event: Union[GroupMessageEvent, PrivateMessageEvent], args: Message = CommandArg()):
    key = args.extract_plain_text()
    uid = event.user_id

    # 白名单
    gid = event.group_id
    if gid != potato_group:
        await delete.finish()

    # 全部删除
    if key == 'all':
        data = load_data_from_json(pathway)
        already_broadcast = data['already_broadcast']
        res = {'count': 0, 'already_broadcast': already_broadcast, 'blank': '114514'}
        save_data_to_json(res, pathway)
        msg = f'\n曲库已全部清除'
        m = MessageSegment.at(uid) + MessageSegment.text(msg)
        await delete.finish(m)

    # 加载并删除对应曲目
    data = load_data_from_json(pathway)
    _ = {'count': 0, 'already_broadcast': False, 'blank': '114514'}
    if key not in _:
        try:
            del data[key]
            data['count'] -= 1
            data['blank'] = key
            msg = f'\n{key}的曲目已被删除'
            save_data_to_json(data, pathway)
        except:
            msg = f'\n参数“{key}”对应日期无曲目或不正确'
    else:
        msg = f'\n参数“{key}”对应日期无曲目或不正确'
    m = MessageSegment.at(uid) + MessageSegment.text(msg)
    await delete.finish(m)


# 曲库查询
@show.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    key = args.extract_plain_text()
    data = load_data_from_json(pathway)
    msg = None

    # 白名单
    gid = event.group_id
    if gid != potato_group:
        await show.finish()

    # 处理曲库为空时的逻辑
    if data['count'] == 0:
        msg = f'当前曲库为空'
        await show.finish(MessageSegment.text(msg))

    # 处理指定某日查询的操作逻辑
    if key in data:
        user = data[key]['user']
        nid = data[key]['id']
        try:
            # 尝试发送卡片
            try:
                # 尝试生成自定义卡片
                music_card = make_music_card(nid, user)
                await show.finish(music_card)
            except ActionFailed:
                # 失败后生成网易云卡片
                await show.finish(MessageSegment.music(type_="163", id_=nid))
        except ActionFailed:
            # 失败后返回错误信息
            msg = f'音乐卡片发送超时，请稍后重试'
            await search.finish(MessageSegment.text(msg))

    # 处理一般查询的逻辑
    else:
        exclude_key = 'count'
        m: str = ''
        _ = {'count': 0, 'already_broadcast': False, 'blank': '114514'}
        for key in data:
            if key not in _:
                name = data[key]['name']
                m += f'{key}:\n{name}\n\n'
        msg = MessageSegment.text(m.rstrip('\n\n'))

    await show.finish(msg)


# 增删群组列表
@ncm_group_add.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    if group_add(gid):
        msg = f'群{gid}\n已开启音乐播报'
    else:
        msg = f'发生未知错误'
    await ncm_group_add.finish(MessageSegment.text(msg))


@ncm_group_delete.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    if group_del(gid):
        msg = f'群{gid}\n已关闭音乐播报'
    else:
        msg = f'群{gid}不存在或发生错误'
    await ncm_group_delete.finish(MessageSegment.text(msg))


# 测试
@ncm_test.handle()
async def _(event: GroupMessageEvent, args=CommandArg()):
    # 白名单
    key = args.extract_plain_text()
    gid = event.group_id
    if gid != potato_group:
        await ncm_test.finish()

    functions = {
        "notice": notice,
        "broadcast": broadcast,
        "reset": reset
    }
    selected_function = functions.get(str(key))
    await selected_function()
    ncm_test.finish()


# 写入曲库
def write_music_list():
    global _id
    global nickname
    global music_name

    data = load_data_from_json(pathway)
    if data['count'] <= limit:
        # 查重
        exclude_key = 'count'
        _ = {'count': 0, 'already_broadcast': False, 'blank': '114514'}
        for key in data:
            if key not in _:
                if data[key]['id'] == _id:
                    msg = f'id为{_id}的曲目在最近{limit + 1}天内已经存在，换一首试试吧'
                    return msg
                if data[key]['user'] == nickname:
                    msg = f'{nickname}在曲库中已经添加过一首歌了，请等待其播报或主动删除'
                    return msg

        # 获取目标日期
        date: str = get_date(data['count'])

        # 检查非 count 空白项
        if data['blank'] != '114514':
            date: str = data['blank']
            data['blank'] = '114514'

        song = {'user': nickname, 'id': _id, 'name': music_name}
        data[date] = song
        data['count'] += 1
        save_data_to_json(data, pathway)
        msg = f'id为{_id}的曲目已加入{date}的晚间播报'
        return msg
    # 达到上限
    # if data['count'] > limit:
    #     date: str = get_date()
    #     msg = f'{date}起三天内播报容量已满，请于今日播报结束后再尝试添加'
    #     return msg


# 定时解锁进程
async def timeout_handler(matcher, uid):
    global control
    global timeout

    # if not control:
    #     # 等待
    #     await asyncio.sleep(timeout)
    #     # 解锁进程
    #     control = True
    #     # 上报超时信息
    #     msg = f'\n会话超时，请重新尝试。'
    #     await matcher.finish(MessageSegment.at(uid) + MessageSegment.text(msg))
    # else:
    #     # 如果会话在规定时间内完成，则取消计时器
    #     await matcher.finish()

    # 等待
    await asyncio.sleep(timeout)
    # 解锁进程
    control = True
    await matcher.finish()


# 当日曲目为空时提醒补充
async def notice():
    global pathway
    data = load_data_from_json(pathway)
    if data['count'] == 0:
        date: str = get_date()
        msg = f'{date}:\n今日推荐曲目暂空，欢迎添加😉'
        m = MessageSegment.text(msg)
        await nonebot.get_bot().call_api("send_msg", group_id=potato_group, message=m)
    else:
        pass


# 定时播报
async def broadcast():
    global pathway
    group_pathway = "data/potato_music_report/group.json"
    data = load_data_from_json(pathway)
    group = load_data_from_json_for_group(group_pathway)
    date = get_date()
    if data['count'] != 0:
        song = data.pop(date)
        data['count'] -= 1
        data['already_broadcast'] = True
        save_data_to_json(data, pathway)
        nid: int = song['id']
        user: str = song['user']
        card = make_music_card(nid, user)
        for gid in group:
            # 尝试发送卡片
            try:
                # 尝试发送自定义卡片
                await nonebot.get_bot().call_api("send_msg", group_id=int(gid), message=card)
            except:
                # 失败后生成并发送网易云卡片
                await nonebot.get_bot().call_api("send_msg", group_id=int(gid),
                                                 message=MessageSegment.music("163", nid))
            # 降低风控风险，并避免一次性向签名服务器发送过多请求
            time.sleep(7)
    else:
        pass


# 重置播报状态
async def reset():
    data = load_data_from_json(pathway)
    data['already_broadcast'] = False
    save_data_to_json(data, pathway)


# 注册定时任务
scheduler.add_job(notice, "cron", hour=Config.ncm_notice_hour, minute=Config.ncm_notice_minute)
scheduler.add_job(broadcast, "cron", hour=Config.ncm_broadcast_hour, minute=Config.ncm_broadcast_minute)
scheduler.add_job(reset, "cron", hour=0, minute=0)
