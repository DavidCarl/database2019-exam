import filemanager
import re
import mysqlconnector as sql_db
from console_progressbar import ProgressBar


# countries = filemanager.load_file('countries_city.json')

def go_through_books():
    fileNames = filemanager.get_files()
    fileCounter = 0
    # print('Searching through the books!')
    print('')
    pb = ProgressBar(total=len(fileNames),prefix='Inserting books to MySQL!', suffix='', decimals=3, length=100, fill='█', zfill='░') # ▒
    for each in fileNames:
        fileCounter += 1
        content = filemanager.load_book(each)
        sql_db.insert_book(each, 'Book Title Here', 'Author here', content)
        pb.print_progress_bar(fileCounter)
    print('File Counter', fileCounter)

def get_author():
    pass

def line_contain_words(line, word):
    pass

def failed_books():
    content = filemanager.load_book('12hgp10a.txt')
    sql_db.insert_book('12hgp10a.txt', 'Book Title Here', 'Author here', content)

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
                cities[row[4]] = {"lat": row[5], "lng": row[6]}
        # print(book_id)
        # print(title)
        # print(fileName)
        # print(cities)
        # print(authors)

#         break

# migrate_mysql_to_mongo()

# go_through_books()
# filemanager.load_countries()

# sql_db.insert_book('test', 'David Carl', 'CykaBlyat')
# failed_books()