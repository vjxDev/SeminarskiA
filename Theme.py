

from my_types import ColorsType, ModuleType, ThemeType
from color_picker import ColorPicerFormat, color_picker
from helper import hex_to_rgb, rgb_to_hex
import import_files

import json
import inquirer

from blessed import Terminal
term = Terminal()


def printCubeWithColor(color: str):
    r, g, b = hex_to_rgb(color)
    return term.color_rgb(r, g, b)


def select() -> ThemeType:
    themes = import_files.themes()
    themes.sort(key=lambda the: the['name'])
    options = []

    for t in themes:
        o = t['dotsColor']['colors'] + t['eyesColor'][0]['colors'] + \
            t['eyesColor'][1]['colors'] + t['eyesColor'][2]['colors']

        options.append(
            f"{t['name']}:"+"".join(printCubeWithColor(i)+'◼' for i in o))

    selectedTheme = inquirer.list_input(
        message='Select theme',
        choices=options
    )
    return themes[options.index(selectedTheme)]


def create() -> ThemeType:
    colors = import_files.colors()
    name = ""
    while True:
        name = input("Name your theme ")
        if name != "":
            break
        print("Enter a name")

    option_dots = ["One color", "Gradient", "Multi Color"]
    option_eyes = ["One color", "Gradient"]
    print("Input the dots colors:")
    option_dots_colors = select_color(colors, option_dots)
    option_dots_shape = select_shape_dots()

    option_eyes_colors = []
    print("Input top eye top left colors: ")
    option_eyes_colors.append(select_color(colors, option_eyes))
    print("Input top eye top right colors: ")
    option_eyes_colors.append(select_color(colors, option_eyes))
    print("Input top eye bottom left colors: ")
    option_eyes_colors.append(select_color(colors, option_eyes))

    option_eyes_shape = select_shape_eyes()
    theme: ThemeType = {
        'name': name,
        'dotsColor': option_dots_colors,
        'dotsShape': option_dots_shape,
        'eyesColor': option_eyes_colors,
        'eyesShape': option_eyes_shape
    }
    return theme


def select_color_one(colors: ColorsType) -> tuple[int, int, int]:
    c = ['Manual input', 'Color picker', 'Select color from files']
    choce = inquirer.list_input(
        message="How do you want to select your colors", choices=c)
    match choce:
        case 'Manual input':
            while True:
                r = input('Input the red color ')
                g = input('Input the greean color ')
                b = input('Input the blue color ')

                if 0 <= int(r) and int(r) <= 255 and 0 <= int(g) and int(g) <= 255 and 0 <= int(b) and int(b) <= 255:
                    return int(r), int(g), int(b)
                print("Error during input")

        case 'Color picker':
            return color_picker()

        case 'Select color from files':
            options: list[ColorPicerFormat] = []
            for value in colors:
                r, g, b = hex_to_rgb(value['color'])
                options.append({'name': value['name'], 'color': (r, g, b)})
            return color_picker(options)


def select_color(colors: ColorsType, options: list[str] = ["One color", "Gradient", "Multi Color"], ) -> dict[str, list[str]]:
    color_type = inquirer.list_input(
        message="Select color type", choices=options)
    object = {}
    match color_type:
        case 'One color':
            color = select_color_one(colors)
            return {'type': "one", 'colors': [rgb_to_hex(color)]}
        case "Multi Color":
            object = {'type': 'multicolor', 'colors': []}
            keep_on_going = True
            while keep_on_going:
                color = select_color_one(colors)
                object['colors'].append(rgb_to_hex(color))
                keep_on_going = inquirer.confirm("Add more colors")
            return object

        case "Gradient":
            object = {'type': 'gradient', 'colors': []}
            keep_on_going = True
            while keep_on_going:
                color = select_color_one(colors)
                object['colors'].append(rgb_to_hex(color))
                keep_on_going = inquirer.confirm("Add more colors")
            return object


def select_shape_dots() -> ModuleType:
    shapes = import_files.shapes()
    options = [shape['name'] for shape in shapes]
    selected = inquirer.list_input("Input the dots shape", choices=options)
    index = options.index(selected)
    return shapes[index]


def select_shape_eyes() -> tuple[ModuleType, ModuleType, ModuleType]:
    shapes = import_files.eyes()
    options = [shape['name'] for shape in shapes]
    selectedTL = inquirer.list_input(
        "Select the eyes shape for top left", choices=options)
    indexTL = options.index(selectedTL)

    selectedTR = inquirer.list_input(
        "Select the eyes shape for top right ", choices=options)
    indexTR = options.index(selectedTR)

    selectedBL = inquirer.list_input(
        "Select the eyes shape for bottom left", choices=options)
    indexBL = options.index(selectedBL)
    return shapes[indexTL], shapes[indexTR], shapes[indexBL]


def main():
    create = True
    print(len(import_files.colors()))
    if(create):
        theme = create()
        with open(f'mods/themes/hello.json', 'w+') as file:
            json.dump(theme, file)
        print(theme)
    else:
        theme = select()
        print(theme)


if __name__ == "__main__":
    main()
