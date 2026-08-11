import config
from config import FIRE, WATER, HOSPITAL, SHOP


class Helicopter:
    """Вертолёт: позиция, вода в резервуарах, жизни и очки."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tank_capacity = config.START_TANK
        self.water = 0
        self.lives = config.START_LIVES
        self.score = 0

    def move(self, dx, dy, field):
        """Перелёт на соседнюю клетку. Возвращает сообщения о событиях."""
        новый_x = self.x + dx
        новый_y = self.y + dy

        if not field.in_bounds(новый_x, новый_y):
            return ["Дальше край карты"]

        self.x = новый_x
        self.y = новый_y

        сообщения = []
        клетка = field.get(self.x, self.y)

        if клетка == WATER:
            сообщения += self.take_water()
        elif клетка == FIRE and self.water == 0:
            self.damage(1)
            сообщения.append("Влетели в пожар без воды: −1 жизнь")
        elif клетка == HOSPITAL:
            сообщения.append("Госпиталь: клавиша h — купить жизнь за "
                             + str(config.PRICE_LIFE))
        elif клетка == SHOP:
            сообщения.append("Магазин: клавиша b — купить резервуар за "
                             + str(config.PRICE_TANK))

        return сообщения

    def take_water(self):
        # набор воды при пролёте над рекой
        if self.water == self.tank_capacity:
            return ["Резервуары уже полные"]

        self.water = self.tank_capacity
        return ["Набрали воду: " + str(self.water) + "/" + str(self.tank_capacity)]

    def extinguish(self, field):
        """Потушить пожар под вертолётом."""
        if field.get(self.x, self.y) != FIRE:
            return ["Под вертолётом нечего тушить"]

        if self.water == 0:
            return ["Нет воды — летите к реке"]

        field.extinguish(self.x, self.y)
        self.water -= 1
        self.score += config.SCORE_EXTINGUISH

        return ["Пожар потушен: +" + str(config.SCORE_EXTINGUISH) + " очков"]

    def damage(self, количество=1):
        self.lives -= количество
        if self.lives < 0:
            self.lives = 0

    def heal(self, количество=1):
        self.lives += количество
        if self.lives > config.MAX_LIVES:
            self.lives = config.MAX_LIVES

    def add_score(self, количество):
        self.score += количество

    def alive(self):
        return self.lives > 0
