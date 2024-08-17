import random, time, copy, sys
WIDTH = 300
HEIGHT = 20

# создание списка списков для клеток
next_cells = []
for x in range(WIDTH):
    column = []  # создание нового столбца
    for y in range(HEIGHT):
        if random.randint(0, 1) == 0:
            column.append("#")  # добавление живой клетки
        else:
            column.append(".")  # добавление мертвой клетки
    next_cells.append(column)

# основной цикл
try:
    while True:
        print("\n\n\n\n\n")  # отделить каждый шаг с помощью символов новой строки
        current_cells = copy.deepcopy(next_cells)

        # вывод текущих клеток на экран
        for y in range(HEIGHT):
            for x in range(WIDTH):
                print(current_cells[x][y], end="")  # отображение сетки
            print()  # новая строка

        # вычисление клеток на следующем шаге
        for x in range(WIDTH):
            for y in range(HEIGHT):
                # получение соседних координат

                # выражение "% WIDTH" гарантирует, что значение left_coord всегда находится между 0 и WIDTH - 1
                left_coord  = (x-1) % WIDTH
                right_coord = (x+1) % WIDTH
                above_coord = (y-1) % HEIGHT
                below_coord = (y+1) % HEIGHT

                # вычисление количества живых соседних клеток
                num_neighbors = 0
                if current_cells[left_coord][above_coord] == "#":  # слева сверху
                    num_neighbors += 1
                if current_cells[x][above_coord] == "#":  # сверху
                    num_neighbors += 1
                if current_cells[right_coord][above_coord] == "#":  # сверху справа
                    num_neighbors += 1
                if current_cells[left_coord][y] == "#":  # слева
                    num_neighbors += 1
                if current_cells[right_coord][y] == "#":  # справа
                    num_neighbors += 1
                if current_cells[left_coord][below_coord] == "#":  # слева снизу
                    num_neighbors += 1
                if current_cells[x][below_coord] == "#":  # снизу
                    num_neighbors += 1
                if current_cells[right_coord][below_coord] == "#":  # справа снизу
                    num_neighbors += 1

                # изменение клетки на основе правил игры "Жизнь"
                if current_cells[x][y] == "#" and (num_neighbors == 2  # если есть соседи - клетка остается живой
                                                   or num_neighbors == 3):
                    next_cells[x][y] = "#"
                elif current_cells[x][y] == "." and num_neighbors == 3:  # мертвая клетка оживает при наличии соседей
                    next_cells[x][y] = "#"
                else:  # остальные клетки умирают или остаются мертвыми
                    next_cells[x][y] = "."

        time.sleep(1)  # пауза в секунду

except KeyboardInterrupt:
    sys.exit()