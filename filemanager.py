from os import listdir
from os.path import isfile, join
import csv
import json


def get_files():
    mypath = 'unzipped'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def city_mentions():
    mypath = 'test'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def city_mentions_sql():
    mypath = 'sql_scripts/generated/mentions/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def load_mentions(path):
    with open('test/' + path, 'r', encoding='utf-8', errors='replace') as f:
        line = f.readline()
        while line:
            try:
                yield line.strip()
            except UnicodeDecodeError:
                print('UnicodeDecodeError: DAFUQ!')
            line = f.readline()

def load_book(path):
    with open('unzipped/' + path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

# def load_book(path):
#     with open('unzipped/' + path, 'r', encoding='utf-8', errors='replace') as f:
#         line = f.readline()
#         while line:
#             try:
#                 yield line.strip()
#             except UnicodeDecodeError:
#                 print('UnicodeDecodeError: DAFUQ!')
#             line = f.readline()

def load_countries():
    countries = {}
    with open('correct.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        lineNumber = 0
        for row in csv_reader:
            if row[8] not in countries and lineNumber != 0:
                countries[row[8]] = {'cities': []}
            elif lineNumber != 0 and row[2] is not "":
                data = countries[row[8]]
                new_list = {}
                new_list['city'] = row[2]
                new_list['lat'] = row[4]
                new_list['long'] = row[5]
                data['cities'].append(new_list)
                # 4 is lat, 5 is long
                
            lineNumber += 1
    save_file(json.dumps(countries), 'countries_city.json')

# def gelocation_data():


def save_file(data, path):
    print('Saving data into file', path)
    with open(path, 'w') as f:
        f.write(data)
    print('Done saving data into file', path)

def load_file(path):
    print('Loading data from file', path)
    with open(path, 'r') as f:
        return json.loads(f.read())