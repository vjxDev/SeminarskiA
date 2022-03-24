from typing import Literal
import inquirer

import re

AnswerType = Literal['text', 'URL', 'WI-FI', 'contact', 'event', 'call']


def start() -> str:

    answers = inquirer.list_input(
        message='Select qrcode type',
        choices=['text', 'URL', 'WI-FI', 'contact', 'event', 'call']
    )
    selected: AnswerType = answers
    match selected:
        case 'text':
            text = input("Input some text ")
            return text
        case 'URL':
            url_text = ""
            while(True):
                text = input(f"Input a url {url_text} ")
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
                    url_text = "!!! Add http:// or https:// at the start !!! - "
        case 'WI-FI':
            return form_WIFI()
        case 'contact':
            return from_contact()
        case 'event':
            return fileIn()
        case 'call':
            # [ ] - Call
            print("call")

    return "add me"


def form_WIFI() -> str:
    wifiname: str = input("WiFi name (SSID) ")
    has_password: bool = False
    hidden: bool = False
    password: str = ""
    type: Literal["WAP/WAP2", "WEP"]

    answers1 = inquirer.checkbox(
        message="Options ", choices=["Is your wifi hidden", "Dose your WiFi have a password"], default=False),

    options = {v: True for v in answers1[0]}
    hidden = options.get("Is your wifi hidden", False)
    has_password = options.get(
        "Dose your WiFi have a password", False)

    if(has_password):
        password = input("Password "),
        type = inquirer.list_input(
            message="WiFi type", choices=["WEP", "WPA/WPA2"]),

    out = f"WIFI:T:"
    if has_password:
        if type == "WEP":
            out += "WEP"
        else:
            out += "WPA"
    else:
        out += "nopass"
    out += f";S:{wifiname};P:{password};"
    if hidden:
        out += "H:true"
    out += ";"
    return out


def from_contact():
    name = input("Name ")
    company = input("Company ")
    title = input("Title ")
    tel = input("Telphone ")
    site = input("Web site ")
    email = input("Email ")
    address = input("Address ")
    memo = input("Memo/Note ")

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

# [ ] TODO


def fileIn() -> str:
    return "kjsrhg"


if __name__ == "__main__":
    print(start())
