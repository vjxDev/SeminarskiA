from Element import Element
from helper import add_padding, draw_rect


def draw(matrix_in: list[list[bool]]) -> Element:
    g = Element('g')

    for y_index, row in enumerate(matrix_in):
        for x_index, el in enumerate(row):
            if el:
                rect = draw_rect(x_index*24, y_index*24)
                g.append_child(rect)
    return g
