import mongoconnector


def q1(city):
    books = []
    return {
        'data': {} 
    }
    # return {
    #     'data': [
    #             {'title':'title1', 'authors':['name1','name2']},
    #             {'title':'title2', 'authors':['name1','name2']}
    #     ],
    #     'db_type': 'mongodb'
    # }


def q2(title):
    return {
        'data': {
                'city1':{'lat':15.34, 'lng': 55.4},
                'city2':{'lat':0, 'lng': 55.4}
                },
        'db_type': 'mongodb'
    }

def q3(author):
    return {
        'data': {
            'books': [
                {'title':'title1'},
                {'title':'title2'}
            ],
            'cities': {
                'city1':{'lat':15.34, 'lng': 55.4},
                'city2':{'lat':0, 'lng': 55.4}
            }
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