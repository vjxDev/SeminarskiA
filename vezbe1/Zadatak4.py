ulog = eval(input("Unesite ulog"))
kamata = eval(input("Unesite kamatna stopa u % "))

for i in range(10):
    ulog = ulog*(1+kamata/100)
    print("ulog posle", i+1, "je:", ulog)

print(ulog)
