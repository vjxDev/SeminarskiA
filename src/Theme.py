import json
import inquirer
from inquirer import themes
from ColorPicker import ColorPicerFormat, colorPicker
from helper import hex_to_rgb, rgb_to_hex
from import_files import getColors, getThemes
from my_types import ColorsType, ThemeType

from blessed import Terminal
term = Terminal()


def selectTheme() -> ThemeType:
    themes = getThemes()
    themes.sort(key=lambda the: the['name'])
    printStrings = []

    def printCubeWithColor(color: str):
        r, g, b = hex_to_rgb(color)
        return term.color_rgb(r, g, b)

    for t in themes:
        printStrings.append(
            f"{t['name']}:"+"".join(printCubeWithColor(i)+'◼' for i in t['colors']))

    selectedTheme = inquirer.list_input(
        message='Select theme',
        choices=printStrings
    )

    return themes[printStrings.index(selectedTheme)]


def validate(_, current):
    print(current)

    number = int(current, base=10)
    return 0 <= number <= 255


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


def createTheme() -> ThemeType:
    name = input("Name your theme")
    colors = getColors()
    c = ["one", "gradient", "multicolor"]
    colorType = inquirer.list_input(message="Select color type", choices=[
                                    "One color", "Gradient", "Multi Color"])
    theme: ThemeType = {}

    match colorType:
        case 'One color':
            color = oneColorChoice(colors)
            return {'name': name, 'type': "one", 'colors': [rgb_to_hex(color)]}
        case "Multi Color":
            theme = {'name': name, 'type': 'multicolor', 'colors': []}
            keepOnGoing = True
            while keepOnGoing:
                color = oneColorChoice(colors)
                theme['colors'].append(rgb_to_hex(color))
                keepOnGoing = inquirer.confirm("Add more colors")
            return theme

        case  "Gradient":
            theme = {'name': name,
                     'type': 'gradient', 'colors': []}
            keepOnGoing = True
            while keepOnGoing:
                color = oneColorChoice(colors)
                theme['colors'].append(rgb_to_hex(color))
                keepOnGoing = inquirer.confirm("Add more colors")
            return theme


def main():
    theme = createTheme()
    with open(f'mods/themes/hello.json', 'w+') as file:
        json.dump(theme, file)
    print(theme)


if __name__ == "__main__":
    main()
