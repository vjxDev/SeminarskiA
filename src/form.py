from typing import Literal, TypedDict
import inquirer
from inquirer import themes
import re

formOptions = Literal['text', 'URL', 'WI-FI', 'contact', 'event', 'call']


class WiFi(TypedDict):
    wifiname: str
    hasPassword: bool
    isHidden: bool
    password: str
    type: Literal["WAP/WAP2", "WEP"]


def form() -> str:
    questions = [
        inquirer.List(
            'type',
            message='Select qrcode type',
            choices=['text', 'URL', 'WI-FI', 'contact', 'event', 'call']
        )
    ]
    answers = inquirer.prompt(questions, theme=themes.GreenPassion())
    selected: formOptions = answers['type']
    match selected:
        case 'text':
            questions = [inquirer.Text('text', "Imput some text")]
            answers = inquirer.prompt(questions, theme=themes.GreenPassion())
            text = answers['text']
            return text

        case 'URL':
            t = ""
            while(True):
                questions = [inquirer.Text(
                    'text', f"Imput a url {t}", default="https://")]
                answers = inquirer.prompt(
                    questions, theme=themes.GreenPassion())
                text = answers['text']
                regex = re.compile(
                    r'^https?://'
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
                    r'localhost|'
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                    r'(?::\d+)?'
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                test = regex.search(text)
                if test != None:
                    return text
                else:
                    t = "!!! Add https:// or http:// at the start !!! - "

        case 'WI-FI':
            wifi: WiFi = {}
            questions1 = [
                inquirer.Text('wifiname', message="WiFi name (SSID):"),
                inquirer.Checkbox(
                    'options', message="Options ", choices=["Is your wifi hidden", "Dose your WiFi have a password"], default=False),
            ]
            answers1 = inquirer.prompt(questions1, theme=themes.GreenPassion())
            wifi["password"] = ''
            wifi['wifiname'] = answers1['wifiname']

            options = {v: True for v in answers1['options']}
            wifi['isHidden'] = options.get("Is your wifi hidden", False)
            wifi['hasPassword'] = options.get(
                "Dose your WiFi have a password", False)

            if(wifi['hasPassword']):
                questions2 = [
                    inquirer.Text('password', message="Password"),
                    inquirer.List(
                        'type', message="WiFi type", choices=["WEP", "WPA/WPA2"]),
                ]
                answers2 = inquirer.prompt(
                    questions2, theme=themes.GreenPassion())
                wifi.update(answers2)

            out = wifi_to_text(wifi)

            return out

        case 'contact':
            name = inquirer.text("Name")
            company = inquirer.text("Company")
            title = inquirer.text("Title")
            tel = inquirer.text("Telphone")
            site = inquirer.text("Web site")
            email = inquirer.text("Email")
            address = inquirer.text("Address")
            memo = inquirer.text("Memo/Note")

            out = f"""BEGIN:VCARD
VERSION:3.0
{name!="" and f"N:{name}"}
{company!="" and f"ORG:{company}"}
{title!="" and f"TITLE:{title}"}
{tel!="" and f"TEL:+{tel}"}
{site!="" and f"URL:{site}"}
{email!="" and f"EMAIL{email}"}
{address!="" and f"ADR:{address}"}
{memo!="" and f"NOTE:{memo}"}
END:VCARD"""
            return out
        case 'event':
            print("event")
        case 'call':
            print("call")

    return "add me"


def wifi_to_text(wifi):
    out = f"WIFI:T:"
    if wifi['hasPassword']:
        if wifi['type'] == "WEP":
            out += "WEP"
        else:
            out += "WPA"
    else:
        out += "nopass"
    out += f";S:{wifi['wifiname']};P:{wifi['password']};"
    if wifi['isHidden']:
        out += "H:true"
    out += ";"
    return out


if __name__ == "__main__":
    form()
