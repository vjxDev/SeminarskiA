from form import form
from import_files import getAll
from make_qrcode import debugPrintQrCode, make


def styleImput():
    print("style")


def main():
    print(getAll())
    text: str = form()
    styleImput()  # unos izgleda ... Oblik tipa json
    matrix = make(text)
    debugPrintQrCode(matrix)


if __name__ == "__main__":
    main()
