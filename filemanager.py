from os import listdir
from os.path import isfile, join


def get_files():
    mypath = 'unzipped'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def load_book(path):
    # if path == '17152.txt' or path == '12514.txt' or path == '36093.txt':
    #     print('Wierd encoding skipping for now!')
    # else:
    with open('unzipped/' + path, 'r', encoding='utf-8', errors='replace') as f:
        line = f.readline()
        cnt = 1
        while line:
            try:
                print("Line {}: {}".format(cnt, line.strip()))
            except UnicodeDecodeError:
                print('UnicodeDecodeError: DAFUQ!')
            line = f.readline()
            cnt += 1

def go_through_books():
    fileNames = get_files()
    for each in fileNames:
        load_book(each) 
    # load_book('17152.txt')

go_through_books()