import pymysql
def create_table():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='spacex',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # 插入数据
            sql = f'''CREATE TABLE IF NOT EXISTS tb_live (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
            name VARCHAR(30) COMMENT '平台名称',
            uid VARCHAR(30) COMMENT '房间号',
            time DATETIME COMMENT '时间',
            img LONGBLOB  COMMENT '图片数据');'''
            cursor.execute(sql)

            sql = f'''CREATE TABLE IF NOT EXISTS tb_hot (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键',
            platform VARCHAR(20) COMMENT '平台名称',
            time DATETIME COMMENT '时间', 
            data JSON COMMENT 'JSON 数据');'''
            cursor.execute(sql)
    finally:
        connection.close()
def create_database():
    connection = pymysql.connect(
       host='127.0.0.1',
       user='root',
       password='123456',
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
       # 执行 SQL 语句
       sql = "CREATE DATABASE IF NOT EXISTS SPACEX"
       cursor.execute(sql)

if __name__ == '__main__':
    create_database()
    create_table()