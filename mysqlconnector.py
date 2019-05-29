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

# This could work for question 1
def find_books_on_city(city):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT c.name as CityName, b.id as bookID, b.fileName, b.title as BookTitle, a.name as AuthorName \
                    FROM city c \
                    INNER JOIN city_mentions cm on c.id = cm.city_id \
                    INNER JOIN books b on cm.book_id = b.id \
                    INNER JOIN book_authors ba on b.id = ba.book_id \
                    INNER JOIN author a on ba.author_id = a.id \
                    WHERE c.name = %s;'
            cursor.execute(sql, (city))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 2
def find_all_cities_in_books(title):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT b.id as BookID, b.title as BookTitle, c.name as CityName, c.geolocation \
                    FROM books b \
                    INNER JOIN city_mentions cm on b.id = cm.book_id \
                    INNER JOIN city c on cm.city_id = c.id \
                    WHERE b.title = %s;'
            cursor.execute(sql, (title))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 3
def find_books_on_author(author):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT * \
                    FROM author a \
                    INNER JOIN book_authors ba on a.id = ba.author_id \
                    INNER JOIN books b on ba.book_id = b.id \
                    INNER JOIN city_mentions cm on b.id = cm.book_id \
                    INNER JOIN city c on cm.city_id = c.id \
                    WHERE a.name = %s'
            cursor.execute(sql, (author))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 4
def find_books_on_geolocation(location):
    #TODO
    pass