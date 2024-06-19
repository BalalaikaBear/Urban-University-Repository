immutable_var = (True, "str", [1, 10], 5.5)
print(immutable_var)

immutable_var[2][0] = 5  # кортеж хранит ССЫЛКИ на объекты, которые нельзя изменять (нельзя изменять ссылки)
print(immutable_var)     # но редактировать список в кортеже можно, поскольку данные в нем не являются элементом кортежа

mutable_list = [False, "euphoria", [15, 3.1415], immutable_var]
mutable_list[3] = "radio"
print(mutable_list)
