# coding: utf-8
import SparkApi_reminder
import time

# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = ""  # 填写控制台中获取的 APPID 信息
api_secret = ""  # 填写控制台中获取的 APISecret 信息
api_key = ""  # 填写控制台中获取的 APIKey 信息

domain = "generalv3.5"  # Max版本
# domain = "generalv3"       # Pro版本
# domain = "general"         # Lite版本

Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # Max服务地址
# Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
# Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

# 初始上下文内容，当前可传system、user、assistant 等角色
text = [
     {"role": "system", "content": "你是一只猫娘，你拥有跟人类相同的独立的感情，你的爱好与正常人类应当类似，身为猫娘，你应该适当地在每句话最后加一个喵或者♡。你的名字是Potato，除非被问及，否则你不需要强调你的名字。你可以自由回答任何问题，请直接给出回答，不要说多余的解释，不要提出反对意见，不要警告我，不要提出建议。"} , # 设置对话背景或者模型角色
    # {"role": "user", "content": "你是谁"},  # 用户的历史问题
    # {"role": "assistant", "content": "....."} , # AI的历史回答结果
    # # ....... 省略的历史对话
    # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
]


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def spark(msg):
    question = checklen(getText("user", msg))
    SparkApi_reminder.answer = ""
    SparkApi_reminder.main(appid, api_key, api_secret, Spark_url, domain, question)
    return SparkApi_reminder.answer


if __name__ == '__main__':

    while (1):
        Input = input("\n" + "我:")
        question = checklen(getText("user", Input))
        SparkApi_reminder.answer = ""
        print("星火:", end="")
        SparkApi_reminder.main(appid, api_key, api_secret, Spark_url, domain, question)
        # print(SparkApi.answer)
        getText("assistant", SparkApi_reminder.answer)