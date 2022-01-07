from typing import TypedDict, Literal


class ColorType(TypedDict):
    name: str
    color: str


ColorsType = list[ColorType]


class EyeType(TypedDict):
    name: str
    path: str
    type: Literal['module', 'file']


class ShapeType(TypedDict):
    name: str
    path: str
    type: Literal['module', 'file']


class DotsThemeType(TypedDict):
    type: Literal["one", "gradient", "multicolor"]
    colors: list[str]


class EyesThemeType(TypedDict):
    type: Literal["one", "gradient"]
    colors: list[str]


class ThemeType(TypedDict):
    name: str
    dotsColor: DotsThemeType
    dotsShape: ShapeType
    eyesColor: tuple[EyesThemeType, EyesThemeType, EyesThemeType]
    eyesShape: tuple[EyeType, EyeType, EyeType]


ThemesType = list[ThemeType]
