import datetime
import json
from random import randint

results = []
files = ['file1.json', 'file2.json', 'file3.json', 'file4.json']

# заполнение файлов
for file in files:
    for _ in range(100_000):
        results.append(randint(0, 100_000))
    with open(file, 'w') as f:
        json.dump(results, f)
    results = []

# считывание файлов
results_to_count = []
start = datetime.datetime.now()

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        results_to_count.extend(data)

# вывод суммы чисел
print(sum(results_to_count))
end = datetime.datetime.now()
print(end - start)