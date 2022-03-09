from importlib.machinery import SourceFileLoader
from types import ModuleType
from typing import Callable
from Element import Element


def get_draw_fun_from_module(mod: ModuleType) -> Callable[[list[list[bool]]], Element]:
    # mod je dict sa kljucevima "name" i "path", path je relativna putanja od lokacije projekta
    # primer oblika mod mozete naci u mods\themes\Banana.json
    m = SourceFileLoader(
        mod["name"], mod["path"]).load_module()
    if(hasattr(m, "draw")):
        d: Callable[[list[list[bool]]], Element] = m.draw
        return d
    raise ImportError("Now draw function in", mod["name"], mod["path"])


def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def rgb_to_hex(colortuple: tuple[int, int, int]):
    return '#' + ''.join(f'{i:02X}' for i in colortuple)


cell_size = 24
padding = 1


def add_padding(matrix_mod, padding=padding):
    cells = len(matrix_mod[0])
    matrix_p = [[False for x in range(cells+padding*2)]
                for x in range(cells+padding*2)]
    for row_index in range(cells):
        for element_index in range(cells):
            matrix_p[row_index+padding][element_index +
                                        padding] = matrix_mod[row_index][element_index]
    return matrix_p


def draw_rect(startX: int, startY: int, width=cell_size, height=cell_size):
    el = Element("rect")
    el.add_attribute("x", str(startX))
    el.add_attribute("y", str(startY))
    el.add_attribute("width", str(width))
    el.add_attribute("height", str(height))
    return el


def draw_circle(startX, startY, width=cell_size):
    el = Element('circle')
    el.add_attribute('cx', str(startX+width/2))
    el.add_attribute('cy', str(startY+width/2))
    el.add_attribute('r', str(width/2))
    return el


def draw_rect_code(matrix: list[list[bool]]) -> Element:
    g = Element('g')
    for yIndex, row in enumerate(matrix):
        for xIndex, el in enumerate(row):
            if el:
                rect = draw_rect(xIndex*24, yIndex*24, 24, 24)
                g.append_child(rect)
    return g
