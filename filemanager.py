from os import listdir
from os.path import isfile, join
import csv
import json


def get_files():
    mypath = 'unzipped'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def load_book(path):
    with open('unzipped/' + path, 'r', encoding='utf-8', errors='replace') as f:
        line = f.readline()
        while line:
            try:
                yield line.strip()
            except UnicodeDecodeError:
                print('UnicodeDecodeError: DAFUQ!')
            line = f.readline()

def load_countries():
    countries = {}
    with open('correct.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        lineNumber = 0
        for row in csv_reader:
            if row[8] not in countries and lineNumber != 0:
                # print(f'Unique country: {row[8]}')
                countries[row[8]] = {'cities': []}
            elif lineNumber != 0 and row[2] is not "":
                data = countries[row[8]]
                data['cities'].append(row[2])
            lineNumber += 1
    save_file(json.dumps(countries), 'countries_city.json')

def save_file(data, path):
    print('Saving data into file', path)
    with open(path, 'w') as f:
        f.write(data)
    print('Done saving data into file', path)

def load_file(path):
    print('Loading data from file', path)
    with open(path, 'r') as f:
        return json.loads(f.read())