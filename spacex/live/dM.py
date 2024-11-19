import requests,json,threading,time, os

with open('../config/config.json', 'r') as f:
    #bili_cookies = json.load(f)['cookies']['bili'][0]
    pass


def dM(id,name):
    file_path = f'cache/dM/dM_{name}.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w',encoding='utf-8') as f:
            f.write('{}')

    with open(file_path, 'r', encoding='utf-8') as f:
        dM_data = json.load(f)
    url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        #'Cookie': "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in bili_cookies])
    }

    response = requests.get(url, headers=headers)
    datas = response.json()
    for i in datas['data']['admin']:
        ts = str(i["check_info"]["ts"])
        entry = {
            "text": i["text"], "nickname": i["nickname"], "time": i["timeline"], "uid": i["uid"],
            "dm_type": i["dm_type"], "user_level": "admin", "id_str": i["id_str"]
        }
        dM_data[ts] = entry

    for i in datas['data']['room']:
        ts = str(i["check_info"]["ts"])
        entry = {
            "text": i["text"], "nickname": i["nickname"], "time": i["timeline"], "uid": i["uid"],
            "dm_type": i["dm_type"], "user_level": "room", "id_str": i["id_str"]
        }
        dM_data[ts] = entry

    with open(f'cache/dM/dM_{name}.json', 'w+', encoding='utf-8') as f:
        data_json = json.dumps(dM_data, ensure_ascii=False, indent=4)
        f.write(data_json)


def get_dM(rooms_id,rooms_name):
    threads = []
    for i in rooms_id:
        t = threading.Thread(target=dM, args=(i,rooms_name[i]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    with open('config/rooms.json', 'r', encoding='utf-8') as f:
        a = json.load(f)['rooms']
    rooms_id = [a[i] for i in a]
    rooms_name = { a[i]: i for i in a }
    while True:
        get_dM(rooms_id,rooms_name)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))} 弹幕更新完成")
        time.sleep(10)
