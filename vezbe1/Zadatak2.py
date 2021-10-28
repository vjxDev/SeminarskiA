# import math
from math import sqrt
# from math import sqrt as koren
a = eval(input("Unesite parametar a "))
b = eval(input("Unesite parametar b "))
c = eval(input("Unesite parametar c "))

d = sqrt(b**2 - 4*a*c)
x1 = (-b+d)/(2*a)
x2 = (-b-d)/(2*a)

print(x1, x2)
