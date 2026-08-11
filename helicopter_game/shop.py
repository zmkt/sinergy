import config
from config import HOSPITAL, SHOP


def buy_upgrade(helicopter, field):
    """Магазин улучшений: +1 резервуар для воды."""
    if field.get(helicopter.x, helicopter.y) != SHOP:
        return ["Магазин в другой клетке карты"]

    if helicopter.score < config.PRICE_TANK:
        return ["Не хватает очков: нужно " + str(config.PRICE_TANK)]

    helicopter.score -= config.PRICE_TANK
    helicopter.tank_capacity += 1

    return ["Куплен резервуар, теперь их " + str(helicopter.tank_capacity)]


def buy_health(helicopter, field):
    """Госпиталь: +1 жизнь за очки."""
    if field.get(helicopter.x, helicopter.y) != HOSPITAL:
        return ["Госпиталь в другой клетке карты"]

    if helicopter.lives >= config.MAX_LIVES:
        return ["Жизни и так полные"]

    if helicopter.score < config.PRICE_LIFE:
        return ["Не хватает очков: нужно " + str(config.PRICE_LIFE)]

    helicopter.score -= config.PRICE_LIFE
    helicopter.heal(1)

    return ["Куплена жизнь, теперь их " + str(helicopter.lives)]
