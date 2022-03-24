
from my_types import ModuleType, ThemesType, ColorsType
import glob
import ntpath
import json

folders = ('default', 'mods')
subfolders = ('colors', 'eyes', 'shapes', 'themes')


def colors() -> ColorsType:
    colors: ColorsType = []
    for folder in folders:
        for file_name in glob.glob(f'{folder}/{subfolders[0]}/*.txt'):
            with open(file_name, 'r') as file:
                color = file.read()
                head, tail = ntpath.split(file_name)
                name, ext = ntpath.splitext(tail)
                colors.append({'name': name, 'color': color})

        for file_name in glob.glob(f'{folder}/{subfolders[0]}/*.colors'):
            with open(file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    name, color = tuple(line.split("|"))
                    colors.append({'name': name, 'color': color})
    return colors


def eyes() -> list[ModuleType]:
    eyes: list[ModuleType] = []
    for folder in folders:
        for file_name in glob.glob(f'{folder}/{subfolders[1]}/*.py'):
            head, tail = ntpath.split(file_name)
            name, ext = ntpath.splitext(tail)
            eyes.append({'name': name, 'path': file_name})
    return eyes


def shapes() -> list[ModuleType]:
    shapes: list[ModuleType] = []
    for folder in folders:
        for file_name in glob.glob(f'{folder}/{subfolders[2]}/*.py'):
            head, tail = ntpath.split(file_name)
            name, ext = ntpath.splitext(tail)
            shapes.append({'name': name, 'path': file_name})

    return shapes


def themes() -> ThemesType:
    themes: ThemesType = []
    for folder in folders:
        for file_name in glob.glob(f'{folder}/{subfolders[3]}/*.json'):
            with open(file_name, 'r') as file:
                json_data = json.load(file)
                themes.append(json_data)
    return themes


def simple_shpaes() -> list[ModuleType]:
    simple_shapes: list[ModuleType] = []

    for folder in folders:
        for file_name in glob.glob(f'{folder}/{subfolders[2]}/simple/*.py'):
            head, tail = ntpath.split(file_name)
            name, ext = ntpath.splitext(tail)
            simple_shapes.append({'name': name, 'path': file_name})

    return simple_shapes


def main():
    print(colors())
    print(eyes())
    print(shapes())
    print(themes())
    print(simple_shpaes())


if __name__ == '__main__':
    main()
