# Задание №1

class Transport:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

    def seating_capacity(self, capacity):
        return f"Вместимость одного автобуса {self.name}  {capacity} пассажиров"


class Autobus(Transport):
    def seating_capacity(self, capacity=50):
        return f"Вместимость одного автобуса {self.name}: {capacity} пассажиров"


autobus = Autobus("Renaul Logan", 180, 12)

print("Название автомобиля:", autobus.name,
      "Скорость:", autobus.max_speed,
      "Пробег:", autobus.mileage)


# Задание №2

print()
print(autobus.seating_capacity())
print(autobus.seating_capacity(75))
