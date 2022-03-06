import math
import colorsys
from typing import TypedDict

from blessed import Terminal


term = Terminal()


class ColorPicerFormat(TypedDict):
    name: str
    color: tuple[int, int, int]


def sortby_hv(item: ColorPicerFormat):
    digit = 0
    hsv = colorsys.rgb_to_hsv(*item['color'])
    if item['color'][0] == item['color'][1] == item['color'][2]:
        return 100, hsv[2], digit
    return int(math.floor(hsv[0] * 100)), digit, hsv[2]


def color_table() -> list[ColorPicerFormat]:
    listOfRGB = []

    for r in range(16):
        for g in range(16):
            for b in range(16):
                listOfRGB.append((r*16, b*16, g*16))
    return [{'name': f"{item[0]}{item[1]}{item[2]}", "color": item} for item in listOfRGB]


def render(HSV_SORTED_COLORS: list[ColorPicerFormat], term: Terminal, selected_index: int, cache: str = ""):
    r, g, b = HSV_SORTED_COLORS[selected_index]['color']
    result = cache
    result += term.clear_eos + '\n'
    result += term.on_color_rgb(r, g, b) + term.clear_eos + '\n'
    result += term.normal + \
        term.center(f'{HSV_SORTED_COLORS[selected_index]["name"]}') + '\n'
    result += term.normal + term.center(
        f'{term.number_of_colors} colors - ')

    result += term.move_yx(selected_index // term.width,
                           selected_index % term.width)
    result += term.on_color_rgb(r, g, b)(" \b")
    return result


def next_color(color, forward):
    colorspaces = (4, 8, 16, 256, 1 << 24)
    next_index = colorspaces.index(color) + (1 if forward else -1)
    if next_index == len(colorspaces):
        next_index = 0
    return colorspaces[next_index]


def colorPicker(c: list[ColorPicerFormat] = color_table()) -> tuple[int, int, int]:
    HSV_SORTED_COLORS = sorted(c, key=sortby_hv)

    cache: str = term.home + term.normal + ''.join(
        term.color_rgb(HSV_SORTED_COLORS[i]['color'][0], HSV_SORTED_COLORS[i]['color'][1], HSV_SORTED_COLORS[i]['color'][2]) + '◼'+term.normal for i in range(len(HSV_SORTED_COLORS))
    )

    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        idx = len(HSV_SORTED_COLORS) // 2
        dirty = True
        while True:
            if dirty:
                outp = render(HSV_SORTED_COLORS, term, idx, cache)
                print(outp, end='', flush=True)
            with term.hidden_cursor():
                inp = term.inkey()
            dirty = True
            if inp.code == term.KEY_ENTER:
                return HSV_SORTED_COLORS[idx]['color']
            elif inp.code == term.KEY_LEFT or inp == 'h':
                idx -= 1
            elif inp.code == term.KEY_DOWN or inp == 'j':
                idx += term.width
            elif inp.code == term.KEY_UP or inp == 'k':
                idx -= term.width
            elif inp.code == term.KEY_RIGHT or inp == 'l':
                idx += 1

            elif inp != '\x0c':
                dirty = False

            while idx < 0:
                idx += len(HSV_SORTED_COLORS)
            while idx >= len(HSV_SORTED_COLORS):
                idx -= len(HSV_SORTED_COLORS)


if __name__ == '__main__':
    r, g, b = colorPicker()
    print(term.color_rgb(r, g, b)+"◼"+term.normal)
