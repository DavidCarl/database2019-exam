

def book_author(id, book_id, fileName):
    sql = f'({id}, {book_id}),\n'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def city_mentions(id, book_id, fileName):
    sql = f'({id}, {book_id}),\n'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def city(city, lat, lon, fileName):
    city = city.replace('`', ' ')
    city = city.replace('\'', ' ')
    sql = f'(\'{city}\', ST_GeomFromText("POINT ({lat} {lon})"))'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def start_file(table, fileName, fields):
    sql = f'INSERT INTO {table} {fields}VALUES '
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def end_file(fileName, parameter):
    sql = ',\n'
    if parameter == 'end':
        sql = ';'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def author(authorName, fileName):
    sql = f'(\'{authorName}\'),\n'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def title(title, book_id, fileName):
    sql = f'UPDATE books SET title = \'{title}\' WHERE id = {book_id};\n'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)