from utils.u import *
import json
import requests
from lxml import etree
import time
import datetime
import threading


with open(root_path + '/config/config.json', 'r') as f:
    bili_cookies = json.load(f)['cookies']['bili']

def status(id,name):
    url = f'https://live.bilibili.com/{id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Cookie': "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in bili_cookies])
    }
    response = requests.get(url, headers=headers).text

    parser = etree.HTMLParser()
    tree = etree.fromstring(response, parser)
    script = tree.findall('.//script')

    data_json = ""
    for p in script:
        if 'window.__NEPTUNE_IS_MY_WAIFU__={' in str(p.text):
            data_json = str(p.text).replace('window.__NEPTUNE_IS_MY_WAIFU__=', '').replace('<script>', '')
    datas_init = json.loads(data_json)["roomInitRes"]["data"]
    if datas_init["playurl_info"] :
        playurl_info = "Already Exists"
    else:
        playurl_info = "Not Exist"

    b = {
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"): {
            "room_id": datas_init["room_id"],
            "short_id": datas_init["short_id"],
            "is_hidden": datas_init["is_hidden"],
            "is_locked": datas_init["is_locked"],
            "is_portrait": datas_init["is_portrait"],
            "live_status": datas_init["live_status"],
            "hidden_till": datas_init["hidden_till"],
            "lock_till":   datas_init["lock_till"],
            "encrypted": datas_init["encrypted"],
            "pwd_verified": datas_init["pwd_verified"],
            "live_time": datas_init["live_time"],
            "room_shield": datas_init["room_shield"],
            "all_special_types": datas_init["all_special_types"],
            "playurl_info":  playurl_info,
            "official_type": datas_init["official_type"],
            "official_room_id": datas_init["official_room_id"],
            "risk_with_delay": datas_init["risk_with_delay"],
            "multi_screen_info": datas_init["multi_screen_info"],
        }
    }
    d  = open_file(root_path + f'live/cache/status/status_{name}.json')
    d.update(b)
    with open(root_path + f'live/cache/status/status_{name}.json', 'w') as f:
        json.dump(d, f, indent=4,ensure_ascii=False)



def get_status(rooms_id,rooms_name):


    threads = []
    for i in rooms_id:
        t = threading.Thread(target=status, args=(i,rooms_name[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    with open(root_path + f'live/config/rooms.json', 'r', encoding='utf-8') as f:
        a = json.load(f)['rooms']
    rooms_id = [a[i] for i in a]
    rooms_name = {a[i]: i for i in a}
    while True:
        get_status(rooms_id,rooms_name)
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} 直播间状态更新完成')
        time.sleep(5)
        with open(root_path + f'live/config/live', 'r', encoding='utf-8') as f:
            if f.read() == "0":
                break
