import json
import os

from field import Field
from helicopter import Helicopter
from weather import Weather


ПАПКА = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
ФАЙЛ = os.path.join(ПАПКА, "save.json")


def save_game(game, путь=ФАЙЛ):
    """Сохранение состояния игры в файл."""
    данные = {
        "tick": game.tick_number,
        "field": {
            "width": game.field.width,
            "height": game.field.height,
            "grid": game.field.grid,
            # ключи словаря в JSON только строки, потому "x,y"
            "fires": {str(x) + "," + str(y): осталось
                      for (x, y), осталось in game.field.fires.items()},
        },
        "helicopter": {
            "x": game.helicopter.x,
            "y": game.helicopter.y,
            "water": game.helicopter.water,
            "tank_capacity": game.helicopter.tank_capacity,
            "lives": game.helicopter.lives,
            "score": game.helicopter.score,
        },
        "weather": {
            "wind": list(game.weather.wind),
            "clouds": game.weather.clouds,
        },
    }

    if not os.path.isdir(ПАПКА):
        os.makedirs(ПАПКА)

    with open(путь, "w", encoding="utf-8") as файл:
        json.dump(данные, файл, ensure_ascii=False, indent=2)

    return ["Игра сохранена: " + os.path.basename(путь)]


def has_save(путь=ФАЙЛ):
    return os.path.isfile(путь)


def load_game(путь=ФАЙЛ):
    """Восстановление игры из файла. Возвращает поле, вертолёт, погоду и тик."""
    with open(путь, encoding="utf-8") as файл:
        данные = json.load(файл)

    поле = Field(данные["field"]["width"], данные["field"]["height"])
    поле.grid = данные["field"]["grid"]
    поле.fires = {}
    for ключ, осталось in данные["field"]["fires"].items():
        x, y = ключ.split(",")
        поле.fires[(int(x), int(y))] = осталось

    вертолёт = Helicopter(данные["helicopter"]["x"], данные["helicopter"]["y"])
    вертолёт.water = данные["helicopter"]["water"]
    вертолёт.tank_capacity = данные["helicopter"]["tank_capacity"]
    вертолёт.lives = данные["helicopter"]["lives"]
    вертолёт.score = данные["helicopter"]["score"]

    погода = Weather()
    погода.wind = tuple(данные["weather"]["wind"])
    погода.clouds = данные["weather"]["clouds"]

    return поле, вертолёт, погода, данные["tick"]
