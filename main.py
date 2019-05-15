import csv


with open('correct.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\tCountry_Code {row[8]} contains city called {row[1]}, with a population of {row[14]} people.')
            line_count += 1
    print(f'Processed {line_count} lines.')