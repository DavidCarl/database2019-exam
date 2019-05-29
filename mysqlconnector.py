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
    db = connect()
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `books` (`fileName`, `title`, `content`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (fileName, title, content))
        db.commit()
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
            sql = "SELECT id, fileName, title FROM books"
            cursor.execute(sql)
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

def get_mongoDB_obj_from_id(book_id):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = 'SELECT b.id, b.fileName, b.title, a.name as authorName, c.name as cityName, ST_Latitude(geolocation) as Lat, ST_Longitude(geolocation) as Lng \
                    FROM books b \
                    INNER JOIN book_authors ba on b.id = ba.book_id \
                    INNER JOIN city_mentions cm on b.id = cm.book_id \
                    INNER JOIN city c on cm.city_id = c.id \
                    INNER JOIN author a on ba.author_id = a.id \
                    WHERE b.id = %s'
            cursor.execute(sql, (book_id))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

def get_all_id_author():
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = "SELECT id, name FROM author"
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
        return result

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
            sql = 'SELECT b.id as BookID, b.title as BookTitle, c.name as CityName, ST_Latitude(geolocation) as Latitude, ST_Longitude(geolocation) as Longitude \
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
            sql = 'SELECT a.name, b.title, c.name, ST_Latitude(c.geolocation) as Latitude, ST_Longitude(c.geolocation) as Longitude \
                    FROM author a \
                    INNER JOIN book_authors ba on a.id = ba.author_id \
                    INNER JOIN books b on ba.book_id = b.id \
                    INNER JOIN city_mentions cm on b.id = cm.book_id \
                    INNER JOIN city c on cm.city_id = c.id \
                    WHERE a.name = %s;'
            cursor.execute(sql, (author))
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result

# Question 4
def find_books_on_geolocation(location):
    db = connect()
    ids = None
    idlist = ''
    try:
        with db.cursor() as cursor:
            sql = 'WITH vicinity as (select ST_GeomFromText(ST_ASTEXT(ST_Buffer(ST_GeomFromText("POINT (%s %s)", 0), 0.1)), 4326) as area) \
                   SELECT city.name, city.id \
                   FROM vicinity, city \
                   WHERE ST_WITHIN(city.geolocation, vicinity.area);'
            cursor.execute(sql, (location['lat'], location['lng']))
            ids = cursor.fetchall()
        size = len(ids)
        loop = 1
        for e in ids:
            idlist += str(e[1])
            if loop != size:
                idlist += ','
            loop += 1
        db.commit()
    finally:
        db.close()
        return q4_helper(idlist)
 
def q4_helper(id_list):
    db = connect()
    result = None
    try:
        with db.cursor() as cursor:
            sql = f'SELECT b.id, b.title, c.name \
                   FROM books b \
                   INNER JOIN city_mentions cm ON b.id = cm.book_id \
                   INNER JOIN city c ON cm.city_id = c.id \
                   WHERE c.id IN ({id_list}) AND b.title != \'\';'
            cursor.execute(sql)
            result = cursor.fetchall()
        db.commit()
    finally:
        db.close()
        return result