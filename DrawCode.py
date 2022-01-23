from importlib.machinery import SourceFileLoader
from copy import copy, deepcopy
import math
from typing import Callable

from Generator import generator
from Theme import selectTheme
from Make_qrcode import makeCode
from my_types import ModuleType, ThemeType
from Element import Element
from helper import drawRect, getDrawFromModule


def matrixWithoutEyes(list: list[list[bool]]) -> list[list[bool]]:
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


def drawCode(matrix: list[list[bool]], theme: ThemeType) -> str:

    drawDotsFun = getDrawFromModule(theme["dotsShape"])
    dEyesFList = [getDrawFromModule(m) for m in theme["eyesShape"]]

    cells = len(matrix[0])
    width = height = cells*24

    modMatrix = matrixWithoutEyes(matrix)

    defs = Element('defs')

    outerNoMaskG = Element('g')
    outerMaskG = Element('g')
    dotsMatrixG = drawDotsFun(modMatrix)

    g = generator(239856329867)

    def dotsRandom():
        return math.floor(next(g)*len(dotsColors))
    dotsColors = theme["dotsColor"]["colors"]
    match theme["dotsColor"]["type"]:
        case 'one':
            dotsMatrixG.add_attribute('fill', dotsColors[0])
        case "gradient":
            gradiant = Element('linearGradient')
            gradiant.add_attribute('id', IDDotsFill)
            for index, color in enumerate(dotsColors):
                stop = Element('stop')
                stop.add_attribute(
                    'offset', f"{int(100/len(dotsColors) * index)}%")
                stop.add_attribute("stop-color", color)
                gradiant.append_child(stop)
            defs.append_child(gradiant)

            mask = Element("mask")
            mask.add_attribute("id", IDDotsMask)

            l = deepcopy(dotsMatrixG)
            l.add_attribute('fill', 'white')
            mask.append_child(l)

            dotsMatrixG.children = []
            defs.append_child(mask)

            recMask = drawRect(0, 0, width, height)
            recMask.add_attribute('mask', f'url(#{IDDotsMask})')
            recMask.add_attribute('fill', f"url(#{IDDotsFill})")
            outerMaskG.append_child(recMask)

        case  "multicolor":
            g = generator(239856329867)
            for x in dotsMatrixG.children:
                x.add_attribute('fill', dotsColors[dotsRandom()])

    eyesG = Element('g')
    eyesG.children = [dEyesFList[0](0, 0), dEyesFList[1](
        cells-7, 0), dEyesFList[2](0, cells-7,)]
    toRemove = []
    for index, options in enumerate(theme["eyesColor"]):

        dotsColors = options["colors"]
        position = 'tl'
        if index == 0:
            position = 'tl'
        elif index == 1:
            position = 'tr'
        elif index == 2:
            position = 'bl'

        match options["type"]:
            case 'one':
                eyesG.children[index].add_attribute('fill', dotsColors[0])

            case "gradient":
                gradiant = Element('linearGradient')
                gradiant.add_attribute('id', IDEyesFill(position))

                for i, color in enumerate(dotsColors):
                    stop = Element('stop')
                    stop.add_attribute(
                        'offset', f"{int(100/len(dotsColors) * i)}%")
                    stop.add_attribute("stop-color", color)
                    gradiant.append_child(stop)

                defs.append_child(gradiant)
                mask = Element("mask")
                mask.add_attribute("id", IDEyesMask(position))

                toRemove.append(eyesG.children[index])
                l = deepcopy(eyesG.children[index])
                l.add_attribute('fill', 'white')
                mask.append_child(l)

                defs.append_child(mask)
                recMask: Element
                match(position):
                    case "tl":
                        recMask = drawRect(0, 0, 7*24, 7*24)
                    case "tr":
                        recMask = drawRect(width-7*24, 0, width, 7*24)
                    case "bl":
                        recMask = drawRect(0, height-7*24, 7*24, height)

                recMask.add_attribute('mask', f'url(#{IDEyesMask(position)})')
                recMask.add_attribute('fill', f"url(#{IDEyesFill(position)})")
                outerMaskG.append_child(recMask)
    for r in toRemove:
        eyesG.children.remove(r)
    svg = Element('svg')
    svg.append_child(defs)
    outerNoMaskG.append_child(dotsMatrixG)
    outerNoMaskG.append_child(eyesG)
    svg.append_child(outerNoMaskG)
    svg.append_child(outerMaskG)

    svg.add_attribute("width", str(width))
    svg.add_attribute("height", str(height))
    svg.add_attribute("viewBox", f"0 0 {width} {height}")
    svg.add_attribute("xmlns", "http://www.w3.org/2000/svg")
    svg.add_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
    return svg.to_text()


def main():
    theme = selectTheme()
    matrix = makeCode("https://vjxdev.github.io")
    code = drawCode(matrix, theme)
    with open('./output/out.svg', 'w', encoding="utf-8")as file:
        file.write(code)


if __name__ == "__main__":
    main()
