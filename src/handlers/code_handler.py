# formats = ['DD/MM/YYYY', 'MM/DD/YYYY', 'YYYY/MM/DD', 'YYYY/DD/MM']


def code_handler(date_format, date, month, year):
    req_format = '%d-%d-%d'
    if date_format == 'DD/MM/YYYY':
        out = req_format % (date, month, year)
    elif date_format == 'MM/DD/YYYY':
        out = req_format % (month, date, year)
    elif date_format == 'YYYY/MM/DD':
        out = req_format % (year, month, date)
    elif date_format == 'YYYY/DD/MM':
        out = req_format % (year, date, month)
    else:
        out = req_format % (date, month, year)
    return out
