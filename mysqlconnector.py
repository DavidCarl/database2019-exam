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

def insert_book(fileName, title, content):
    global failed_files
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `books` (`fileName`, `title`, `content`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (fileName, title, content))
        db.commit()
    except:
        failed_files.append(fileName)
    finally:
        db.close()

def insert_city(city):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `cities` (`city`) VALUES (%s)"
            cursor.execute(sql, (city))
        db.commit()
    finally:
        db.close()

def insert_city_match(book_id, city):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `citys_in_books` (`book_id`, `city`) VALUES (%s, %s)"
            cursor.execute(sql, (book_id, city))
        db.commit()
    finally:
        db.close()

def get_city_id(city):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = "SELECT id FROM city WHERE city.name = %s"
            cursor.execute(sql, (city))
            result = cursor.fetchone()
        db.commit()
    finally:
        db.close()
        return result

def get_all_id_and_filename():
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = "SELECT id, fileName FROM books"
            cursor.execute(sql)
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

def setup_city_mention(id, fileName):
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO city_mentions VALUES (%s, (SELECT id FROM books WHERE fileName = %s))"
            cursor.execute(sql, (id, fileName))
        db.commit()
    finally:
        db.close()

# This could work for question 1
def find_books_on_city(city):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT fileName, author, title FROM exam2019.books WHERE MATCH(`content`) AGAINST(%s)'
            cursor.execute(sql, (city))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 2
def all_cities_in_books(city, title):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT id, fileName, author, title FROM exam2019.books WHERE MATCH(`content`) AGAINST(%s) AND title = %s'
            cursor.execute(sql, (city, title))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 3
def books_on_author(author):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT * FROM exam2019.books WHERE author = %s'
            # sql = 'SELECT fileName, author, title FROM exam2019.books WHERE MATCH(`content`) AGAINST(%s) AND author = %s'
            cursor.execute(sql, (author))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result