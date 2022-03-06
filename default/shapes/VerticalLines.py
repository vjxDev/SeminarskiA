from Element import Element
from helper import add_padding, cell_size, draw_rect, draw_circle
import math


def draw(matrix_in: list[list[bool]]) -> Element:
    g = Element('g')
    matrix = add_padding(matrix_in, 1)

    size = 20
    for y_index, row in enumerate(matrix_in):
        for x_index, el in enumerate(row):
            if el:
                top = matrix[y_index+1-1][x_index+1]
                bottom = matrix[y_index+1+1][x_index+1]
                element: Element

                centerX = x_index*cell_size+cell_size/2
                centerY = y_index*cell_size+cell_size/2

                removed = (cell_size - size) / 2

                if top and bottom:
                    element = draw_rect(x_index*cell_size +
                                        removed, y_index*cell_size, size, 24)
                elif top or bottom:
                    element = Element('path')
                    element.add_attribute('d',
                                          f"M {x_index*24} {y_index*24 + removed}" +
                                          f"v {24-removed*2}" +
                                          f"h {24/2}"
                                          f"a {size/2} {size/2}, 0, 0, 0, 0 {-size}"
                                          )
                    if top:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi ) / math.pi/2},{centerX},{centerY})")
                    if bottom:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi * -1) / math.pi/2},{centerX},{centerY})")
                else:
                    element = draw_circle(
                        x_index*cell_size, y_index*cell_size, size)
                g.append_child(element)
    return g
