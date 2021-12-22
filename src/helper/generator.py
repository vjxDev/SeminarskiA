from numpy import uint32


def generator():
    x = 55
    while (True):
        x = uint32(x+2654435769)
        t = x ^ x >> 15
        t = uint32(t*2246822507)
        t = uint32(t*3266489909)
        t = t ^ t >> 16
        yield t/4294967296
