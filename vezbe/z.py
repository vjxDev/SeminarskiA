class Osoba:
    def __init__(self, ime, godine) -> None:
        self.ime = ime
        self.godine = godine


ana = Osoba('Ana', 32)
marko = Osoba('Marko', 66)
luka = Osoba('Luka', 19)

lista = [ana, marko, luka]

lista.sort(key=lambda x: x.godine)

print([item.ime for item in lista])
