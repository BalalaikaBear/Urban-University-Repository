import multiprocessing
from datetime import datetime

def read_info(name):
    with open(name, 'r') as file:
        all_data = [line.strip() for line in file]

if __name__ == '__main__':
    # список файлов
    files = [f'file {i}.txt' for i in range(1,5)]

    # without multiprocessing
    start = datetime.now()
    for file in files:
        read_info(file)
    end = datetime.now()
    print('Without multiprocessing:', end - start)

    # with multiprocessing
    start = datetime.now()
    with multiprocessing.Pool(processes=len(files)) as pool:
        pool.map(read_info, files)
    end = datetime.now()
    print('With multiprocessing:   ', end - start)
