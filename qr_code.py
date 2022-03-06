from copy import copy, deepcopy
import math

import random_g
import theme
from my_types import ThemeType
from Element import Element
from helper import draw_rect, get_draw_fun_from_module

from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L


def make_matrix(string: str, padding=0) -> list[list[bool]]:
    code = QRCode(border=padding, error_correction=ERROR_CORRECT_L)
    code.add_data(string)
    code.make()
    matrix = code.get_matrix()
    return matrix


def debug_print_qrcode(matrix: list[list[bool]]):
    for row in matrix:
        for el in row:
            if el:
                print("⬛", end="")
            else:
                print("⬜", end="")
        print()


def matrix_remove_eyes(list: list[list[bool]]) -> list[list[bool]]:
    m = copy(list)
    cells = len(m[0])

    for rowIndex in range(cells):
        for elementIndex in range(cells):
            if rowIndex < 7 and elementIndex < 7:
                m[rowIndex][elementIndex] = False

            if rowIndex < 7 and elementIndex > cells-8:
                m[rowIndex][elementIndex] = False
            if rowIndex > cells-8 and elementIndex < 7:
                m[rowIndex][elementIndex] = False
    return m


IDDotsFill = "dots-fill"
IDDotsMask = "dots-mask"
def IDEyesFill(x): return f"{x}-eye-fill"
def IDEyesMask(x): return f"{x}-eye-mask"


def draw_code(matrix: list[list[bool]], theme: ThemeType) -> str:

    drawDotsFun = get_draw_fun_from_module(theme["dotsShape"])
    dEyesFList = [get_draw_fun_from_module(m) for m in theme["eyesShape"]]

    cells = len(matrix[0])
    width = height = cells*24

    modMatrix = matrix_remove_eyes(matrix)

    defs = Element('defs')

    g_outer_no_mask = Element('g')
    g_outer_mask = Element('g')
    g_dots_matrix = drawDotsFun(modMatrix)

    g = random_g.gen(239856329867)

    def dots_random():
        return math.floor(next(g)*len(dots_colors))

    dots_colors = theme["dotsColor"]["colors"]
    match theme["dotsColor"]["type"]:
        case 'one':
            g_dots_matrix.add_attribute('fill', dots_colors[0])
        case "gradient":
            gradiant = Element('linearGradient')
            gradiant.add_attribute('id', IDDotsFill)
            for index, color in enumerate(dots_colors):
                stop = Element('stop')
                stop.add_attribute(
                    'offset', f"{int(100/len(dots_colors) * index)}%")
                stop.add_attribute("stop-color", color)
                gradiant.append_child(stop)
            defs.append_child(gradiant)

            mask = Element("mask")
            mask.add_attribute("id", IDDotsMask)

            l = deepcopy(g_dots_matrix)
            l.add_attribute('fill', 'white')
            mask.append_child(l)

            g_dots_matrix.children = []
            defs.append_child(mask)

            rec_mask = draw_rect(0, 0, width, height)
            rec_mask.add_attribute('mask', f'url(#{IDDotsMask})')
            rec_mask.add_attribute('fill', f"url(#{IDDotsFill})")
            g_outer_mask.append_child(rec_mask)

        case  "multicolor":
            g = random_g.gen(239856329867)
            for x in g_dots_matrix.children:
                x.add_attribute('fill', dots_colors[dots_random()])

    g_eyes = Element('g')
    g_eyes.children = [dEyesFList[0](0, 0), dEyesFList[1](
        cells-7, 0), dEyesFList[2](0, cells-7,)]
    to_remove = []
    for index, options in enumerate(theme["eyesColor"]):

        dots_colors = options["colors"]
        position = 'tl'
        if index == 0:
            position = 'tl'
        elif index == 1:
            position = 'tr'
        elif index == 2:
            position = 'bl'

        match options["type"]:
            case 'one':
                g_eyes.children[index].add_attribute('fill', dots_colors[0])

            case "gradient":
                gradiant = Element('linearGradient')
                gradiant.add_attribute('id', IDEyesFill(position))

                for i, color in enumerate(dots_colors):
                    stop = Element('stop')
                    stop.add_attribute(
                        'offset', f"{int(100/len(dots_colors) * i)}%")
                    stop.add_attribute("stop-color", color)
                    gradiant.append_child(stop)

                defs.append_child(gradiant)
                mask = Element("mask")
                mask.add_attribute("id", IDEyesMask(position))

                to_remove.append(g_eyes.children[index])
                l = deepcopy(g_eyes.children[index])
                l.add_attribute('fill', 'white')
                mask.append_child(l)

                defs.append_child(mask)
                rec_mask: Element
                match(position):
                    case "tl":
                        rec_mask = draw_rect(0, 0, 7*24, 7*24)
                    case "tr":
                        rec_mask = draw_rect(width-7*24, 0, width, 7*24)
                    case "bl":
                        rec_mask = draw_rect(0, height-7*24, 7*24, height)

                rec_mask.add_attribute('mask', f'url(#{IDEyesMask(position)})')
                rec_mask.add_attribute('fill', f"url(#{IDEyesFill(position)})")
                g_outer_mask.append_child(rec_mask)
    for r in to_remove:
        g_eyes.children.remove(r)
    svg = Element('svg')
    svg.append_child(defs)
    g_outer_no_mask.append_child(g_dots_matrix)
    g_outer_no_mask.append_child(g_eyes)
    svg.append_child(g_outer_no_mask)
    svg.append_child(g_outer_mask)

    svg.add_attribute("width", str(width))
    svg.add_attribute("height", str(height))
    svg.add_attribute("viewBox", f"0 0 {width} {height}")
    svg.add_attribute("xmlns", "http://www.w3.org/2000/svg")
    svg.add_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
    return svg.to_text()


def main():
    theme_config = theme.select()
    matrix = make_matrix("https://vjxdev.github.io")
    code = draw_code(matrix, theme_config)
    with open('./output/out.svg', 'w', encoding="utf-8")as file:
        file.write(code)


if __name__ == "__main__":
    main()
