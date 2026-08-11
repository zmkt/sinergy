# Задание №1

class Касса:
    def __init__(self, деньги=0):
        self.деньги = деньги

    def top_up(self, X):
        self.деньги += X
        return self.деньги

    def count_1000(self):
        целых_тысяч = self.деньги // 1000
        print("Целых тысяч в кассе:", целых_тысяч)
        return целых_тысяч

    def take_away(self, X):
        if X > self.деньги:
            raise ValueError("Недостаточно денег в кассе")

        self.деньги -= X
        return self.деньги


касса = Касса(500)

касса.top_up(4700)
print("В кассе:", касса.деньги)

касса.count_1000()

касса.take_away(200)
print("После снятия 200 в кассе:", касса.деньги)

try:
    касса.take_away(100000)
except ValueError as ошибка:
    print("Ошибка:", ошибка)


# Задание №2

print()


class Черепашка:
    def __init__(self, x=0, y=0, s=1):
        self.x = x
        self.y = y
        self.s = s

    def go_up(self):
        self.y += self.s

    def go_down(self):
        self.y -= self.s

    def go_left(self):
        self.x -= self.s

    def go_right(self):
        self.x += self.s

    def evolve(self):
        self.s += 1

    def degrade(self):
        if self.s - 1 <= 0:
            raise ValueError("Шаг не может стать меньше единицы")

        self.s -= 1

    def count_moves(self, x2, y2):
        dx = abs(x2 - self.x)
        dy = abs(y2 - self.y)

        if dx % self.s != 0 or dy % self.s != 0:
            raise ValueError("Точка недостижима шагом " + str(self.s))

        return dx // self.s + dy // self.s

    def позиция(self):
        return "x =", self.x, "y =", self.y, "шаг =", self.s


черепашка = Черепашка()

черепашка.go_right()
черепашка.go_up()
print(*черепашка.позиция())

черепашка.evolve()
черепашка.go_right()
черепашка.go_down()
print(*черепашка.позиция())

print("Ходов до (9, 3):", черепашка.count_moves(9, 3))

черепашка.degrade()
print("После degrade шаг =", черепашка.s)

try:
    черепашка.degrade()
except ValueError as ошибка:
    print("Ошибка:", ошибка)

черепашка.evolve()
try:
    черепашка.count_moves(4, 0)
except ValueError as ошибка:
    print("Ошибка:", ошибка)
