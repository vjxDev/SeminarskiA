import inquirer
from analytics import add_theme, create_report
import qr_code
import theme
from my_types import ThemeType
import form

import json
from datetime import datetime


def option_create_qrcode():
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
    add_theme(theme_config)
    print("\n"*3)
    string_data = form.start()
    code_matrix = qr_code.make_matrix(string_data)
    code_svg = qr_code.draw_code(code_matrix, theme_config)

    with open('./output/out.svg', 'w', encoding="utf-8") as file:
        file.write(code_svg)
    date_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(f'./output/archive/{date_string}.svg', 'w', encoding="utf-8") as file:
        file.write(code_svg)
    print("\n\n QRCode Successfuly created")


def option_create_theme():
    theme_config = theme.create()
    add_theme(theme_config)
    with open(f'mods/themes/{theme_config["name"]}.json', 'w+') as file:
        json.dump(theme_config, file)


def option_draw_stats():
    create_report()
    pass


def main():
    choices = ["Create new QR code",
               "Create new QR code theme",
               "Drew statistics graph"]
    go_again = True
    while go_again:
        a = inquirer.list_input("Welcome", choices=choices)
        match a:
            case "Create new QR code":
                option_create_qrcode()

            case "Create new QR code theme":
                option_create_theme()

            case "Drew statistics graph":
                option_draw_stats()
        go_again = inquirer.confirm("Run the program again")


if __name__ == "__main__":
    main()
