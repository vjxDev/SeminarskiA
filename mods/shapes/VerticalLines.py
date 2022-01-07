from src.Element import Element
from src.helper import addPadding, cellSize, drawRect, drawCircle
import math


def draw(matrix: list[list[bool]]) -> Element:
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
