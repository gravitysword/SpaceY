import json
from datetime import datetime

import sys,os

sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql


def download_img(name, uid):
    os.makedirs(f'../cache/realtime/{name}', exist_ok=True)
    imgs = sql.query_img(uid)
    for i in imgs:
        file_path = f'../cache/realtime/{name}/{i["time"].strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        with open(file_path, 'wb') as f:
            f.write(i['img'])


def create():
    with open('../config/rooms.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    name = config['rooms']
    for i in name:
        download_img(i, name[i])


if __name__ == '__main__':
    create()
