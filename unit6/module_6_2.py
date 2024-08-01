from colorama import Fore


class Vehicle:

    __COLOR_VARIANTS = ["blue", "orange", "white", "gray", "black", "magenta", "red", "green"]

    def __init__(self, owner, model, color, engine_power):
        self.owner = owner
        self.__model = model
        self.__color = color
        self.__engine_power = engine_power

    def get_model(self):
        return f"Модель: {Fore.RESET + self.__model}"

    def get_horsepower(self):
        return f"Мощность двигателя: {Fore.RESET + str(self.__engine_power)}"

    def get_color(self):
        return f"Цвет: {Fore.RESET + self.__color.capitalize()}"

    def print_info(self):
        print(Fore.BLUE + self.get_model(),
              Fore.BLUE + self.get_horsepower(),
              Fore.BLUE + self.get_color(),
              Fore.BLUE + f"Владелец: {Fore.RESET + self.owner}", sep="\n")

    def set_color(self, new_color):
        if new_color.lower() in self.__COLOR_VARIANTS:
            self.__color = new_color.lower()
        else:
            print(Fore.RED + f"Нельзя сменить цвет на {new_color.capitalize()}")


class Sedan(Vehicle):

    __PASSENGERS_LIMIT = 5


vehicle1 = Sedan('Fedos', 'Toyota Mark II', 'blue', 500)
vehicle1.print_info()
vehicle1.set_color('Pink')
vehicle1.set_color('BLACK')
vehicle1.owner = 'Vasyok'
vehicle1.print_info()