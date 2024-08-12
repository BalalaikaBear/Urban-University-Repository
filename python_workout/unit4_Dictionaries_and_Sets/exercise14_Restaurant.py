MENU = {"сэндвич": 10, "шаурма": 20, "сок": 5, "газировка": 3, "лазанья": 22, "грибной суп": 14}


def restaurant():
    order_sum = 0
    while order := input("Введите блюдо, которое хотите заказать: ").strip().lower():  # strip - удаление пробелов
        if price := MENU.get(order):  # если блюдо есть в меню...
            order_sum += price
            print(f"Стоимость блюда {order}: {price} злотых. Итоговая сумма заказа: {order_sum} злотых")
        else:
            print("Данного блюда нет в меню")
    print(f"Финальная стоимость заказа: {order_sum} злотых")


restaurant()
