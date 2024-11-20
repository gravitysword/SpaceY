import json
from datetime import datetime
import shutil

import sys, os

sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql

import subprocess


def download_img(name, uid):
    os.makedirs(f'../live/cache/realtime/{name}', exist_ok=True)
    imgs = sql.query_img(uid)
    for i in imgs:
        file_path = f'../live/cache/realtime/{name}/{i["time"].strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        with open(file_path, 'wb') as f:
            f.write(i['img'])


def export_live():
    with open('../live/config/rooms.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    name = config['rooms']
    for i in name:
        download_img(i, name[i])


def export_hot():
    try:
        # 定义 mysqldump 命令
        command = [
            'mysqldump',
            '-u', 'root',
            '--default-character-set=utf8mb4',
            'spacex',
            'tb_hot'
        ]

        # 设置环境变量
        env = os.environ.copy()
        env['MYSQL_PWD'] = '123456'

        # 执行 mysqldump 命令
        with open('../hot/cache/hot.sql', 'w+') as f:
            subprocess.run(command, check=True, stdout=f, env=env)

        print("数据库导出成功")

    except subprocess.CalledProcessError as e:
        print(f"数据库导出失败: {e}")

    except Exception as e:
        print(f"发生错误: {e}")


def zip():
    # 定义要压缩的文件夹路径
    folders_to_zip = [
        '../live/cache/',
        '../hot/cache/'
    ]
    output_zip_file = 'export.zip'

    temp_dir = 'temp/'
    os.makedirs(temp_dir, exist_ok=True)

    for folder in folders_to_zip:
        folder_name = os.path.basename(folder)
        target_dir = os.path.join(temp_dir, folder_name)

        # 检查并删除已存在的目标目录
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        # 复制文件夹
        shutil.copytree(folder, target_dir)

    # 压缩临时目录
    shutil.make_archive(output_zip_file.replace('.zip', ''), 'zip', temp_dir)

    # 删除临时目录
    shutil.rmtree(temp_dir)

    print(f'文件夹已成功压缩为 {output_zip_file}')

if __name__ == '__main__':
    export_hot()
    export_live()
    with open('../live/config/rooms.json', 'r', encoding='utf-8') as f:
        a = f.read()
    with open('../live/cache/rooms.json', 'w', encoding='utf-8') as f:
        f.write(a)
    zip()
