class Product:
    def __init__(self, name, weight, category):
        self.name = name
        self.weight = weight
        self.category = category

    def __str__(self):
        return f"{self.name}, {self.weight}, {self.category}"


class Shop:
    def __init__(self):
        self.__file_name = "products.txt"

    def get_products(self):
        """
        Вывод информации о продуктах из файла
        """
        file = open(self.__file_name, "r")
        info = file.read()
        file.close()
        return info

    def add(self, *products):
        """
        Добавление продукта в файл
        """
        existed_products = self.get_products().split("\n")  # запись строк в список
        for i, product in enumerate(existed_products):
            existed_products[i] = product[:product.find(",")]  # оставить только информацию о названии продукта

        # добавление продукта в файл
        file = open(self.__file_name, "a")
        for item in products:
            if item.name in existed_products:
                print(f"Продукт {item.name} уже есть в магазине")
            else:
                file.write(f"{item}\n")
                existed_products.append(item.name)

        file.close()


s1 = Shop()
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2) # __str__

s1.add(p1, p2, p3)

print(s1.get_products())
