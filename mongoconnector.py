import pymongo
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint
import filemanager


mongodb_config = filemanager.load_file('configs/mongodb.json')

client = MongoClient(mongodb_config['ip'], mongodb_config['port'], username=mongodb_config['username'],password=mongodb_config['password'])
db = client.dbexam2019
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