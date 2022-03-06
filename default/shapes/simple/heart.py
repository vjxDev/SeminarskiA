from Element import Element
from helper import cell_size, draw_rect


def draw(x: int, y: int) -> Element:
    element = Element('path')
    pos_x = x + 12
    pos_y = y + 21
    element.add_attribute('d',
                          f"M{pos_x} {pos_y}.35l-1.45-1.32c-5.15-4.67-8.55-7.76-8.55-11.53 0-3.09 2.42-5.5 5.5-5.5 1.74 0 3.41.81 4.5 2.08 1.09-1.27 2.76-2.08 4.5-2.08 3.08 0 5.5 2.41 5.5 5.5 0 3.77-3.4 6.86-8.55 11.53l-1.45 1.32z")
    return element
