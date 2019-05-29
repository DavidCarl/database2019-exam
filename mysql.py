import mysqlconnector as sql_db



def q1(city):
    res = sql_db.find_books_on_city(city)
    data = []
    for e in res:
        data.append({'title': e[3], 'authors':[e[4]]})
    return {
        'data': data,
        'db_type': 'mysql'
    }

def q2(title):
    res = sql_db.find_all_cities_in_books(title)
    data = {}
    for e in res:
        data[e[2]] = {'lat': e[3], 'lng': e[4]}
    return {
        'data': data,
        'db_type': 'mysql'
    }

def q3(author):
    res = sql_db.find_books_on_author(author)
    books_unique = []
    books = []
    cities = {}
    for e in res:
        if e[1] not in books_unique:
            books_unique.append(e[1])
            books.append({'title':e[1]})
        if e[2] not in cities:
            cities[e[2]] = {'lat': e[3], 'lng': e[4]}
    return {
        'data': {
            'books': books,
            'cities': cities
        },
        'db_type': 'mysql'
    }

def q4(geolocation):
    res = sql_db.find_books_on_geolocation(geolocation)
    obj = {}
    obj['data'] = []
    for e in res:
        new_obj = {}
        found = False
        for each in obj['data']:
            if e[1] in each['title']:
                found = True
        if found is False:
            new_obj['title'] = e[1]
            obj['data'].append(new_obj)
    return obj