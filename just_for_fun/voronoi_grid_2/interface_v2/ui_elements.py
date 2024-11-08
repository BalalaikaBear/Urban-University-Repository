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
        return pygame.Rect(0, 0, 400, 50)

    def _size_calc(self, *children: 'Container', parent: 'Container') -> pygame.Rect:
        """Расчет размера контейнера через рекурсию собственных атрибутов"""
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


class TextBox(Container):
    """Текст"""
    def __init__(self, text: str, multiline: bool = True):
        super().__init__()
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