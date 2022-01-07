def generator(seed=55):
    def g():
        x = seed
        while (True):
            x = x+2654435769
            x = x & 4294967295

            t = x ^ x >> 15
            t = t & 4294967295

            t = t*2246822507
            t = t & 4294967295

            t = t*3266489909
            t = t & 4294967295

            t = t ^ t >> 16
            t = t & 4294967295
            yield t/4294967296
    return g()


if __name__ == "__main__":
    g = generator(239856329867)
    m = generator(239856329866)
    while(True):
        print(f"{next(g)}|{next(m)}")
