

from Element import Element
from helper import add_padding, cell_size, draw_rect


def draw(matrix_in: list[list[bool]]) -> Element:
    g = Element('g')
    matrix = add_padding(matrix_in, 1)

    radius = 4
    f = True

    for y_index, row in enumerate(matrix_in):
        for x_index, el in enumerate(row):
            if el:
                top = matrix[y_index+1-1][x_index+1]
                bottom = matrix[y_index+1+1][x_index+1]
                left = matrix[y_index+1][x_index-1+1]
                right = matrix[y_index+1][x_index+1+1]
                total_sum = [top, bottom, left, right].count(True)
                element: Element
                if(f):
                    print(f"t:{top}|l{left}|b{bottom}|r{right}|s{total_sum}")
                    f = False

                if total_sum >= 3:
                    element = draw_rect(x_index*cell_size, y_index*cell_size)
                else:
                    path = f"M {x_index*cell_size+cell_size/2} {y_index*cell_size}"
                    if not (top or left):
                        path += f"h -{(cell_size/2)-radius} q -{radius} 0 -{radius} {radius}"
                    else:
                        path += f"h -{cell_size/2} v{radius}"

                    if not (left or bottom):
                        path += f"v {cell_size-radius*2} q 0 {radius} {radius} {radius}"
                    else:
                        path += f"v {cell_size-radius} h {radius}"

                    if not (bottom or right):
                        path += f"h {cell_size-radius*2} q {radius} 0 {radius} -{radius}"
                    else:
                        path += f"h {cell_size-radius} v -{radius} "

                    if not (right or top):
                        path += f"v -{cell_size-radius*2} q 0 -{radius} -{radius} -{radius}"
                    else:
                        path += f"v -{cell_size-radius} "
                    path += "z"
                    element = Element("path")
                    element.add_attribute("d", path)
                g.append_child(element)

    return g
