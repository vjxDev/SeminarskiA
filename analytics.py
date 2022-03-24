

import json
from typing import TypedDict

import numpy as np
from my_types import ThemeType
import matplotlib.pyplot as plt
import matplotlib.colors as mc
folder = "./analytics/"
analytics_file = folder + "file.json"


class AnalyticsFileDict(TypedDict):
    themes: list[ThemeType]


def report_pie(obj):
    (x, y) = zip(*obj.items())
    fig, ax = plt.subplots()
    ax.pie(y, labels=x,
           autopct='%1.1f%%', )


def report_pie_colors(obj):
    (x, y) = zip(*obj.items())
    colors = (mc.to_rgb(col) for col in x)
    fig, ax = plt.subplots()
    ax.pie(y, labels=x,
           autopct='%1.1f%%', colors=colors)


def report_bar(obj):
    (x, y) = zip(*obj.items())
    fig, ax = plt.subplots()
    ax.bar(x, y)


def create_report():
    json_data: AnalyticsFileDict = {"themes": []}
    with open(analytics_file, "r") as f:
        json_data = json.load(f)
    name_count = {}
    dots_color_count = {}
    dots_color_type_count = {}
    eyes_color_count = {}
    eyes_color_type_count = {}
    dots_shape_count = {}
    eyes_shape_count = {}

    def add_some(object: dict, key: str):
        if key in object:
            object[key] += 1
        else:
            object[key] = 1

    for theme in json_data["themes"]:
        add_some(name_count, theme["name"])
        add_some(dots_color_type_count, theme["dotsColor"]["type"])
        for one_c in theme["dotsColor"]["colors"]:
            add_some(dots_color_count, one_c)

        for eyes_color in theme["eyesColor"]:
            for eye_color in eyes_color["colors"]:
                add_some(eyes_color_count, eye_color)
            add_some(eyes_color_type_count, eyes_color["type"])

        add_some(dots_shape_count, theme["dotsShape"]["name"])
        for eyes_shape in theme["eyesShape"]:
            add_some(eyes_shape_count, eyes_shape["name"])
    # [ ] butfy
    report_pie(name_count)
    report_pie_colors(dots_color_count)
    report_pie(dots_color_type_count)
    report_pie_colors(eyes_color_count)
    report_pie(eyes_color_type_count)
    report_bar(dots_shape_count)
    report_bar(eyes_shape_count)
    plt.show()


def add_theme(theme: ThemeType):
    json_data: AnalyticsFileDict = {"themes": []}

    try:
        with open(analytics_file, "r") as f:
            json_data = json.load(f)
    except IOError:
        pass

    if not "themes" in json_data:
        json_data["themes"] = []
    json_data["themes"].append(theme)

    with open(analytics_file, "w") as f:
        json.dump(json_data, f)


if __name__ == "__main__":
    create_report()
