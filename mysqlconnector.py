import pymysql
import json
import filemanager


mysql_config = filemanager.load_file('configs/mysql.json')

failed_files = []

def connect():
    return pymysql.connect(host=mysql_config['ip'],
                        port=mysql_config['port'],
                        user=mysql_config['username'],
                        passwd=mysql_config['password'],
                        db=mysql_config['database'])

def insert_book(fileName, title, author, content):
    global failed_files
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `books` (`fileName`, `title`, `author`, `content`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (fileName, title, author, content))
        db.commit()
    except:
        failed_files.append(fileName)
    finally:
        db.close()

def find_books_on_city(city):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = 'SELECT count(*) FROM exam2019.books WHERE MATCH(`content`) AGAINST(%s)'
            cursor.execute(sql, (city))
            result = cursor.fetchone()
            print(result)
        db.commit()
    finally:
        db.close()
def save_failed_files():
    print(failed_files)
    # filemanager.save_file(failed_files, )