from Element import Element


def hex_to_rgb(hex_string):
    r_hex = hex_string[1:3]
    g_hex = hex_string[3:5]
    b_hex = hex_string[5:7]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def rgb_to_hex(colortuple: tuple[int, int, int]):
    return '#' + ''.join(f'{i:02X}' for i in colortuple)


cellSize = 24
padding = 1


def addPadding(modMatrix, padding=padding):
    cells = len(modMatrix[0])
    padMatrix = [[False for x in range(cells+padding*2)]
                 for x in range(cells+padding*2)]
    for rowIndex in range(cells):
        for elementIndex in range(cells):
            padMatrix[rowIndex+padding][elementIndex +
                                        padding] = modMatrix[rowIndex][elementIndex]
    return padMatrix


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
