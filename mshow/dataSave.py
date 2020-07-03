import os
import json


def saveJsonFile(path, data):
    with open(path, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def loadJsonFile(path):
    global json_data
    if not os.path.exists(path):
        return {}

    try:
        with open(path, encoding='utf-8') as fh:
            json_data = json.load(fh)
    except Exception as ex:
        print(path)
        print(ex)
    return json_data
