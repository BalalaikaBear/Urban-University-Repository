def solution(a, b):
    c = sorted([a, b], key=len)
    return c[0] + c[1] + c[0]


print(solution('45', '1') == '1451')
print(solution('13', '200') == '1320013')
print(solution('Soon', 'Me') == 'MeSoonMe')
print(solution('U', 'False') == 'UFalseU')