from typing import Optional
import pygame

class Container:
    """Контейнер, являющийся основным классом для всех объектов интерфейса"""
    def __init__(self,
                 *children: 'Container',
                 parent: Optional['Container'] = None,
                 max_size: tuple[int, int] = None,
                 touchable: bool = False) -> None:
        self.touchable = touchable

        if children:
            self.children: tuple['Container', ...] = children

        self.parent: Optional['Container'] = parent

        if max_size:
            self.max_size: pygame.Rect = pygame.Rect(0, 0, *max_size)

        # расчет минимального размера
        if children:
            self._size_calc(*children, parent=self)

    def size_of_container(self) -> pygame.Rect:
        """Расчёт размера контейнера"""
        return pygame.Rect(0, 0, 10, 10)

    def _size_calc(self, *children: 'Container', parent: 'Container') -> pygame.Rect:
        """Расчет размера контейнера через определение минимальных размеров детей"""
        # собственный размер контейнера
        self.min_size: pygame.Rect = self.size_of_container()

        # рекурсия и объединение границ контейнеров
        if children:
            for child in children:
                if hasattr(child, 'children'):
                    self.min_size.union(child._size_calc(*child.children, parent=parent))

        return self.min_size

    def __repr__(self) -> str:
        return f'Container()'


class WordBox(Container):
    """Контейнер с единственным словом"""
    __slots__ = ['word', 'rect', 'bold', 'italic', 'size', 'color', 'font_style', 'font', 'parent', 'touchable']

    def __init__(self, word: str, size: int, font: str):
        super().__init__()
        self.word = word
        self.font = None
        self.rect = None

        # стиль текста
        self.bold = False
        self.italic = False
        self.color = None
        self.size = size
        self.font_style = font

    def size_of_container(self) -> pygame.Rect:
        """Расчёт размера контейнера"""
        self.font: pygame.Font = pygame.font.SysFont(self.font_style, self.size, self.bold, self.italic)
        self.rect: pygame.Rect = pygame.Rect(0, 0, *self.font.size(self.word))
        return self.rect

    def __repr__(self) -> str:
        return self.word


class TextBox(Container):
    """Контейнер с текстом"""
    def __init__(self, text: str, multiline: bool = True):
        # разбиение текста на слова для создания отдельных текстовых контейнеров
        text_split = text.split()
        list_of_WordBoxes: list[Container] = []
        for word in text_split:
            list_of_WordBoxes.append(WordBox(word, 12, 'Arial'))
        super().__init__(*list_of_WordBoxes, parent=self)

        self.text = text
        self.multiline = multiline

    def size_of_container(self) -> pygame.Rect:
        """Расчёт размера контейнера"""
        return pygame.Rect(0, 0, 40, 10)

    def __repr__(self) -> str:
        if len(self.text) > 10:
            return f"TextBox('{self.text[:10]}...')"
        else:
            return f"TextBox('{self.text}')"


if __name__ == '__main__':
    widget: Container = Container(TextBox('TEXT'))
    print(dir(widget))