#https://www.codewars.com/kata/563c13853b07a8f17c000022/python
from datetime import datetime

def is_today(date):
    print(date)
    if date.date() == datetime.today().date():
        return True
    else:
        return False


print(is_today(datetime(2020, 10, 1, 1, 1, 1, 1)))
print(is_today(datetime(2080, 10, 1, 1, 1, 1, 1)))
print(is_today(datetime.today()))