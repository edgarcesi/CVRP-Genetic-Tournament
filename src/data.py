from random import randint
from math import pi, sqrt, cos, sin


def generate_data(
    num_customers,
    min_distance,
    max_distance,
    min_demand,
    max_demand
):
    # Depot
    depot = (0, 0)

    # Random customers in a circle area around depot
    customers = []
    for _ in range(num_customers):
        # Coordinates
        a = randint(min_distance, max_distance) * 2 * pi
        r = sqrt(randint(0, 500))
        x, y = r * cos(a), r * sin(a)

        # Demand
        d = randint(min_demand, max_demand)

        # Vehicles capacity
        vehicles_capacity = randint(
            min_demand * num_customers,
            max_demand * num_customers
        )

        # New customer
        customers.append(tuple([x, y, d]))

    return depot, customers, vehicles_capacity
