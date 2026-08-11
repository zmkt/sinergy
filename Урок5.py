# Задание №1

число = int(input("Введите целое число: "))

if число % 2 != 0:
    print("число не является четным")
elif число == 0:
    print("нулевое число")
elif число > 0:
    print("положительное четное число")
else:
    print("отрицательное четное число")


# Задание №2

print()
слово = input("Введите слово из маленьких латинских букв: ")

гласные = 0
согласные = 0

a = слово.count("a")
e = слово.count("e")
i = слово.count("i")
o = слово.count("o")
u = слово.count("u")

гласные = a + e + i + o + u
согласные = len(слово) - гласные

print("Гласных:", гласные)
print("Согласных:", согласные)

print("a:", a if a > 0 else False)
print("e:", e if e > 0 else False)
print("i:", i if i > 0 else False)
print("o:", o if o > 0 else False)
print("u:", u if u > 0 else False)


# Задание №3

print()
X = float(input("Минимальная сумма инвестиций: "))
A = float(input("Сколько денег у Майкла: "))
B = float(input("Сколько денег у Ивана: "))

if A >= X and B >= X:
    print(2)
elif A >= X:
    print("Mike")
elif B >= X:
    print("Ivan")
elif A + B >= X:
    print(1)
else:
    print(0)
