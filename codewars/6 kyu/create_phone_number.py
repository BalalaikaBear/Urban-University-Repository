#https://www.codewars.com/kata/525f50e3b73515a6db000b83/python

def create_phone_number(n):
    return str('(%s%s%s) %s%s%s-%s%s%s%s'
               % (n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8], n[9]))


print(create_phone_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
print(create_phone_number([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))
print(create_phone_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
print(create_phone_number([0, 2, 3, 0, 5, 6, 0, 8, 9, 0]))
print(create_phone_number([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))