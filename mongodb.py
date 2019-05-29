import mongoconnector as mongo_db
import json


def q1(city):
    res = mongo_db.find_books_on_city(city)
    data = []
    for e in res:
        data.append(e)

    return {
        'data': data, 
        'db_type': 'mongodb'
    }


def q2(title):
    res = mongo_db.find_all_cities_in_books(title)
    for e in res:
        data = e['cities']
    return {
        'data': data,
        'db_type': 'mongodb'
    }

def q3(author):
    res = mongo_db.find_books_on_author(author)
    books = []
    cities = {}
    for e in res:
        books.append({'title':e['title']})
        for city in e['cities']:
            print(city)
            if city not in cities:
                cities[city] = e['cities'][city]
    return {
        'data': {
            'books': books,
            'cities': cities
        },
        'db_type': 'mongodb'
    }

def q4(geolocation):
    return {
        'data': [
                {'title':'title1', 'authors':['name1','name2']},
                {'title':'title2', 'authors':['name1','name2']}
        ],
        'db_type': 'mongodb'
    }