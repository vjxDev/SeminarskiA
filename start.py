import inquirer
from DrawCode import drawCode
from Theme import createTheme, selectTheme
from my_types import ThemeType
from Form import startForm
from Make_qrcode import debugPrintQrCode, makeCode
import json


def option1():
    c = ["Create a theme", "Use a saved theme"]
    a = inquirer.list_input("Theme option", choices=c)
    theme: ThemeType = {}
    match a:
        case "Create a theme":
            theme = createTheme()
            save = inquirer.confirm("Save this theme")
            if save:
                with open(f'mods/themes/{theme["name"]}.json', 'w+') as file:
                    json.dump(theme, file)

        case "Use a saved theme":
            theme = selectTheme()
    print("\n"*3)
    qrcodeString = startForm()
    qrCodeMatrix = makeCode(qrcodeString)
    stringCode = drawCode(qrCodeMatrix, theme)
    with open('./output/out.svg', 'w', encoding="utf-8")as file:
        file.write(stringCode)
    print("\n\n Kod je uspesno napravljen!")


def main():
    c = ["Create new QR code",
         "Create new QR code theme",
         "Drew statistics graph"]
    goAgain = True
    while goAgain:
        a = inquirer.list_input("Welcome", choices=c)
        match a:
            case "Create new QR code":
                option1()

            case "Create new QR code theme":
                theme = createTheme()
                with open(f'mods/themes/{theme["name"]}.json', 'w+') as file:
                    json.dump(theme, file)

            case "Drew statistics graph":
                pass

        goAgain = inquirer.confirm("Run the program again")


if __name__ == "__main__":
    main()
