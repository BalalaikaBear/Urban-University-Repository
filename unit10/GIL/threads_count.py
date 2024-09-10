import datetime
import json
from threading import Thread

results = []
threads = []
files = ['file1.json', 'file2.json', 'file3.json', 'file4.json']

def worker(file):
    with open(file, 'r') as f:
        data = json.load(f)
        results.extend(data)

def main():
    start = datetime.datetime.now()

    for i in range(len(files)):
        t = Thread(target=worker, args=(files[i], ))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    sum(results)
    end = datetime.datetime.now()
    return end - start

time_calc = []

for i in range(100):
    results = []
    time_calc.append(main())

print(sum([calc.microseconds for calc in time_calc]) / len(time_calc))

