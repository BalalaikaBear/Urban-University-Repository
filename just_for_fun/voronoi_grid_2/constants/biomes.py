from dataclasses import dataclass
from enum import Enum, StrEnum, auto

@dataclass(frozen=True, kw_only=True)
class BiomeClass:
    name: str
    cost: int | float = 1
    vision: int = 2
    resources: dict = None


class ResourceClass(StrEnum):
    # основные ресурсы
    WOOD = auto()
    STONE = auto()
    FOOD = auto()

    # стратегические ресурсы
    IRON = auto()
    COAL = auto()


class Biomes(Enum):
    NONE = BiomeClass(
        name='None'
    )

    # roads
    ROAD = BiomeClass(
        name='Road',
        cost=0.5
    )
    RAILROAD = BiomeClass(
        name='Rail road',
        cost=0.25
    )

    # land
    GRASSLAND = BiomeClass(
        name='grassland',
        resources={ResourceClass.FOOD: 2}
    )
    DESERT = BiomeClass(
        name='Desert'
    )
    SAVANNA = BiomeClass(
        name='Savanna',
        resources={ResourceClass.FOOD: 1}
    )
    HILL = BiomeClass(
        name='Hill',
        cost=2,
        vision=3,
        resources={ResourceClass.STONE: 1}
    )

    # forests
    FOREST = BiomeClass(
        name='Forest',
        cost=2,
        vision=1,
        resources={ResourceClass.WOOD: 2}
    )
    TUNDRA = BiomeClass(
        name='Tundra',
        cost=2,
        vision=1,
        resources={ResourceClass.WOOD: 2}
    )
    TAIGA = BiomeClass(
        name='Taiga',
        cost=2,
        vision=1,
        resources={ResourceClass.WOOD: 2}
    )

    # mountains
    MOUNTAIN = BiomeClass(
        name='Mountain',
        cost=4,
        vision=4,
        resources={ResourceClass.STONE: 1}
    )
    VULCANO = BiomeClass(
        name='Vulcano',
        cost=4,
        vision=4,
        resources={ResourceClass.STONE: 1}
    )

    # water
    RIVER = BiomeClass(
        name='River',
        resources={ResourceClass.FOOD: 1}
    )
    LAKE = BiomeClass(
        name='Lake',
        vision=3,
        resources={ResourceClass.FOOD: 1}
    )
    COAST = BiomeClass(
        name='Coast',
        resources={ResourceClass.FOOD: 1}
    )
    OCEAN = BiomeClass(
        name='Ocean',
        vision=3
    )

if __name__ == '__main__':
    print(ResourceClass.WOOD)
