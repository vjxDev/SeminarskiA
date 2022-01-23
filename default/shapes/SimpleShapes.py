from importlib.machinery import SourceFileLoader
import math
from types import ModuleType
from typing import Callable
from Element import Element
from Generator import generator
from helper import cellSize, drawRect, drawCircle
from import_files import getSimpleShpaes
import inquirer


def importSimpleShapeDraw(mod: ModuleType) -> Callable[[int, int], Element]:
    m = SourceFileLoader(
        mod["name"], mod["path"]).load_module()
    if(hasattr(m, "draw")):
        d: Callable[[int, int], Element] = m.draw
        return d
    raise ImportError("Now draw funcion in", mod["name"], mod["path"])


def defaultDraw(x: int, y: int) -> Element:
    return drawRect(x, y)


def miniForm():
    simpleShapes = getSimpleShpaes()

    options = [shape['name'] for shape in simpleShapes]
    selectedList = inquirer.checkbox(
        "Select one or multiple simple shapes", choices=options)
    drawFuncs: list[Callable[[int, int], str]] = []

    for s in selectedList:
        index = next((i for i, item in enumerate(options) if item == s), -1)
        if index == -1:
            continue
        else:
            option = simpleShapes[index]
            drawFuncs.append(importSimpleShapeDraw(option))
    if(len(drawFuncs) == 0):
        drawFuncs.append(defaultDraw)

    return drawFuncs


def draw(matrix: list[list[bool]]) -> Element:
    g = Element('g')

    funcs = miniForm()
    gen = generator(239856329867)

    def fRandom():
        return math.floor(next(gen)*len(funcs))

    for yIndex, row in enumerate(matrix):
        for xIndex, el in enumerate(row):
            if el:
                g.append_child(funcs[fRandom()](
                    xIndex*cellSize, yIndex*cellSize))
    return g
