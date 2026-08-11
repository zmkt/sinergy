import random

import config
from config import EMPTY, TREE, FIRE, BURNT, WATER, HOSPITAL, SHOP


class Field:
    """Игровое поле: клетки, реки, деревья и пожары."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.fires = {}   # (x, y) -> сколько тиков осталось до сгорания

    # --- базовые операции -------------------------------------------------

    def in_bounds(self, x, y):
        # принадлежит ли клетка полю
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x, y):
        return self.grid[y][x] if self.in_bounds(x, y) else None

    def set(self, x, y, вид):
        if self.in_bounds(x, y):
            self.grid[y][x] = вид

    def neighbors(self, x, y):
        # четыре соседние клетки, не выходящие за поле
        соседи = []
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if self.in_bounds(x + dx, y + dy):
                соседи.append((x + dx, y + dy))
        return соседи

    def random_cell(self, region="any"):
        """Случайная клетка в заданной части карты.

        region: 'nw', 'ne', 'sw', 'se' или 'any'.
        """
        половина_x = self.width // 2
        половина_y = self.height // 2

        if region == "nw":
            x = random.randint(0, максимум(половина_x - 1))
            y = random.randint(0, максимум(половина_y - 1))
        elif region == "ne":
            x = random.randint(половина_x, self.width - 1)
            y = random.randint(0, максимум(половина_y - 1))
        elif region == "sw":
            x = random.randint(0, максимум(половина_x - 1))
            y = random.randint(половина_y, self.height - 1)
        elif region == "se":
            x = random.randint(половина_x, self.width - 1)
            y = random.randint(половина_y, self.height - 1)
        else:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

        return x, y

    def random_empty_cell(self):
        # свободная клетка: земля или пепелище
        for попытка in range(self.width * self.height):
            x, y = self.random_cell()
            if self.get(x, y) in (EMPTY, BURNT):
                return x, y
        return None

    # --- генерация карты --------------------------------------------------

    def generate_rivers(self, count):
        # река — случайное блуждание от края карты
        for номер in range(count):
            x, y = self.random_cell()
            горизонтальная = random.choice([True, False])
            длина = self.width if горизонтальная else self.height
            шаг = random.choice([-1, 1])

            for клетка in range(длина):
                if not self.in_bounds(x, y):
                    break
                self.set(x, y, WATER)
                if горизонтальная:
                    x += шаг
                    y += random.choice([-1, 0, 0, 1])   # река слегка виляет
                else:
                    y += шаг
                    x += random.choice([-1, 0, 0, 1])

    def generate_trees(self, count):
        посажено = 0
        for попытка in range(count * 10):
            if посажено == count:
                break
            x, y = self.random_cell()
            if self.get(x, y) == EMPTY:
                self.set(x, y, TREE)
                посажено += 1
        return посажено

    def place_buildings(self):
        # госпиталь и магазин ставим в разные части карты
        for вид, region in ((HOSPITAL, "nw"), (SHOP, "se")):
            for попытка in range(100):
                x, y = self.random_cell(region)
                if self.get(x, y) in (EMPTY, TREE, BURNT):
                    self.set(x, y, вид)
                    break

    # --- жизнь леса -------------------------------------------------------

    def grow_trees(self):
        # деревья периодически вырастают сами
        if random.random() < config.GROW_CHANCE:
            клетка = self.random_empty_cell()
            if клетка is not None:
                self.set(клетка[0], клетка[1], TREE)

    def ignite(self, x, y):
        # поджечь дерево
        if self.get(x, y) == TREE:
            self.set(x, y, FIRE)
            self.fires[(x, y)] = config.FIRE_TICKS
            return True
        return False

    def random_fire(self):
        # случайное возгорание в любой части карты
        if random.random() >= config.IGNITE_CHANCE:
            return None
        for попытка in range(50):
            x, y = self.random_cell()
            if self.ignite(x, y):
                return x, y
        return None

    def extinguish(self, x, y):
        # потушить горящую клетку — дерево остаётся живым
        if self.get(x, y) == FIRE:
            self.set(x, y, TREE)
            self.fires.pop((x, y), None)
            return True
        return False

    def tick_fires(self, wind):
        """Тик пожаров. Возвращает список сгоревших клеток."""
        сгорели = []

        for позиция in list(self.fires.keys()):
            self.fires[позиция] -= 1
            if self.fires[позиция] > 0:
                continue

            # дерево догорело: клетка меняется на пепелище
            x, y = позиция
            del self.fires[позиция]
            self.set(x, y, BURNT)
            сгорели.append(позиция)

            # огонь перекидывается на соседей, по ветру — всегда
            dx, dy = wind
            if self.ignite(x + dx, y + dy):
                pass
            for сосед in self.neighbors(x, y):
                if random.random() < config.SPREAD_CHANCE:
                    self.ignite(сосед[0], сосед[1])

        return сгорели

    def count(self, вид):
        # сколько клеток заданного вида на поле
        всего = 0
        for строка in self.grid:
            всего += строка.count(вид)
        return всего


def максимум(число):
    # защита от пустого диапазона на очень маленьких полях
    return число if число > 0 else 0
