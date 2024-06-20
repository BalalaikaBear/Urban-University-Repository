 # работа со словарями
my_dict = {"Aurora": 1965, "Dracula": 655, "Alucard": 2000}
print(my_dict)

print(my_dict["Aurora"], my_dict.get("John", -1))

my_dict.update({"Mike": 1912,
                "Pedro": 1999})

print(my_dict.pop("Dracula"))
print(my_dict)

 # работа с множествами
my_set = {1, 10 ,100, 10, 1, "c", "c"}
print(my_set)

my_set.update({25, "a"})
my_set.discard(100)
print(my_set)