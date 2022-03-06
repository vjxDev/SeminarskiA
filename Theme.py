

from my_types import ColorsType, ModuleType, ThemeType
from ColorPicker import ColorPicerFormat, colorPicker
from helper import hex_to_rgb, rgb_to_hex
import import_files

import json
import inquirer

from blessed import Terminal
term = Terminal()


def select() -> ThemeType:
    themes = import_files.themes()
    themes.sort(key=lambda the: the['name'])
    options = []

    def printCubeWithColor(color: str):
        r, g, b = hex_to_rgb(color)
        return term.color_rgb(r, g, b)

    for t in themes:
        o = t['dotsColor']['colors']

        options.append(
            f"{t['name']}:"+"".join(printCubeWithColor(i)+'◼' for i in o))

    selectedTheme = inquirer.list_input(
        message='Select theme',
        choices=options
    )

    return themes[options.index(selectedTheme)]


def oneColorChoice(colors: ColorsType) -> tuple[int, int, int]:
    c = ['Manual input', 'Color picker', 'Select color from files']
    inputChoioce = inquirer.list_input(
        message="How do you want to select your colors", choices=c)
    match inputChoioce:
        case 'Manual input':
            while True:
                # [ ] LATER! : validate=lambda _, c: 0 <= int(c) <= 255 is not working

                r = input('Input the red color ')
                g = input('Input the greean color ')
                b = input('Input the blue color ')

                if 0 <= int(r) and int(r) <= 255 and 0 <= int(g) and int(g) <= 255 and 0 <= int(b) and int(b) <= 255:
                    return int(r), int(g), int(b)
                print("Error during input")
        case 'Color picker':
            return colorPicker()
        case 'Select color from files':
            options: list[ColorPicerFormat] = []

            for value in colors:
                r, g, b = hex_to_rgb(value['color'])
                options.append({'name': value['name'], 'color': (r, g, b)})

            return colorPicker(options)


def inputColors(colors: ColorsType, options: list[str] = ["One color", "Gradient", "Multi Color"], ) -> dict[str, list[str]]:

    colorType = inquirer.list_input(
        message="Select color type", choices=options)
    returnObject = {}
    match colorType:
        case 'One color':
            color = oneColorChoice(colors)
            return {'type': "one", 'colors': [rgb_to_hex(color)]}
        case "Multi Color":
            returnObject = {'type': 'multicolor', 'colors': []}
            keepOnGoing = True
            while keepOnGoing:
                color = oneColorChoice(colors)
                returnObject['colors'].append(rgb_to_hex(color))
                keepOnGoing = inquirer.confirm("Add more colors")
            return returnObject

        case  "Gradient":
            returnObject = {
                'type': 'gradient', 'colors': []}
            keepOnGoing = True
            while keepOnGoing:
                color = oneColorChoice(colors)
                returnObject['colors'].append(rgb_to_hex(color))
                keepOnGoing = inquirer.confirm("Add more colors")
            return returnObject


def inputDotsShape() -> ModuleType:
    shapes = import_files.shapes()
    options = [shape['name'] for shape in shapes]
    selected = inquirer.list_input("Input the dots shape", choices=options)
    index = options.index(selected)
    return shapes[index]


def inputEyesShape() -> tuple[ModuleType, ModuleType, ModuleType]:
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


def create() -> ThemeType:
    colors = import_files.colors()
    name = ""
    while True:
        name = input("Name your theme ")
        if name != "":
            break
        print("Unesite ime")

    dotsOptions = ["One color", "Gradient", "Multi Color"]
    eyesOptions = ["One color", "Gradient"]
    print("Input the dots colors:")
    dotsColor = inputColors(colors, dotsOptions)
    dotsShape = inputDotsShape()

    eyesColors = []
    print("Input top eye tl colors: ")
    eyesColors.append(inputColors(colors, eyesOptions))
    print("Input top eye tr colors: ")
    eyesColors.append(inputColors(colors, eyesOptions))
    print("Input top eye bl colors: ")
    eyesColors.append(inputColors(colors, eyesOptions))

    eyesShape = inputEyesShape()
    theme: ThemeType = {
        'name': name,
        'dotsColor': dotsColor,
        'dotsShape': dotsShape,
        'eyesColor': eyesColors,
        'eyesShape': eyesShape
    }
    return theme


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
