import pymongo
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint
import mysqlconnector as sql_db
import filemanager


mongodb_config = filemanager.load_file('configs/mongodb.json')

client = MongoClient(mongodb_config['ip'], mongodb_config['port'], username=mongodb_config['username'],password=mongodb_config['password'])
db = client.dbexam2019
# db.books.drop() #for testing 
books = db.books


class Book():
    def __init__(self, book_id, title, filename, authors, cities):
        self.id = book_id
        self.title = title
        self.file = filename
        self.authors = authors
        self.cities = cities
    
    def get(self):
        return {'_id': self.id, 'title': self.title, 'file':self.file, 'authors':self.authors, 'cities': self.cities}



# Question 1
def find_books_on_city(city):
    result = None
    try:
        result = books.find({f'cities.{city}': {'$exists': True}},{'_id':0, 'title':1, 'authors':1})
    finally:
        return result

# Question 2
def find_all_cities_in_books(title):
    result = None
    try:
        result = books.find({'title': title},{'_id':0, 'cities': 1})        
    finally:
        return result

# Question 3
def find_books_on_author(author):
    result = None
    try:
        result = books.find({f'authors': author},{'_id':0, 'title':1, 'cities':1})        
    finally:
        return result

# Question 4
def find_books_on_geolocation(location):
    #TODO
    pass
    # result = None
    # try:
    #     result = books.find({f'cities.*.lat': location['lat']},{'_id':0, 'title':1, 'cities':1})        
    # finally:
    #     return result


def migrate_mysql_to_mongo():
    all_book_id = sql_db.get_all_book_ids()
    for each in all_book_id:
        bookInfo = sql_db.get_mongoDB_obj_from_id(each[0])
        book_id = None
        title = None
        fileName = None
        authors = []
        cities = {}
        if bookInfo is not ():
            book_id = bookInfo[0][0]
            fileName = bookInfo[0][1]
            title = bookInfo[0][2]
            for row in bookInfo:
                if bookInfo[0][3] not in authors:
                    authors.append(row[3])
                cities[row[4].replace(',', '')] = {"lat": row[5], "lng": row[6]}
            newBook = Book(book_id, title, fileName, authors, cities)
            books.insert_one(newBook.get())

migrate_mysql_to_mongo()

# test = books.find({})
# for e in test:
#     pprint(e)

# b = Book(44,'sometitle','2123.txt',['auth1','auth2'],{'city1':{'lat':0.5,'lng':44.4},'city2':{'lat':5.5,'lng':48.4}})
# b2 = Book(45,'someothertitle','212443.txt',['auth1','auth2'],{'city1':{'lat':0.5,'lng':44.4},'city2':{'lat':5.5,'lng':48.4}})

# books.insert_one(b.get())
# books.insert_one(b2.get())

# res = find_books_on_geolocation({'lat':0.5,'lng':44.4})
# for e in res:
#     pprint(e)