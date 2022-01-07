from src.form import startForm
from src.import_files import getAll
from src.make_qrcode import makeCode


def styleImput():
    print("style")


def main():
    text: str = startForm()
    styleImput()
    matrix = makeCode(text)


if __name__ == "__main__":
    main()
