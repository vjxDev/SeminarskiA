from importlib.machinery import SourceFileLoader

from Make_qrcode import makeCode
from src.Element import Element


def main():
    foo = SourceFileLoader(
        "VerticalLines", "./mods\shapes\VerticalLines.py").load_module()
    # Problem za buduceg mene
    # [ ] - Poglredaj kako se radi sa ovim cudom i da li mogu da iimportujem preko putanje ili mora sa tackama(.)

    el: Element = foo.draw(makeCode("https://vjxdev.github.io"))
    print(hasattr(foo, "draw"))


if __name__ == "__main__":
    main()
