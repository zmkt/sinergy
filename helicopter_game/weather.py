import random

import config
from config import TREE, FIRE


ВЕТРЫ = {
    (0, -1): "север",
    (0, 1): "юг",
    (-1, 0): "запад",
    (1, 0): "восток",
}


class Weather:
    """Погода: ветер, дождевые облака и грозы."""

    def __init__(self):
        self.wind = random.choice(list(ВЕТРЫ.keys()))
        self.clouds = []      # список словарей {"x", "y", "storm"}

    def wind_name(self):
        return ВЕТРЫ[self.wind]

    def spawn_cloud(self, field):
        # облако появляется с наветренного края карты
        dx, dy = self.wind
        if dx != 0:
            x = 0 if dx > 0 else field.width - 1
            y = random.randint(0, field.height - 1)
        else:
            x = random.randint(0, field.width - 1)
            y = 0 if dy > 0 else field.height - 1

        self.clouds.append({"x": x, "y": y, "storm": random.random() < config.STORM_CHANCE})

    def cloud_at(self, x, y):
        for облако in self.clouds:
            if облако["x"] == x and облако["y"] == y:
                return облако
        return None

    def tick(self, field, helicopter):
        """Ход погоды: ветер, движение облаков, дождь и молнии."""
        сообщения = []

        if random.random() < config.WIND_CHANGE_CHANCE:
            self.wind = random.choice(list(ВЕТРЫ.keys()))
            сообщения.append("Ветер сменился на " + self.wind_name())

        if random.random() < config.CLOUD_CHANCE:
            self.spawn_cloud(field)

        dx, dy = self.wind
        оставшиеся = []

        for облако in self.clouds:
            облако["x"] += dx
            облако["y"] += dy

            if not field.in_bounds(облако["x"], облако["y"]):
                continue          # облако ушло за карту
            оставшиеся.append(облако)

            x, y = облако["x"], облако["y"]

            # дождь тушит пожар под облаком
            if field.get(x, y) == FIRE and random.random() < config.RAIN_CHANCE:
                field.extinguish(x, y)
                сообщения.append("Дождь потушил пожар в клетке "
                                 + str(x) + ", " + str(y))

            # под дождём вертолёт набирает воду
            if helicopter.x == x and helicopter.y == y and helicopter.water < helicopter.tank_capacity:
                helicopter.water = helicopter.tank_capacity
                сообщения.append("Дождь наполнил резервуары")

            if облако["storm"] and random.random() < config.LIGHTNING_CHANCE:
                сообщения += self.lightning(field, helicopter, x, y)

        self.clouds = оставшиеся
        return сообщения

    def lightning(self, field, helicopter, x, y):
        # молния бьёт в клетку под грозовой тучей
        сообщения = []

        if helicopter.x == x and helicopter.y == y:
            helicopter.damage(1)
            сообщения.append("Молния ударила в вертолёт: −1 жизнь")
            return сообщения

        if field.get(x, y) == TREE:
            field.ignite(x, y)
            сообщения.append("Молния подожгла дерево в клетке "
                             + str(x) + ", " + str(y))

        return сообщения
