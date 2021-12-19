def gen(seed: str):
    while(True):
        seed = seed+' hello '
        yield seed


hello = iter(gen('rr'))

print(next(hello))
print(next(hello))
print(next(hello))
print(next(hello))
print(next(hello))

print([[5*i+j for j in range(1, 6)] for i in range(5)])
