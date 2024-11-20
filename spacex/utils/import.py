
import os
import subprocess
import glob
import json
import sys,os
sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql

def import_hot():
    command = [
        'Get-Content',
            'hot/cache/hot.sql','|',
            'mysql','-u','-root'
            '-p','spacex'
          ]

    env = os.environ.copy()
    env['MYSQL_PWD'] = '123456'

        # 执行 mysqldump 命令
    with open('../hot/cache/hot.sql', 'w+') as f:
        subprocess.run(command, check=True, stdout=f, env=env)

def import_live():
    directory = '../live/cache/realtime/'
    with open('../live/cache/rooms.json', 'r', encoding='utf-8') as f:
        config = json.load(f)["rooms"]
    for name in os.listdir(directory):
        for file in os.listdir(directory+name):
            time = file.split('.')[0]
            img = open(directory+name+'/'+file,'rb').read()
            sql.insert_img(name,config[name],img,time = time)

if __name__ == '__main__':
    import_hot()
    import_live()



