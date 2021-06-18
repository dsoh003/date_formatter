import csv
import os
import platform
from src.handlers.dateformat_handler import *


def read_csv(file, date_format, selections, filelocation=None):
    error = None
    rows = []
    with open(file, 'r+') as data:
        reader = csv.DictReader(data)
        fieldnames = reader.fieldnames
        for idx in selections.curselection():
            for i, row in enumerate(reader):
                row[selections.get(idx)] = date_formatter(row[selections.get(idx)], date_format)
                rows.append(row)
        if filelocation is None:
            if platform.system() != 'Windows':
                error = 'Only Windows supported'
            else:
                username = os.getlogin()
                filename = 'C:\\Users\\%s\\Desktop\\%s' \
                           % (username, os.path.basename(file))
        else:
            error = 'Other locations not supported'
        with open(filename, 'w', newline='') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            new_file.close()
        return filename, error


def get_fieldnames(file):
    with open(file, 'r') as data:
        reader = csv.DictReader(data)
        return reader.fieldnames
