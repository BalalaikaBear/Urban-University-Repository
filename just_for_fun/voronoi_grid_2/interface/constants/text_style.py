from enum import StrEnum, auto

class TextStyle(StrEnum):
    BOLD = 'BOLD'
    ITALIC = 'ITALIC'
    ITALICBOLD = 'ITALICBOLD'
    COLOR = 'COLOR:'

if __name__ == '__main__':
    ts = TextStyle.COLOR
    print(ts, ts.name, ts.value)
    print(TextStyle.ITALIC, TextStyle.ITALIC.name, TextStyle.ITALIC.value)