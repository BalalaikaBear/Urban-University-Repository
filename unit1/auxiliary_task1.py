grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}

students = sorted(students)  # sorting names in alphabetical order

# a SHORT variant of calculating the average
average = []
for i in grades:
    average.append(sum(i)/len(i))

# a LONG variant of calculating the average
average = []
average.append(sum(grades[0])/len(grades[0]))
average.append(sum(grades[1])/len(grades[1]))
average.append(sum(grades[2])/len(grades[2]))
average.append(sum(grades[3])/len(grades[3]))
average.append(sum(grades[4])/len(grades[4]))

book = dict(zip(students, average))  # unite keys and average numbers
print(book)