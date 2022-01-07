from typing import TypedDict, Literal


class ColorType(TypedDict):
    name: str
    color: str


ColorsType = list[ColorType]


class EyeType(TypedDict):
    name: str
    shape: str


EyesType = list[EyeType]


class ShapeType(TypedDict):
    name: str
    path: str
    type: Literal['module', 'file']


ShapesType = list[ShapeType]


class ThemeType(TypedDict):
    name: str
    type: Literal["one", "gradient", "multicolor"]
    colors: list[str]


ThemesType = list[ThemeType]
