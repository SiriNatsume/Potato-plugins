import json


def save_data_to_json(data, pathway):
    with open(pathway, "w") as json_file:
        json.dump(data, json_file)


def load_data_from_json(pathway):
    try:
        with open(pathway, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return []


def group_add(gid):
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    if gid not in data:
        data.append(gid)
        save_data_to_json(data,pathway)
        return 1
    else:
        pass


def group_del(gid):
    pathway = "data/potato_reminder/group.json"
    data = load_data_from_json(pathway)
    if gid not in data:
        return 0
    else:
        data.remove(gid)
        save_data_to_json(data, pathway)
        return 1


def menu_add(text):
    pathway = "data/potato_reminder/menu.json"
    data = load_data_from_json(pathway)
    if text not in data:
        data.append(text)
        save_data_to_json(data, pathway)
        return 1
    else:
        pass


def menu_del(text):
    pathway = "data/potato_reminder/menu.json"
    data = load_data_from_json(pathway)
    if text not in data:
        return 0
    else:
        data.remove(text)
        save_data_to_json(data, pathway)
        return 1
