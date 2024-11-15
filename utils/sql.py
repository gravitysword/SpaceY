import pymysql
import json
from datetime import datetime
import os


def update_hot(platform, time, data):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='SPACEX',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 插入数据
            sql = f'''INSERT INTO tb_hot (id , platform, time, data) VALUES (NULL , '{platform}', '{time}', '{json.dumps(data, ensure_ascii=False, indent=4)}');'''
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()


def query_hot(platform):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='SPACEX',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 插入数据
            sql = f"SELECT * FROM tb_hot WHERE platform = '{platform}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()



def insert_img(name, uid, img):
    # 连接到数据库
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='SPACEX',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # 插入数据
            query = "INSERT INTO tb_live (id , name,uid, time,img) VALUES (NULL, %s,%s, %s,%s)"
            values = (name, uid, datetime.now(), img)
            cursor.execute(query, values)
            connection.commit()
    finally:
        connection.close()


def query_img(uid):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='SPACEX',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 插入数据
            sql = f"SELECT * FROM tb_live WHERE uid = '{uid}' "
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


# 调用函数
