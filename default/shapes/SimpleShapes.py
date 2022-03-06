from importlib.machinery import SourceFileLoader
import math
from types import ModuleType
from typing import Callable
from Element import Element
import random_g
from helper import cell_size, draw_rect, draw_circle
import import_files
import inquirer


def import_simple_draw(mod: ModuleType) -> Callable[[int, int], Element]:
    m = SourceFileLoader(
        mod["name"], mod["path"]).load_module()
    if(hasattr(m, "draw")):
        draw: Callable[[int, int], Element] = m.draw
        return draw
    raise ImportError("Now draw funcion in", mod["name"], mod["path"])


def default_draw(x: int, y: int) -> Element:
    return draw_rect(x, y)


def form_simple_shapes():
    simple_shapes = import_files.simple_shpaes()

    options = [shape['name'] for shape in simple_shapes]
    selected_list = inquirer.checkbox(
        "Select one or multiple simple shapes", choices=options)
    draw_functions: list[Callable[[int, int], str]] = []

    for s in selected_list:
        index = next((i for i, item in enumerate(options) if item == s), -1)
        if index == -1:
            continue
        else:
            option = simple_shapes[index]
            draw_functions.append(import_simple_draw(option))
    if(len(draw_functions) == 0):
        draw_functions.append(default_draw)

    return draw_functions


def draw(matrix: list[list[bool]]) -> Element:
    g = Element('g')

    funcs = form_simple_shapes()
    gen = random_g.gen(239856329867)

    def fRandom():
        return math.floor(next(gen)*len(funcs))

    for y_index, row in enumerate(matrix):
        for x_index, el in enumerate(row):
            if el:
                g.append_child(funcs[fRandom()](
                    x_index*cell_size, y_index*cell_size))
    return g
