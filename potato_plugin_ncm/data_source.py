#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime, timedelta
from nonebot.log import logger
from pyncm import apis
from pyncm.apis.cloudsearch import SONG
from pyncm.apis.login import LoginViaAnonymousAccount
from nonebot.adapters.onebot.v11 import MessageSegment
from .config import Config


# 网易云 api 方法
class Ncm:
    def __init__(self):
        self.api = apis

    async def search_song(self, keyword: str, limit: int = 1) -> int:  # 搜索歌曲
        res = self.api.cloudsearch.GetSearchResult(keyword=keyword, stype=SONG, limit=limit)
        logger.debug(f"搜索歌曲{keyword},返回结果:{res}")
        if "result" in res.keys():
            data = res["result"]["songs"]
        else:
            data = res["songs"]
        if data:
            return data[0]["id"]

    def get_info(self, _id: int):
        res1 = self.api.track.GetTrackDetail(_id)
        return res1

    def get_song(self, _id: int):
        LoginViaAnonymousAccount()
        res2 = self.api.track.GetTrackAudio(_id)
        return res2


nncm = Ncm()


# 其他方法
def save_data_to_json(data, pathway):
    with open(pathway, "w") as json_file:
        json.dump(data, json_file)


def load_data_from_json(pathway):
    try:
        with open(pathway, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {'count': 0, 'already_broadcast': False, 'blank': '114514'}


def load_data_from_json_for_group(pathway):
    try:
        with open(pathway, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []


# 已建设的曲库收集区域
def load_data_from_json_for_list(pathway):
    try:
        with open(pathway, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {'count': 0}


# cd 的 load 函数
def load_data_from_json_for_cd(pathway):
    try:
        with open(pathway, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {}


def group_add(gid):
    pathway = "data/potato_music_report/group.json"
    data = load_data_from_json_for_group(pathway)
    if gid not in data:
        data.append(gid)
        save_data_to_json(data, pathway)
        return 1
    else:
        pass


def group_del(gid):
    pathway = "data/potato_music_report/group.json"
    data = load_data_from_json_for_group(pathway)
    if gid not in data:
        return 0
    else:
        data.remove(gid)
        save_data_to_json(data, pathway)
        return 1


def get_date(count=0):
    # 获取当前播报状态
    data = load_data_from_json('data/potato_music_report/music.json')
    if data['already_broadcast']:
        count += 1
    # 获取当前日期
    current_date = datetime.now()
    # 计算目标日期
    target_date = current_date + timedelta(days=count)
    # 格式化日期为 "几月-几号"
    formatted_date = target_date.strftime("%m-%d")
    return formatted_date


def make_music_card(nid, user):
    # 获取各种信息
    _res = nncm.get_info(_id=nid)
    _res2 = nncm.get_song(_id=nid)
    _name = _res['songs'][0]['name']
    _ar = _res['songs'][0]['ar'][0]['name']
    _picurl = _res['songs'][0]['al']['picUrl']
    _audio = _res2['data'][0]['url']
    _head = 'https://music.163.com/song?id='
    # _id = res2['data'][0]['id']
    _url = f'{_head}{nid}'
    # 根据名称长度生成不同样式的content
    length = len(user)
    if length <= 4:
        content = f'Recommended by {user}'
    else:
        content = f'{user} recommends'

    # 生成卡片
    msg = MessageSegment("music", {"type": "custom", "url": _url, "audio": _audio, "voice": _audio,
                                   "title": _name, "content": content, "image": _picurl})
    # msg = {
    #     "type": "music",
    #     "data": {
    #         "type": "custom",
    #         "url": _url,
    #         "audio": _audio,
    #         "title": _name,
    #         "content": content,
    #         "image": _picurl
    #     }
    # }
    # m = MessageSegment('music', msg)
    return msg


# cd相关函数
cd_use = Config.cd
cd_pathway = 'data/potato_music_report/cd.json'
# 初始化时间戳,初始化为开机时间 - cd时间
init_last_notice_response = time.time() - cd_use

# cd 检查函数
def cd_check(group_id, cd_time=cd_use):
    data = load_data_from_json_for_cd(cd_pathway)
    if group_id not in data:
        data[group_id] = init_last_notice_response
        save_data_to_json(data, cd_pathway)
        return 1
    else:
        return time.time() - data[group_id] > cd_time


# cd 响应函数
def cd_response(group_id):
    data = load_data_from_json_for_cd(cd_pathway)
    data[group_id] = time.time()
    save_data_to_json(data, cd_pathway)


# cd 重置函数
def cd_reset(group_id):
    data = load_data_from_json_for_cd(cd_pathway)
    data = data.pop(group_id)
    save_data_to_json(data, cd_pathway)


if __name__ == '__main__':
    res = nncm.get_info(_id=2154054722)
    res2 = nncm.get_song(_id=2154054722)
    name = res['songs'][0]['name']
    ar = res['songs'][0]['ar'][0]['name']
    picurl = res['songs'][0]['al']['picUrl']
    audio = res2['data'][0]['url']
    head = 'https://music.163.com/song?id='
    _id = res2['data'][0]['id']
    url = f'{head}{_id}'
    print(audio)
    print(url)
    print(picurl)
    print(ar)
    print(name)
    print(res)
    print(res2)
