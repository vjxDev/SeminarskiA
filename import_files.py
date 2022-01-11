
from my_types import ModuleType, ThemesType, ColorsType
import glob
import ntpath
import json

folders = ('default', 'mods')
subfolders = ('colors', 'eyes', 'shapes', 'themes')


def getColors() -> ColorsType:
    colors: ColorsType = []
    for folder in folders:
        for fileName in glob.glob(f'{folder}/{subfolders[0]}/*.txt'):
            with open(fileName, 'r') as file:
                color = file.read()
                head, tail = ntpath.split(fileName)
                name, ext = ntpath.splitext(tail)
                colors.append({'name': name, 'color': color})

        for fileName in glob.glob(f'{folder}/{subfolders[0]}/*.data'):
            with open(fileName, 'r') as file:
                for line in file:
                    line = line.strip()
                    name, color = tuple(line.split("|"))
                    colors.append({'name': name, 'color': color})

    return colors


def getEyes() -> list[ModuleType]:
    eyes: list[ModuleType] = []
    for folder in folders:

        for fileName in glob.glob(f'{folder}/{subfolders[1]}/*.py'):
            head, tail = ntpath.split(fileName)
            name, ext = ntpath.splitext(tail)
            eyes.append({'name': name, 'path': fileName, })
    return eyes


def getShapes() -> list[ModuleType]:
    shapes: list[ModuleType] = []

    for folder in folders:
        for fileName in glob.glob(f'{folder}/{subfolders[2]}/*.py'):
            head, tail = ntpath.split(fileName)
            name, ext = ntpath.splitext(tail)
            shapes.append({'name': name, 'path': fileName})

    return shapes


def getThemes() -> ThemesType:
    themes: ThemesType = []
    for folder in folders:
        for fileName in glob.glob(f'{folder}/{subfolders[3]}/*.json'):
            with open(fileName, 'r') as file:
                jsonData = json.load(file)
                themes.append(jsonData)
    return themes


def main():
    print(getColors())
    print(getEyes())
    print(getShapes())
    print(getThemes())


print(__name__)

if __name__ == '__main__':
    main()
