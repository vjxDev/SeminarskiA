import inquirer
import qr_code
import theme
from my_types import ThemeType
import form

import json
from datetime import datetime


def option1():
    c = ["Create a theme", "Use a saved theme"]
    a = inquirer.list_input("Theme option", choices=c)
    theme_config: ThemeType = {}
    match a:
        case "Create a theme":
            theme_config = theme.create()
            save = inquirer.confirm("Save this theme")
            if save:
                with open(f'mods/themes/{theme_config["name"]}.json', 'w+') as file:
                    json.dump(theme_config, file)

        case "Use a saved theme":
            theme_config = theme.select()

    print("\n"*3)

    code_matrix = qr_code.make_matrix(form.start())
    code_svg = qr_code.draw_code(code_matrix, theme_config)
    with open('./output/out.svg', 'w', encoding="utf-8") as file:
        file.write(code_svg)
    now = datetime.now()

    with open(f'./output/archive/{now.strftime("%d-%m-%Y-%H-%M-%S")}.svg', 'w', encoding="utf-8") as file:
        file.write(code_svg)
    print("\n\n Kod je uspesno napravljen!")


def main():
    choices = ["Create new QR code",
               "Create new QR code theme",
               "Drew statistics graph"]
    go_again = True
    while go_again:
        a = inquirer.list_input("Welcome", choices=choices)
        match a:
            case "Create new QR code":
                option1()

            case "Create new QR code theme":
                theme_config = theme.create()
                with open(f'mods/themes/{theme_config["name"]}.json', 'w+') as file:
                    json.dump(theme_config, file)

            case "Drew statistics graph":
                pass
        go_again = inquirer.confirm("Run the program again")


if __name__ == "__main__":
    main()
