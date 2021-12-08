from typing import TypedDict, Literal


class ColorType(TypedDict):
    name: str
    color: str


colorsType = list[ColorType]


class EyeType(TypedDict):
    name: str
    shape: str


EyesType = list[EyeType]


class ShapeType(TypedDict):
    name: str
    path: str
    type: Literal['module', 'file']


ShapesType = list[ShapeType]
