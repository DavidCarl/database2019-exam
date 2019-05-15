import filemanager
import re
from console_progressbar import ProgressBar


def go_through_books():
    fileNames = filemanager.get_files()
    counter = 0
    fileCounter = 0
    # print('Searching through the books!')
    print('')
    pb = ProgressBar(total=len(fileNames),prefix='Searching books!', suffix='', decimals=3, length=100, fill='█', zfill='░') # ▒
    for each in fileNames:
        fileCounter += 1
        for line in filemanager.load_book(each):
            if 'The Project Gutenberg eBook' in line:
                counter += 1
        pb.print_progress_bar(fileCounter)
    print('File Counter', fileCounter)
    print('Contains counter', counter)

def get_author():
    pass

def line_contain_words(line, word):
    pass

go_through_books()
# filemanager.load_countries()