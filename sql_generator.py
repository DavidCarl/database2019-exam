

# INSERT INTO city_mentions VALUES 
def city_mentions(id, book_id, fileName):
    sql = f'({id}, {book_id}),\n'
    with open(f'sql_scripts/generated/{fileName}.sql', 'a+') as sql_file:
        sql_file.write(sql)

def city(city, lat, lon, fileName):
    # ST_GeomFromText("POINT (42.98339	-81.23304)")
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