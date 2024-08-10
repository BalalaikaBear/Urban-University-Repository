def strsort(string):
    return "".join(sorted(string))


print(strsort("bCa"))


def word_sorted(string):
    return ", ".join(sorted(string.split()))

def last_sorted_word(string):
    return sorted(string.split())[-1]

def the_longest_word(string):
    return sorted(string.split(), key=len)[-1]


test = "Tom Dick Harry"
print(word_sorted(test))
print(last_sorted_word(test))
print(the_longest_word(test))
