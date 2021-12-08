from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L


def make(string: str) -> list[list[bool]]:
    code = QRCode(border=0, error_correction=ERROR_CORRECT_L)
    code.add_data(string)
    code.make()
    matrix = code.get_matrix()
    return matrix


def debugPrintQrCode(matrix: list[list[bool]]):
    for row in matrix:
        for el in row:
            if el:
                print("⬜", end="")
            else:
                print("⬛", end="")
        print()


def main():
    matrix = make("hello")
    debugPrintQrCode(matrix)


if __name__ == "__main__":
    main()
