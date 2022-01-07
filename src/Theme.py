

from src.my_types import ColorsType, EyeType, ShapeType, ThemeType
from src.ColorPicker import ColorPicerFormat, colorPicker
from src.helper import hex_to_rgb, rgb_to_hex
from src.import_files import getColors, getEyes, getShapes, getThemes

import json
import inquirer

from blessed import Terminal
term = Terminal()


def selectTheme() -> ThemeType:
    themes = getThemes()
    themes.sort(key=lambda the: the['name'])
    options = []

    def printCubeWithColor(color: str):
        r, g, b = hex_to_rgb(color)
        return term.color_rgb(r, g, b)

    for t in themes:
        o = t['dotsColor']['colors'] + t['eyesColor']['colors']
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
            # [ ] LATER! : validate=lambda _, c: 0 <= int(c) <= 255 is not working

            r = input('Input the red color')
            g = input('Input the greean color')
            b = input('Input the blue color')

            return int(r), int(g), int(b)
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


def inputDotsShape() -> ShapeType:
    shapes = getShapes()
    options = [shape['name'] for shape in shapes]
    selected = inquirer.list_input("Input the dots shape", choices=options)
    index = options.index(selected)
    return shapes[index]


def inputEyesShape() -> tuple[EyeType, EyeType, EyeType]:
    shapes = getEyes()
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


def createTheme() -> ThemeType:
    colors = getColors()
    name = input("Name your theme ")

    dotsOptions = ["One color", "Gradient", "Multi Color"]
    eyesOptions = ["One color", "Gradient"]
    print("Input the dots colors:")
    dotsColor = inputColors(colors, dotsOptions)
    dotsShape = inputDotsShape()

    print("Input the dots colors:")
    eyesColor = inputColors(colors, eyesOptions)
    eyesShape = inputEyesShape()
    theme: ThemeType = {
        'name': name,
        'dotsColor': dotsColor,
        'dotsShape': dotsShape,
        'eyesColor': eyesColor,
        'eyesShape': eyesShape
    }
    return theme


def main():
    create = False
    if(create):
        theme = createTheme()
        with open(f'mods/themes/hello.json', 'w+') as file:
            json.dump(theme, file)
        print(theme)
    else:
        theme = selectTheme()
        print(theme)


if __name__ == "__main__":
    main()
