from random import shuffle
from math import sqrt


def create_shuffle_array(n):
    a = list(range(n))
    shuffle(a)
    return a


def reorder_array(a, b, positions):
    new_positions = []

    for i in range(len(positions)):
        new_positions.append(list(b).index(a[positions[i]]))

    new_positions.sort()

    for i in range(len(positions)):
        a[positions[i]] = b[positions[i]]

    return a


def change_position_array(a, b, positions):
    for i in range(len(positions) - 1):
        if i % 2 == 0:
            for j in range(positions[i], positions[i + 1]):
                pos = list(a).index(b[j])

                a[pos] = a[j]
                a[j] = b[j]

    return a


def distance(a, b):
    xa, ya = a[0], a[1]
    xb, yb = b[0], b[1]
    return sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
