#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime


def now_day():
    # 获取当前日期
    current_date = datetime.now()

    # 提取年份、月份、日期
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # 格式化日期为 YYYY-M-D
    formatted_current_date = f"{year}-{month}-{day}"
    return formatted_current_date


def request_date():
    date = now_day()
    # 向api请求数据
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "http://v.juhe.cn/calendar/day"
    params = {
        "key": "",  # 在个人中心->我的数据,接口名称上方查看
        "date": date,  # 指定日期,格式为YYYY-MM-DD,如月份和日期小于10,则取个位,如:2012-1-1

    }
    resp = requests.get(url, params, headers=headers)
    resp_json = json.loads(resp.text)
    return resp_json


# 判断节假日
def is_holiday(holiday, weekday):
    if holiday:
        return 1, holiday
    elif weekday in ["星期六", "星期日"]:
        return 1, "周末"
    else:
        return 0, ""


def date_info():
    resp_json = request_date()
    # 获取result里的所有字段
    result_data = resp_json.get("result", {}).get("data", {})

    # 获取需要信息
    date = result_data['date']
    weekday = result_data['weekday']
    holiday = result_data['holiday']

    # 提取year, month, day
    year, month, day = date.split('-')
    # 将year, month, day转换为YY年MM月DD日格式
    formatted_date = f"{year}年{month}月{day}日"

    # 获取节假日信息
    holiday_status, holiday_info = is_holiday(holiday, weekday)

    # 汇总成字典
    day_info = {"date": formatted_date, "weekday": weekday, "holiday_status": holiday_status,
                "holiday_info": holiday_info}

    return day_info


if __name__ == "__main__":
    # 调用函数并获取返回值
    test = date_info()

    # 打印结果
    print(test)
    # print(f"Weekday: {weekday}")
    # print(f"Formatted date: {date}")
    # print(f"Holiday status: {holiday_status}")
    # print(f"Description: {desc}")
