
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from typing import Callable, Generator, Literal, TypedDict
import math

from Make_qrcode import makeCode
from Element import Element
import copy

matrix: list[list[bool]] = makeCode("https://google.com")

cells = len(matrix[0])
width = height = cells*24

modMatrix = matrix


for rowIndex in range(cells):
    for elementIndex in range(cells):

        if rowIndex < 7 and elementIndex < 7:
            modMatrix[rowIndex][elementIndex] = False

        if rowIndex < 7 and elementIndex > cells-8:
            modMatrix[rowIndex][elementIndex] = False
        if rowIndex > cells-8 and elementIndex < 7:
            modMatrix[rowIndex][elementIndex] = False


padding = 1


def addPadding(modMatrix, padding=padding):
    padMatrix = [[False for x in range(cells+padding*2)]
                 for x in range(cells+padding*2)]
    for rowIndex in range(cells):
        for elementIndex in range(cells):
            padMatrix[rowIndex+padding][elementIndex +
                                        padding] = modMatrix[rowIndex][elementIndex]
    return padMatrix


cellSize = 24
svg = Element(type="svg")
svg.add_attribute("viewBox", f"0 0 {width} {height}")
svg.add_attribute("xmlns", "http://www.w3.org/2000/svg")
svg.add_attribute("xmlns:xlink", "http://www.w3.org/1999/xlink")

defs = Element('defs')
svg.append_child(defs)


def drawRect(startX, startY, width, height):
    el = Element("rect")
    el.add_attribute("x", str(startX))
    el.add_attribute("y", str(startY))
    el.add_attribute("width", str(width))
    el.add_attribute("height", str(height))
    return el


def drawCircle(startX, startY, width):
    el = Element('circle')
    el.add_attribute('cx', str(startX+width/2))
    el.add_attribute('cy', str(startY+width/2))
    el.add_attribute('r', str(width/2))
    return el


def drawRectCode(matrix: list[list[bool]]) -> Element:
    g = Element('g')
    for yIndex, row in enumerate(matrix):
        for xIndex, el in enumerate(row):
            if el:
                rect = drawRect(xIndex*24, yIndex*24, 24, 24)
                g.append_child(rect)
    return g


def drawHorisontalLinesCode(matrix: list[list[bool]]) -> Element:
    g = Element('g')
    pMatrix = addPadding(matrix, 1)

    size = 20
    for yIndex, row in enumerate(matrix):
        for xIndex, el in enumerate(row):
            if el:
                left = pMatrix[yIndex+1][xIndex-1+1]
                right = pMatrix[yIndex+1][xIndex+1+1]
                element: Element

                centerX = xIndex*cellSize+cellSize/2
                centerY = yIndex*cellSize+cellSize/2

                removed = (cellSize - size) / 2

                if left and right:
                    element = drawRect(
                        xIndex*cellSize, yIndex*cellSize + removed, 24, size)
                elif left or right:
                    element = Element('path')
                    element.add_attribute('d',
                                          f"M {xIndex*24} {yIndex*24 + removed}" +
                                          f"v {24-removed*2}" +
                                          f"h {24/2}"
                                          f"a {size/2} {size/2}, 0, 0, 0, 0 {-size}"
                                          )
                    if right:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi ) / math.pi},{centerX},{centerY})")
                else:
                    element = drawCircle(
                        xIndex*cellSize, yIndex*cellSize, size)

                g.append_child(element)
    return g


def drawVercialLinesCode(matrix: list[list[bool]]) -> Element:
    g = Element('g')
    pMatrix = addPadding(matrix, 1)

    size = 20
    for yIndex, row in enumerate(matrix):
        for xIndex, el in enumerate(row):
            if el:
                top = pMatrix[yIndex+1-1][xIndex+1]
                bottom = pMatrix[yIndex+1+1][xIndex+1]
                element: Element

                centerX = xIndex*cellSize+cellSize/2
                centerY = yIndex*cellSize+cellSize/2

                removed = (cellSize - size) / 2

                if top and bottom:
                    element = drawRect(xIndex*cellSize +
                                       removed, yIndex*cellSize, size, 24)
                elif top or bottom:
                    element = Element('path')
                    element.add_attribute('d',
                                          f"M {xIndex*24} {yIndex*24 + removed}" +
                                          f"v {24-removed*2}" +
                                          f"h {24/2}"
                                          f"a {size/2} {size/2}, 0, 0, 0, 0 {-size}"
                                          )
                    if top:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi ) / math.pi/2},{centerX},{centerY})")
                    if bottom:
                        element.add_attribute(
                            "transform", f"rotate({(180 * math.pi * -1) / math.pi/2},{centerX},{centerY})")
                else:
                    element = drawCircle(
                        xIndex*cellSize, yIndex*cellSize, size)
                g.append_child(element)
    return g


svg.append_child(drawHorisontalLinesCode(modMatrix))


def oko(x, y): return f"M{x*24+5.5*24} {y*24+24}a12 12 90 0112 12v96a12 12 90 01-12 12h-96a12 12 90 01-12-12v-96a12 12 90 0112-12h96m0-24h-108q-24 0-24 24v120q0 24 24 24h120q24 0 24-24v-120q0-24-24-24zm-84 54v60a6 6 90 006 6h60a6 6 90 006-6v-60a6 6 90 00-6-6h-60a6 6 90 00-6 6"


def drawEyes(tl: Callable[[int, int], str], tr: Callable[[int, int], str], bl: Callable[[int, int], str]) -> Element:
    gOci = Element('g')
    oci = [tl(0, 0), tr(0, cells-7), bl(cells-7, 0)]

    for d in oci:
        path = Element("path")
        path.add_attribute("d", d)
        path.add_attribute("fill", "black")
        path.add_attribute("fill-rule", "evenodd")
        gOci.append_child(path)
    return gOci


svg.append_child(drawEyes(oko, oko, oko))


class ColorSingle(TypedDict):
    type: Literal['single']
    colors: str


class ColorMulti(TypedDict):
    type: Literal['multi']
    colors: list[str]


class ColorGradient(TypedDict):
    type: Literal['gradient']
    colors: list[str]


ColorT = ColorSingle | ColorMulti | ColorGradient

c: ColorT = {
    'type': 'single',
    'color': 'red'
}

match(c["type"]):
    case 'single':

        codeG: Element = svg.children[1]

        clipPath = Element('clipPath')

        clipPath.add_attribute('id', 'clip-path-dots-color')
        clipPath.children = copy.deepcopy(codeG.children)
        svg.children[0].append_child(clipPath)
        svg.children[1].children = []

        recMask = drawRect(0, 0, width, height)
        recMask.add_attribute('clip-path', 'url(#clip-path-dots-color)')
        recMask.add_attribute('fill', str(c["color"]))

        svg.children[1].append_child(recMask)


svg.add_attribute("width", str(24*cells))
svg.add_attribute("height", str(24*cells))
svg.add_attribute("xmlns", "http://www.w3.org/2000/svg")
svgText = svg.to_text()


file = open('svg.svg', 'w', encoding="utf-8")
file.write(svgText)
file.close()


drawing = svg2rlg("svg.svg")


renderPM.drawToFile(drawing, "image.png", fmt="PNG")
