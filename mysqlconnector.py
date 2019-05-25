import pymysql
import json
import filemanager


mysql_config = filemanager.load_file('configs/mysql.json')

def connect():
    return pymysql.connect(host=mysql_config['ip'],
                        port=mysql_config['port'],
                        user=mysql_config['username'],
                        passwd=mysql_config['password'],
                        db=mysql_config['database'])

def insert_book(title, author, content):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `books` (`title`, `author`, `content`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, author, content))
        db.commit()
    finally:
        db.close()