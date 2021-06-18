import datetime
from src.handlers.code_handler import *

months = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3,
    "april": 4, "june": 6, "july": 5,
    "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12
}


def get_year(year_str: str) -> int:
    sys_year = datetime.datetime.today().year
    # return if year valid, if not return ridiculous time
    if year_str.isnumeric():
        if len(year_str) == 2:
            if int(str(sys_year)[2:]) <= int(year_str):
                year_str = '20' + year_str
            else:
                year_str = '19' + year_str
        year = int(year_str)
    else:
        year = 9999
    return year


def get_month(month_str: str) -> int:
    sys_month = datetime.datetime.today().month
    # return if month valid, if not return ridiculous time
    if month_str.isnumeric():
        month = int(month_str) if int(month_str) <= 12 else 12
    else:
        month = months[month_str.lower()] \
            if month_str.lower() in months else 12
    return month


def get_date(date_str: str) -> int:
    sys_month = datetime.datetime.today().month
    # return if month valid, if not return ridiculous time
    if date_str.isnumeric():
        date = int(date_str) if int(date_str) <= 31 else 31
    else:
        date = 31
    return date


def date_formatter(date_str, date_format):
    code = ''
    req_code = date_format
    req_format = '%d-%d-%d'
    str_list = []
    specials = '/.-_, '
    start = -1
    # Ensure date_str is string
    date_str = str(date_str)
    for i in range(len(date_str)):
        if start == -1:
            start = i
        if date_str[i] in specials or i == len(date_str)-1:
            if i == len(date_str)-1:
                str_list.append(date_str[start:i+1])
            else:
                str_list.append(date_str[start:i])
            start = -1
    for i in range(len(str_list)):
        code += str(len(str_list[i]))
        if str_list[i].isnumeric():
            code += 'N'
        else:
            code += 'S'
    if code == req_code:
        date = code_handler(
            req_code,
            get_date(str_list[2]),
            get_month(str_list[1]),
            get_year(str_list[0])
        )
    elif code == '2N2N4N':
        if int(str_list[1]) > 12:
            date = code_handler(
                req_code,
                get_date(str_list[1]),
                get_month(str_list[0]),
                get_year(str_list[2])
            )
        else:
            date = code_handler(
                req_code,
                get_date(str_list[0]),
                get_month(str_list[1]),
                get_year(str_list[2])
            )
    elif code == '4N2N2N':
        if int(str_list[2]) > 12:
            date = code_handler(
                req_code,
                get_date(str_list[2]),
                get_month(str_list[1]),
                get_year(str_list[0])
            )
        else:
            date = code_handler(
                req_code,
                get_date(str_list[1]),
                get_month(str_list[2]),
                get_year(str_list[0])
            )
    else:
        date = date_str
    return date

