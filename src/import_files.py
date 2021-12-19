
from helper.my_types import colorsType, EyesType, ShapesType
import glob
import ntpath

folders = ('default', 'mods')
subfolders = ('colors', 'eyes', 'shapes')


def getColors() -> colorsType:
    colors: colorsType = []
    for folder in folders:
        for fileName in glob.glob(f'{folder}/colors/*.txt'):
            with open(fileName, 'r') as file:
                color = file.read()
                head, tail = ntpath.split(fileName)
                name, ext = ntpath.splitext(tail)
                colors.append({'name': name, 'color': color})

        for fileName in glob.glob(f'{folder}/colors/*.data'):
            with open(fileName, 'r') as file:
                for line in file:
                    line = line.strip()
                    name, color = tuple(line.split("|"))
                    colors.append({'name': name, 'color': color})

    return colors


def getEyes() -> EyesType:
    eyes: EyesType = []
    for folder in folders:
        for fileName in glob.glob(f'{folder}/eyes/*.txt'):
            with open(fileName, 'r') as file:
                eye = file.read()
                head, tail = ntpath.split(fileName)
                name, ext = ntpath.splitext(tail)
                eyes.append({'name': name, 'shape': eye})
    return eyes


def getShapes() -> ShapesType:
    shapes: ShapesType = []

    for folder in folders:
        for fileName in glob.glob(f'{folder}/shapes/*.txt'):
            head, tail = ntpath.split(fileName)
            name, ext = ntpath.splitext(tail)
            shapes.append({'name': name, 'path': fileName, 'type': 'file'})
        for fileName in glob.glob(f'{folder}/shapes/*.py'):
            head, tail = ntpath.split(fileName)
            name, ext = ntpath.splitext(tail)
            shapes.append({'name': name, 'path': fileName, 'type': 'module'})

    return shapes


def getAll():
    return (getColors(), getShapes(), getEyes())


def main():
    print(getColors())
    print(getEyes())
    print(getShapes())


if __name__ == '__main__':
    main()
