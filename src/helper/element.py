class Element:
    def __init__(self, type: str):
        self.t = type
        self.children: list[Element] = []
        self.attributes: dict = {}

    def add_attribute(self, name, value):
        self.attributes[name] = value

    def append_child(self, child):
        self.children.append(child)

    def to_text(self):
        attribute = ""
        for (key, value) in self.attributes.items():
            attribute += f"{key}=\"{value}\" "

        innerHTML = self.children_innerHTML()
        if innerHTML == "":
            return f"<{self.t} {attribute}/>"
        return f"<{self.t} {attribute}> {innerHTML} </{self.t}>"

    def children_innerHTML(self):
        innerHTML = ""
        for el in self.children:
            txt = el.to_text()
            innerHTML += txt
        return innerHTML
