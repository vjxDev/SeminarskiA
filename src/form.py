from typing import Literal
import inquirer
from inquirer import themes
import re

formOptions = Literal['text', 'URL', 'WI-FI', 'contact', 'event', 'call']


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
            print("WI-FI")
        case 'contact':
            print("contact")
        case 'event':
            print("event")
        case 'call':
            print("call")

    return "add me"


if __name__ == "__main__":
    form()
