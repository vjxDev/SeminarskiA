import random
import requests


def rad():
    return ''.join(random.choices(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"], k=6))


print(rad())

for i in range(500):
    x = requests.get(
        f"https://api.color.pizza/v1/{rad()}")
    data = x.json()
    color = data["colors"][0]
    name: str = color["name"]
    name = name.replace(" ", "")
    hex = color["hex"]
    with open(f"./default/colors/{name}.txt", "w") as f:
        f.write(hex)
    print(hex)
