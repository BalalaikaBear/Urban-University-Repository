from typing import Type

from just_for_fun.voronoi_grid_2.constants.biomes import Biomes

from perlin_noise import PerlinNoise

# ПАРАМЕТРЫ КАРТЫ
AVG_TEMP: float = 36  # средняя температура
WATER_PERCENT: float = 0.02  # процент воды
ROUGHNESS: int = 1  # шероховатость карты

# кол-во особых клеток
RIVER_MAX: int = 4  # максимальное количество рек на чанк
CRATER_MAX: int = 2  # максимальное количество кратеров на чанк
VOLCANO_MAX: int = 2  # максимальное количество вулканов на чанк

class WorldGen:
    __instance = None

    def __new__(cls, *args, **kwargs) -> Type['WorldGen']:  # паттерн Singleton - объект класса создается единожды
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, seed: int = 1):
        if not hasattr(self, 'data'):  # предотвращение повторной инициализации
            self.seed = seed
            self._noise1 = PerlinNoise(1, seed=seed)
            self._noise2 = PerlinNoise(2, seed=seed)
            self._noise3 = PerlinNoise(3, seed=seed)
            self._noise4 = PerlinNoise(4, seed=seed)

    def noise(self, point: tuple[float, float]) -> float:
        """Возвращает значение шума при заданной координате"""
        return (self._noise1.noise(point) + self._noise2.noise(point)
                + self._noise3.noise(point) + self._noise4.noise(point))

    def cell_type(self, point: tuple[float, float]) -> Biomes:
        if self.noise(point) < WATER_PERCENT:
            return Biomes.OCEAN
        else:
            return Biomes.GRASSLAND
