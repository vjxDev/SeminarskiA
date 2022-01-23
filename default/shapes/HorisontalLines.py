from Element import Element
from helper import addPadding, cellSize, drawRect, drawCircle
import math


def draw(matrix: list[list[bool]]) -> Element:
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
