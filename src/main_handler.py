import argparse
import os
from src.handlers.csv_handler import *
from src.handlers.xlsx_handler import *


def check_filetype(file: str) -> str:
    file_list = file.split('.')
    return file_list[len(file_list)-1].lower()


def check_file(file: str) -> bool:
    return os.path.exists(file)


def main(file):
    if not check_file(file):
        raise Exception('File does not exist')
    ext = check_filetype(file)
    if ext == 'csv':
        read_csv(file)
    elif ext == 'xlsx':
        read_xlsx(file)
    else:
        print('File extension not supported: %s' % ext)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Read a .csv or .xlsx file and normalize date formats.'
        )
        parser.add_argument(
            '-f',
            dest='filename',
            help='Input a filename with path'
        )
        args = parser.parse_args()
        filename = args.filename
        main(filename)
    except Exception as e:
        print('Error:', e)
