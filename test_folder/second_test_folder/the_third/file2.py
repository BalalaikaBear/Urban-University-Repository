import variables

def func2():
    variables.var = 'func 2 variable'
    return variables.var

if __name__ == '__main__':
    print(variables.var)
    print(func2())
    print(variables.var)