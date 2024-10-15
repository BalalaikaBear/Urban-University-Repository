from enum import Flag, auto

class Biomes(Flag):
    NONE = auto()

    # roads
    ROAD = auto()
    RAILROAD = auto()

    # land
    GRASSLAND = auto()
    DESERT = auto()
    SAVANNA = auto()
    HILL = auto()

    # forests
    FOREST = auto()
    TUNDRA = auto()
    TAIGA = auto()

    # mountains
    MOUNTAIN = auto()
    VULCANO = auto()

    # water
    RIVER = auto()
    LAKE = auto()
    COAST = auto()
    OCEAN = auto()