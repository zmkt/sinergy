# Настройки игры: типы клеток, картинки для отрисовки, баланс

# Типы клеток поля
EMPTY = "empty"
TREE = "tree"
FIRE = "fire"
BURNT = "burnt"
WATER = "water"
HOSPITAL = "hospital"
SHOP = "shop"

# Картинки клеток
EMOJI = {
    EMPTY: "🟩",
    TREE: "🌲",
    FIRE: "🔥",
    BURNT: "⬛",
    WATER: "🟦",
    HOSPITAL: "🏥",
    SHOP: "🏪",
    "helicopter": "🚁",
    "cloud": "🌧",
    "storm": "🌩",
}

ASCII = {
    EMPTY: " .",
    TREE: " T",
    FIRE: " *",
    BURNT: " #",
    WATER: " ~",
    HOSPITAL: " H",
    SHOP: " $",
    "helicopter": " @",
    "cloud": " c",
    "storm": " s",
}

# Переключается в главном меню: эмодзи или простые символы
USE_EMOJI = True


def sprite(вид):
    # возвращает картинку клетки в выбранном режиме отрисовки
    return EMOJI[вид] if USE_EMOJI else ASCII[вид]


# Баланс игры
FIRE_TICKS = 6           # сколько тиков горит дерево до полного сгорания
SPREAD_CHANCE = 0.35     # шанс, что огонь перекинется на соседнее дерево
GROW_CHANCE = 0.25       # шанс вырастить новое дерево за тик
IGNITE_CHANCE = 0.12     # шанс самовозгорания дерева за тик
CLOUD_CHANCE = 0.15      # шанс появления облака за тик
STORM_CHANCE = 0.3       # какая часть облаков оказывается грозовой
RAIN_CHANCE = 0.5        # шанс, что дождь потушит пожар под облаком
LIGHTNING_CHANCE = 0.25  # шанс удара молнии из грозовой тучи
WIND_CHANGE_CHANCE = 0.1 # шанс смены направления ветра за тик

# Очки
SCORE_EXTINGUISH = 10    # за потушенное дерево
SCORE_BURNT = -15        # за сгоревшее дерево

# Цены
PRICE_TANK = 50          # +1 резервуар для воды
PRICE_LIFE = 40          # +1 жизнь в госпитале

# Стартовые параметры вертолёта
START_LIVES = 3
MAX_LIVES = 5
START_TANK = 1

# Направления: клавиша -> сдвиг по x и y
DIRECTIONS = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0),
}

# Русская раскладка тоже работает
KEY_ALIASES = {
    "ц": "w", "ы": "s", "ф": "a", "в": "d",
    "у": "e", "и": "b", "р": "h", "й": "q",
    "л": "k", "д": "l",
}
