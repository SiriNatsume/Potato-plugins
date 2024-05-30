import json

report_hour: int = 18
report_minute: int = 53


def save_data_to_json(data):
    with open("data/potato_news_report/group.json", "w") as json_file:
        json.dump(data, json_file)


def load_data_from_json():
    try:
        with open("data/potato_news_report/group.json", "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []


def group_add(gid):
    data = load_data_from_json()
    if gid not in data:
        data.append(gid)
        save_data_to_json(data)
        return 1
    else:
        pass


def group_del(gid):
    data = load_data_from_json()
    if gid not in data:
        return 0
    else:
        data.remove(gid)
        save_data_to_json(data)
        return 1
