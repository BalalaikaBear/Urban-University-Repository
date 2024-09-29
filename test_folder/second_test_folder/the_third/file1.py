from variables import var

def func1(string = 'var from file 1'):
    global var
    var = string
    return var

if __name__ == '__main__':
    print(var)
    print(func1(250))
    print(var)
