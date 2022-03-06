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
                left = matrix[y_index+1][x_index-1+1]
                right = matrix[y_index+1][x_index+1+1]
                element: Element

                x_center = x_index*cell_size+cell_size/2
                y_center = y_index*cell_size+cell_size/2

                removed = (cell_size - size) / 2

                if left and right:
                    element = draw_rect(
                        x_index*cell_size, y_index*cell_size + removed, 24, size)
                elif left or right:
                    element = Element('path')
                    element.add_attribute('d',
                                          f"M {x_index*24} {y_index*24 + removed}" +
                                          f"v {24-removed*2}" +
                                          f"h {24/2}"
                                          f"a {size/2} {size/2}, 0, 0, 0, 0 {-size}"
                                          )
                    if right:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi ) / math.pi},{x_center},{y_center})")
                else:
                    element = draw_circle(
                        x_index*cell_size, y_index*cell_size, size)

                g.append_child(element)
    return g
