from random import randint
from math import pi, sqrt, cos, sin


def generate_data(
    num_customers,
    min_distance,
    max_distance,
    min_demand,
    max_demand,
    NUMBER_VEHICLES
):
    xl = []
    yl = []
    dl = []

    # Random customers in a circle area around depot
    for _ in range(num_customers):
        # Coordinates
        a = randint(min_distance, max_distance) * 2 * pi
        r = sqrt(randint(0, 500))
        x, y = r * cos(a), r * sin(a)

        # Demand
        d = randint(min_demand, max_demand)

        xl.append(x)
        yl.append(y)
        dl.append(d)

    # New customers
    customers = [tuple([xl[i], yl[i], dl[i]]) for i in range(num_customers)]

    # Vehiclesapacity
    vehicles_capacity = sum(dl) / (NUMBER_VEHICLES - 1)

    return customers, vehicles_capacity
