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

go_through_books()
# filemanager.load_countries()

# sql_db.insert_book('test', 'David Carl', 'CykaBlyat')