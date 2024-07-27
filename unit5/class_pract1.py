class Database:

    """
    Архив данных пользователей
    """

    def __init__(self):
        self.data = {}

    def add_user(self, username, password):
        self.data[username] = password


class User:

    """
    Класс пользователя, содержащий атрибуты: username, password
    """

    def __init__(self, username, password, password_confirm):
        self.username = username
        self.upper_check = False
        self.digit_check = False

        for simb in password:  # проверка каждого символа на то, что символ...
            if simb.isupper():  # ... является заглавным
                self.upper_check = True
            if simb.isdigit():  # ... является цифрой
                self.digit_check = True

        if (len(password) >= 8  # проверка на длину пароля
                and self.upper_check and self.digit_check  # проверка на наличие заглавных символов и цифр
                and password == password_confirm):  # повторный пароль совпадает?
            self.password = password

        # освобождение памяти от проверок
        del self.upper_check
        del self.digit_check


if __name__ == "__main__":
    database = Database()
    while True:
        choice = int(input("Выберите действие: \n1 - Вход\n2 - Регистрация\n"))

        # Вход
        if choice == 1:
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            if login in database.data:
                if password == database.data[login]:
                    print(f"Вход выполнен, здравствуйте {login}")
                    break
                else:
                    print("Неверный пароль")
            else:
                print("Пользователь не найден.")

        # Регистрация
        if choice == 2:
            user = User(input("Введите логин: "),
                        password := input("Введите пароль: "),
                        password2 := input("Повторите пароль: "))
            if password != password2:
                print("Пароли не совпадают, попробуйте еще раз.")
                continue  # иначе ошибка
            database.add_user(user.username, user.password)

        print("Данные: ", database.data)