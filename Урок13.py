import random


# Задание №1

def создать_матрицу(строк, столбцов, минимум=-100, максимум=100):
    матрица = []
    for i in range(строк):
        строка = []
        for j in range(столбцов):
            строка.append(random.randint(минимум, максимум))
        матрица.append(строка)
    return матрица


def сложить(m1, m2):
    # складывать можно только матрицы одинаковой размерности
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        print("Размерности матриц не совпадают")
        return False

    результат = []
    for i in range(len(m1)):
        строка = []
        for j in range(len(m1[i])):
            строка.append(m1[i][j] + m2[i][j])
        результат.append(строка)
    return результат


def напечатать(матрица, заголовок):
    print(заголовок)
    for строка in матрица:
        print(строка)
    print()


строк = int(input("Количество строк: "))
столбцов = int(input("Количество столбцов: "))

print()
matrix_1 = создать_матрицу(строк, столбцов)
matrix_2 = создать_матрицу(строк, столбцов)
matrix_3 = сложить(matrix_1, matrix_2)

напечатать(matrix_1, "matrix_1:")
напечатать(matrix_2, "matrix_2:")
напечатать(matrix_3, "matrix_3 = matrix_1 + matrix_2:")
