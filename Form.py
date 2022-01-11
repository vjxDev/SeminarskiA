from typing import Literal
import inquirer

import re

formOptions = Literal['text', 'URL', 'WI-FI', 'contact', 'event', 'call']


def startForm() -> str:

    answers = inquirer.list_input(
        message='Select qrcode type',
        choices=['text', 'URL', 'WI-FI', 'contact', 'event', 'call']
    )
    selected: formOptions = answers
    match selected:
        case 'text':
            text = input("Input some text")
            return text
        case 'URL':
            t = ""
            while(True):
                text = input(f"Input a url {t}")
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
            return WIFIIn()
        case 'contact':
            return contactIn()
        case 'event':
            return fileIn()
        case 'call':
            print("call")

    return "add me"


def WIFIIn() -> str:
    wifiname: str = input("WiFi name (SSID)")
    hasPassword: bool = False
    isHidden: bool = False
    password: str = ""
    type: Literal["WAP/WAP2", "WEP"]

    answers1 = inquirer.checkbox(
        message="Options ", choices=["Is your wifi hidden", "Dose your WiFi have a password"], default=False),
    print(answers1[0])
    options = {v: True for v in answers1[0]}
    isHidden = options.get("Is your wifi hidden", False)
    hasPassword = options.get(
        "Dose your WiFi have a password", False)

    if(hasPassword):
        password = input("Password"),
        type = inquirer.list_input(
            message="WiFi type", choices=["WEP", "WPA/WPA2"]),

    out = f"WIFI:T:"
    if hasPassword:
        if type == "WEP":
            out += "WEP"
        else:
            out += "WPA"
    else:
        out += "nopass"
    out += f";S:{wifiname};P:{password};"
    if isHidden:
        out += "H:true"
    out += ";"
    return out


def contactIn():
    name = input("Name")
    company = input("Company")
    title = input("Title")
    tel = input("Telphone")
    site = input("Web site")
    email = input("Email")
    address = input("Address")
    memo = input("Memo/Note")

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


def fileIn() -> str:
    return "kjsrhg"


if __name__ == "__main__":
    print(startForm())
