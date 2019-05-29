import filemanager
import re
import mysqlconnector as sql_db
import subprocess
import sql_generator
import os
from console_progressbar import ProgressBar


countries = filemanager.load_file('countries_city.json')

def go_through_books():
    fileNames = filemanager.get_files()
    fileCounter = 0
    print('')
    pb = ProgressBar(total=len(fileNames),prefix='Inserting books to MySQL!', suffix='', decimals=3, length=100, fill='█', zfill='░') # ▒
    for each in fileNames:
        fileCounter += 1
        content = filemanager.load_book(each)
        sql_db.insert_book(each, 'Book Title Here', content)
        pb.print_progress_bar(fileCounter)
    print('File Counter', fileCounter)

def get_author_and_title():
    entries = {}
    p1 = subprocess.run(['grep', '-Pr', '-m', '1', "^.*Project\\sGutenberg.*\\sof\\s(.*\\w).+by\\s(.*\\w)", 'unzipped'], stdout=subprocess.PIPE, encoding='utf-8')
    lines = p1.stdout.split('\n')
    for line in lines:
        try:
            line = line.rstrip()
            line = line.split(':', 1)
            book = line[0].rsplit('/', 1)[1]
            if '.txt' not in book:
                continue
            line = line[1].rsplit('by ', 1)
            title = line[0].strip()

            if title[-2:] == ', ':
                title = title[:-2]
            if title[:1] == '*':
                title = title.rsplit('*', 1)[1]
            
            if ord(title[:1]) == 65279:
                title = title[1:]

            if title[:3] == 'The':
                title = title[4:]

            if title[:2] == 'A ':
                title = title[2:]

            if 'End of the Project Gutenberg ' in title:
                title = title[38:]
            elif 'End of The Project Gutenberg ' in title:
                title = title[38:]
            elif 'End of Project Gutenberg' in title:
                title = title[34:]
            elif title[:18] == 'Project Gutenberg ':
                if title[24:26] == 'of':
                    title = title[27:]
                elif title[23] == ',':
                    title = title[25:]
                elif title[18:23].lower() == 'ebook':
                    title = title[24:]
                elif title[18:23].lower() == 'etext':
                    title = title[24:]
                else:
                    title = title[18:]
            elif 'Project Gutenberg\'' in title[:19]:
                title = title[20:]

            authors = line[1]
            authors = authors.split(' and ')
            entries[book] = {'title': title, 'authors': authors}
        except:
            pass

    return entries

def line_contain_words(line, word):
    pass

def city_mention():
    print('Starting to generate SQL files on mentions!')
    res = sql_db.get_all_id_and_filename()
    fileNameID = {}
    for each in res:
        fileNameID[each[1]] = each[0]
    files = filemanager.city_mentions()
    for city in files:
        city_id = sql_db.get_city_id(city[:-5])
        if city_id is not None:
            sql_generator.start_file('city_mentions', 'mentions/' + city[:-5], '')
            for line in filemanager.load_mentions(city):
                if line[-4:] == '.txt':
                    try:
                        sql_generator.city_mentions(city_id[0], fileNameID[line.split('/')[-1:][0]], 'mentions/' + city[:-5])
                    except:
                        pass
                        # print(f'I crashed on {line.split("/")[-1:][0]}')
    city_mentions_cleanup()
    fix_up()

def city_mentions_cleanup():
    for each in filemanager.city_mentions_sql():
        delete = False
        with open('sql_scripts/generated/mentions/' + each, 'r') as sql_file:
            lineList = sql_file.readlines()
            if len(lineList) == 1 and lineList[0] == 'INSERT INTO city_mentions VALUES ':
                delete = True
        if delete is True:
            print('Deleting')
            os.remove('sql_scripts/generated/mentions/' + each)

        # print(each)

def fix_up():    
    sqlfiles = filemanager.city_mentions_sql()
    for each in sqlfiles:
        lineList = None
        certainLine = None
        with open('sql_scripts/generated/mentions/' + each, 'r') as sql_file:
            lineList = sql_file.readlines()
            certainLine = len(lineList) - 1
        listedLine = list(lineList[certainLine])
        listedLine[len(listedLine) - 2] = ';'
        lineList[certainLine] = ''.join(listedLine)
        with open('sql_scripts/generated/mentions/' + each, 'w') as sql_file:
            for item in lineList:
                sql_file.write("%s" % item)

def add_city():
    size = 0
    loop = 1
    for country in countries:
        sql_generator.start_file('city', 'city/' + country, '(`name`, `geolocation`) ')
        size = len(countries[country]['cities'])
        loop = 1
        for obj in countries[country]['cities']:
            sql_generator.city(obj["city"], obj["lat"], obj["long"], 'city/' + country)
            if obj["city"] == 'Adrogue':
                print(str(loop) + ' ' + str(size))
            if loop == size:
                sql_generator.end_file('city/' + country, 'end')
            else:
                sql_generator.end_file('city/' + country, 'continue')
            loop += 1

def author_title_sql():
    res = sql_db.get_all_id_and_filename()
    fileNameID = {}
    for each in res:
        fileNameID[each[1]] = each[0]
    data = get_author_and_title()
    sql_generator.start_file('author', 'authors', '(`name`) ')
    for each in data:
        for author in data[each]['authors']:
            sql_generator.author(author.replace('\'', '`'), 'authors')
        print(data[each])
        try:
            sql_generator.title(data[each]['title'].replace('\'', '`'), fileNameID[each], 'titles')
        except:
            pass

def author_book_bridge():
    sql_generator.start_file('book_author', 'book_author', '')
    data = get_author_and_title()
    res = sql_db.get_all_id_and_filename()
    fileNameID = {}
    for each in res:
        fileNameID[each[2]] = each[0]
    res = sql_db.get_all_id_author()
    author = {}
    for each in res:
        author[each[1]] = each[0]
    for fileName in data:
        try:
            author_file = data[fileName]['authors']
            for each in author_file:
                author_single = each.replace('\'', '')
                book_id = fileNameID[data[fileName]['title'].replace('\'', '')]
                author_id = author[author_single]
                sql_generator.book_author(author_id, book_id, 'book_author')
        except:
            pass
            
author_book_bridge()
# author_title_sql()
# fix_up()
# city_mentions_cleanup()
# city_mention()
# add_city()
# filemanager.load_countries()