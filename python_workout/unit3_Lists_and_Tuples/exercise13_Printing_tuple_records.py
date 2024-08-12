PEOPLE = [("Duck", "Temp", 7.85),
          ("Ivan", "Petrov", 3.625),
          ("Jan", "Itor", 10.603)]


def format_sort_records(people):
    """
    Возврат данных в виде таблицы.
    Ширина столбца - 10, 10, 5
    """
    output = []
    for person in sorted(people, key=lambda p: p[1]):
        output.append("{1:10} {0:10} {2:5.2f}".format(*person))
    return "\n".join(output)


print(format_sort_records(PEOPLE))
