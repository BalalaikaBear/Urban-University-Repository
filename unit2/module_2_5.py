def get_matrix(n, m, value):
    matrix = []
    for i in range(n-1):
        for j in range(m-1):
            matrix = [[value]*m]*n
    return matrix

print(get_matrix(2, 2, 10))
print(get_matrix(3, 5, 42))
print(get_matrix(4, 2, 13))
