from typing import Literal
import inquirer

import re
import regex_patern

AnswerType = Literal['Text', 'URL', 'WI-FI', 'Mail',
                     'Telephone', 'SMS', 'Contact']


def start() -> str:
    answers = inquirer.list_input(
        message='Select qrcode type',
        choices=['Text', 'URL', 'WI-FI', 'Mail',
                 'Telephone', 'SMS', 'Contact']  # 'Event
    )
    selected: AnswerType = answers
    match selected:
        case 'Text':
            text = input("Input some text ")
            return text
        case 'URL':
            return form_url()
        case 'WI-FI':
            return form_WIFI()
        case 'Mail':
            return form_mail()
        case 'Telephone':
            return form_tel()
        case 'SMS':
            return form_sms()
        case 'Contact':
            return form_contact()
        # case 'Event':
        #     return form_event()
    return "Error????"


def form_url() -> str:
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


def form_WIFI() -> str:
    wifiname: str = input("WiFi name (SSID) ")
    has_password: bool = False
    hidden: bool = False
    password: str = ""
    type: Literal["WAP/WAP2", "WEP"]

    answers1 = inquirer.checkbox(
        message="Options ", choices=["Is your WiFi hidden", "Does your WiFi have a password"], default=False),

    options = {v: True for v in answers1[0]}
    hidden = options.get("Is your WiFi hidden", False)
    has_password = options.get(
        "Does your WiFi have a password", False)

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


def form_mail() -> str:
    url_text = ""
    while(True):
        text = input(f"Input a mail {url_text} ")
        regex = re.compile(regex_patern.mail_regex)
        test = regex.search(text)
        if test != None:
            return text
        else:
            url_text = "!!! Incorect format !!! - "


def form_tel() -> str:
    phone = input("Enter a phone number: +")
    return 'tel:+'+phone


def form_sms() -> str:
    out = "sms:+" + input("Enter a phone number you whant to message: +")

    message = input("Enter a message (opcional):")
    if message != "":
        out += ":"+message
    return out


def form_contact():
    print("You can skip a option by pressing enter:")
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
"""
    if name != "":
        out += "N:"+name+'\n'
    if company != "":
        out += "ORG:"+company+'\n'
    if title != "":
        out += "TITLE:"+title+'\n'
    if tel != "":
        out += "TEL:+"+tel+'\n'
    if site != "":
        out += "URL:"+site+'\n'
    if email != "":
        out += "EMAIL:"+email+'\n'
    if address != "":
        out += "ADR:"+address+'\n'
    if memo != "":
        out += "NOTE:"+memo+'\n'

    return out+"END:VCARD"

# def form_event() -> str:
#     return "its hard"


if __name__ == "__main__":
    print(start())
