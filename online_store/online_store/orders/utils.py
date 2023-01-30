import datetime


def make_order_num():
    year = int(datetime.date.today().strftime('%Y'))
    date = int(datetime.date.today().strftime('%d'))
    month = int(datetime.date.today().strftime('%m'))
    result = datetime.date(year, month, date)
    current_date = result.strftime('%Y%m%d')

    return current_date
