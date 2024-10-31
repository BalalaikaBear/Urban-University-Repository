class Text:
    """Объект, хранящий информацию об отображаемом тексте"""
    def __init__(self,
                 text: str,
                 front: str = 'Arial',
                 size_mult: float | None = None) -> None:
        self.text = text
        self.front = front
        self.size = size_mult
        print(f'Text({self.text = }, {self.front = }, {self.size = })')

    def __repr__(self) -> str:
        return f'Text({self.text})'


class Icon:
    """Объект, хранящий информацию об иконке"""
    def __init__(self,
                 img: str,
                 size_mult: float | None = None) -> None:
        self.img = img
        self.size = size_mult
        print(f'Icon({self.img = }, {self.size = })')

    def __repr__(self) -> str:
        return f'Icon({self.img})'


class IconText(Text, Icon):
    """Объект, хранящий информацию о тексте с иконкой"""
    def __init__(self,
                 text: str,
                 img: str,
                 front: str = 'Arial',
                 size_mult: float | None = None) -> None:
        Text.__init__(self, text, front, size_mult)  # вызов Text
        Icon.__init__(self, img, size_mult)  # вызов Icon

    def __repr__(self) -> str:
        return f'IconText({self.text})'


class CheckBox:
    """Окно флажка"""
    def __init__(self,
                 on_return: str | int | float,
                 off_return: str | int | float,
                 default_state: bool = False) -> None:
        self.on_return = on_return
        self.off_return = off_return
        self.state = default_state

    def click(self) -> None:
        """Изменение состояния флажка при нажатии"""
        self.state = not self.state

    @property
    def named_state(self) -> str | int | float:
        """Возвращает записанное представление флажка"""
        return self.on_return if self.state else self.off_return

    def set_state(self, state: bool) -> None:
        """Устанавливает состояние флажка"""
        self.state = state

    def __bool__(self) -> bool:
        return self.state

    def __repr__(self) -> str:
        return f'CheckBox({self.state})'


class Slider:
    """Слайдер """
    def __init__(self,
                 min_value: int | float,
                 max_value: int | float,
                 steps: int = 10,
                 default_value: int | float = None) -> None:
        self.min_value, self.max_value = sorted([min_value, max_value])
        self.steps = steps
        if not default_value:
            self.value = int((max_value - min_value) / 2)
        else:
            self.value = default_value

    def __repr__(self) -> str:
        return f'Slider({self.value})'

if __name__ == '__main__':
    iron: IconText = IconText('Iron', 'iron.png', 'Arial', 1.2)
    print(dir(iron))
    slider: Slider = Slider(10, 15, 5)
    print(slider.min_value, slider.max_value)