import csv
import os

def write_results(file, dict): # works
    with open('temp.csv', 'w', newline = '') as temp:
            header = ['name', 'assignment', 'grade']
            writer = csv.writer(temp, delimiter=',')
            writer.writerow(header)
            for k, v in dict.items():
                writer.writerow([k, *v, *v.values()])
    os.replace('temp.csv', file)
