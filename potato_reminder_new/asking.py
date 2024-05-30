from date import date_info
from AiChat_reminder import spark


# date_error = {'date': '2024年5月32日', 'weekday': '星期九', 'holiday_status': 1, 'holiday_info': '周末'}


def when_weekend(weekday_str):
    weekdays = {
        "星期一": 1,
        "星期二": 2,
        "星期三": 3,
        "星期四": 4,
        "星期五": 5,
        "星期六": 6,
        "星期日": 7
    }
    # 返回对应的数字，如果找不到对应的星期字符串，则返回None
    now = weekdays.get(weekday_str)
    return 6 - now


def get_answer(question):
    answer = spark(question)
    return answer


def morning_question():
    date = date_info()
    is_holiday = date["holiday_status"]
    weekday = date["weekday"]
    day = date["date"]
    if is_holiday:
        holiday_info = date["holiday_info"]
        question = f"今天是{weekday}，是{holiday_info}，请根据这些信息问候早安，表达自己的关心并提出一些假期建议。"
        print(question)
        return question
    else:
        last = when_weekend(weekday)
        question = f"今天是{weekday}，是工作日，距离周末还剩{last}天，请根据这些信息问候早安，表达自己的关心并提出一些工作或学习建议。"
        print(question)
        return question


def noon_question():
    date = date_info()
    is_holiday = date["holiday_status"]
    weekday = date["weekday"]
    day = date["date"]
    if is_holiday:
        holiday_info = date["holiday_info"]
        question = f"今天是{weekday}，是{holiday_info}，请根据这些信息问候午安，表达自己的关心并提出一些午餐建议。"
        print(question)
        return question
    else:
        last = when_weekend(weekday)
        question = f"今天是{weekday}，是工作日，距离周末还剩{last}天，请根据这些信息问候午安，表达自己的关心并提出一些午餐建议。"
        print(question)
        return question


def evening_question():
    date = date_info()
    is_holiday = date["holiday_status"]
    weekday = date["weekday"]
    day = date["date"]
    if is_holiday:
        holiday_info = date["holiday_info"]
        question = f"今天是{weekday}，是{holiday_info}，请根据这些信息问候晚安，表达自己的关心并提出一些睡眠建议。"
        print(question)
        return question
    else:
        last = when_weekend(weekday)
        question = f"今天是{weekday}，是工作日，距离周末还剩{last}天，请根据这些信息问候晚安，表达自己的关心并提出一些睡眠建议。"
        print(question)
        return question


def night_question():
    question = f"痛斥不要熬夜。"
    return question


if __name__ == "__main__":
    question = morning_question()
    noon_question()
    evening_question()
    # get_answer(question)
