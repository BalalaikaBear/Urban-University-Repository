import time, sys
indent = 0  # количесвтво пробелов для отступа
indent_increasing = True  # увеличение или уменьшение отступа

try:
    while True:  # бесконечный цикл
        print(" " * indent, end="")
        print("********")
        time.sleep(0.1)  # пауза длительностью 1/10 секунды

        if indent_increasing:
            # увеличение количества пробелов
            indent += 1
            if indent == 20:
                # изменение направления
                indent_increasing = False
        else:
            # уменьшение количества пробелов
            indent -= 1
            if indent == 0:
                # изменение направления
                indent_increasing = True

except KeyboardInterrupt:  # при нажатии <Ctrl+C> срабатывает ошибка KeyboardInterrupt проигрывающий код внутри except
    sys.exit()