import numpy as np


def create_shuffle_array(arange):
    arange = np.arange(arange)
    np.random.shuffle(arange)
    return arange


def reorder_array(a, b, positions):
    new_positions = np.array(np.zeros(len(positions)))

    for i in range(len(positions)):
        new_positions[i] = list(b).index(a[positions[i]])

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


def create_shuffle_arange(arange):

    arange = np.arange(arange)
    np.random.shuffle(arange)
    return arange


def distance(a, b):
    return np.linalg.norm(a - b)
