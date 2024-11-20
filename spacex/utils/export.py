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


def zip_folder(folder_to_zip, output_zip_file):
    # 定义要压缩的文件夹路径
    folder_name = os.path.basename(folder_to_zip)
    temp_dir = 'temp/hot'
    os.makedirs(temp_dir, exist_ok=True)

    # 目标目录
    target_dir = os.path.join(temp_dir, folder_name)

    # 检查并删除已存在的目标目录
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    # 复制文件夹
    shutil.copytree(folder_to_zip, target_dir)

    # 压缩临时目录
    shutil.make_archive(output_zip_file.replace('.zip', ''), 'zip', temp_dir)

    # 删除临时目录
    shutil.rmtree(temp_dir)

    print(f'文件夹已成功压缩为 {output_zip_file}')

def zip_files(file_list, output_zip):
    """
    将多个文件压缩到一个ZIP文件中。

    :param file_list: 要压缩的文件列表
    :param output_zip: 输出的ZIP文件路径（不带 .zip 后缀）
    """
    # 检查文件是否存在
    existing_files = [file for file in file_list if os.path.exists(file)]
    if not existing_files:
        print("没有找到任何文件，无法创建ZIP文件。")
        return

    for file in file_list:
        if not os.path.exists(file):
            print(f"警告：文件 {file} 不存在，跳过。")

    # 创建一个临时目录来存放文件
    temp_dir = 'temp_zip_dir'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # 复制文件到临时目录
        for file in existing_files:
            shutil.copy(file, temp_dir)

        # 创建ZIP文件
        shutil.make_archive(output_zip, 'zip', temp_dir)
    finally:
        # 删除临时目录
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    export_hot()
    export_live()
    with open('../live/config/rooms.json', 'r', encoding='utf-8') as f:
        a = f.read()
    with open('../live/cache/rooms.json', 'w', encoding='utf-8') as f:
        f.write(a)
    zip_folder('../live/cache', 'live.zip')
    zip_folder('../hot/cache', 'hot.zip')
    zip_files(['live.zip','hot.zip'],'export')
