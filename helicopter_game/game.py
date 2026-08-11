import os
import sys
import time

import config
import shop
import storage
from config import EMPTY, TREE, FIRE, BURNT, WATER, HOSPITAL, SHOP, sprite
from field import Field
from helicopter import Helicopter
from keyboard import read_key
from weather import Weather


ПОДСКАЗКА = ("w a s d — полёт   e — тушить   b — магазин   h — госпиталь   "
             "пробел — ждать   k — сохранить   l — загрузить   q — выход")


class Game:
    """Состояние игры и главный цикл с механикой тиков."""

    def __init__(self, field, helicopter, weather, tick_number=0):
        self.field = field
        self.helicopter = helicopter
        self.weather = weather
        self.tick_number = tick_number
        self.messages = ["Игра началась. Тушите лес!"]
        self.running = True

    # --- создание новой игры ---------------------------------------------

    @staticmethod
    def new_game(width, height):
        поле = Field(width, height)

        поле.generate_rivers(max(1, width // 8))
        поле.generate_trees(max(4, width * height // 6))
        поле.place_buildings()

        старт = поле.random_empty_cell()
        if старт is None:
            старт = (0, 0)

        вертолёт = Helicopter(старт[0], старт[1])

        return Game(поле, вертолёт, Weather())

    # --- отрисовка --------------------------------------------------------

    def clear_screen(self):
        if sys.stdout.isatty():
            os.system("clear")
        else:
            print("-" * 40)

    def render(self):
        self.clear_screen()

        for y in range(self.field.height):
            строка = ""
            for x in range(self.field.width):
                строка += self.cell_sprite(x, y)
            print(строка)

        print()
        print(self.status())
        print(ПОДСКАЗКА)
        print()

        for сообщение in self.messages[-4:]:
            print("•", сообщение)

    def cell_sprite(self, x, y):
        # вертолёт рисуется поверх клетки, облако — поверх земли
        if self.helicopter.x == x and self.helicopter.y == y:
            return sprite("helicopter")

        облако = self.weather.cloud_at(x, y)
        if облако is not None and self.field.get(x, y) != FIRE:
            return sprite("storm") if облако["storm"] else sprite("cloud")

        return sprite(self.field.get(x, y))

    def status(self):
        вертолёт = self.helicopter
        return ("Тик: " + str(self.tick_number)
                + " | Очки: " + str(вертолёт.score)
                + " | Жизни: " + str(вертолёт.lives)
                + " | Вода: " + str(вертолёт.water) + "/" + str(вертолёт.tank_capacity)
                + " | Пожаров: " + str(len(self.field.fires))
                + " | Деревьев: " + str(self.field.count(TREE))
                + " | Ветер: " + self.weather.wind_name())

    # --- управление -------------------------------------------------------

    def handle_key(self, клавиша):
        """Обрабатывает клавишу. Возвращает True, если прошёл игровой тик."""
        self.messages = []

        if клавиша == "q":
            self.running = False
            return False

        if клавиша in config.DIRECTIONS:
            dx, dy = config.DIRECTIONS[клавиша]
            self.messages += self.helicopter.move(dx, dy, self.field)
            return True

        if клавиша == "e":
            self.messages += self.helicopter.extinguish(self.field)
            return True

        if клавиша == "b":
            self.messages += shop.buy_upgrade(self.helicopter, self.field)
            return True

        if клавиша == "h":
            self.messages += shop.buy_health(self.helicopter, self.field)
            return True

        if клавиша == " ":
            self.messages.append("Ждём...")
            return True

        if клавиша == "k":
            self.messages += storage.save_game(self)
            return False

        if клавиша == "l":
            if not storage.has_save():
                self.messages.append("Сохранений нет")
                return False
            поле, вертолёт, погода, тик = storage.load_game()
            self.field = поле
            self.helicopter = вертолёт
            self.weather = погода
            self.tick_number = тик
            self.messages.append("Игра восстановлена из файла")
            return False

        self.messages.append("Неизвестная клавиша: " + клавиша)
        return False

    # --- тик игры ---------------------------------------------------------

    def tick(self):
        self.tick_number += 1

        # 1. лес растёт и иногда загорается сам
        self.field.grow_trees()
        пожар = self.field.random_fire()
        if пожар is not None:
            self.messages.append("Загорелось дерево в клетке "
                                 + str(пожар[0]) + ", " + str(пожар[1]))

        # 2. погода: ветер, дождь, молнии
        self.messages += self.weather.tick(self.field, self.helicopter)

        # 3. горящие деревья догорают и поджигают соседей
        сгорели = self.field.tick_fires(self.weather.wind)
        for x, y in сгорели:
            self.helicopter.add_score(config.SCORE_BURNT)
            self.messages.append("Дерево сгорело в клетке " + str(x) + ", " + str(y)
                                 + ": " + str(config.SCORE_BURNT) + " очков")

        # 4. вертолёт стоит в горящей клетке — получает урон
        if self.field.get(self.helicopter.x, self.helicopter.y) == FIRE:
            self.helicopter.damage(1)
            self.messages.append("Вертолёт в огне: −1 жизнь")

        if not self.helicopter.alive():
            self.running = False

    # --- главный цикл -----------------------------------------------------

    def run(self):
        while self.running:
            self.render()
            клавиша = read_key()
            прошёл_тик = self.handle_key(клавиша)
            if прошёл_тик:
                self.tick()

        self.render()
        print()
        if not self.helicopter.alive():
            print("Жизни кончились. Игра окончена.")
        else:
            print("Выход из игры.")
        print("Итоговый счёт:", self.helicopter.score)
