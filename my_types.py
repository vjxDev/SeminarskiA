from typing import TypedDict, Literal


class ColorType(TypedDict):
    name: str
    color: str


ColorsType = list[ColorType]


class ModuleType(TypedDict):
    name: str
    path: str


class DotsThemeType(TypedDict):
    type: Literal["one", "gradient", "multicolor"]
    colors: list[str]


class EyesThemeType(TypedDict):
    type: Literal["one", "gradient"]
    colors: list[str]


class ThemeType(TypedDict):
    name: str
    dotsColor: DotsThemeType
    dotsShape: ModuleType
    eyesColor: tuple[EyesThemeType, EyesThemeType, EyesThemeType]
    eyesShape: tuple[ModuleType, ModuleType, ModuleType]


ThemesType = list[ThemeType]
