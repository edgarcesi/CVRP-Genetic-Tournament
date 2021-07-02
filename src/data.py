from random import randint
from math import pi, sqrt, cos, sin
import matplotlib.pyplot as plt
from numpy import block


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


def plot(customers, chromosome, COORDINATES_DEPOT):
    # Seaborn style
    plt.style.use('seaborn')

    # X and Y data
    x = [customer[0] for customer in customers]
    y = [customer[1] for customer in customers]

    # Depot location
    xd, yd = COORDINATES_DEPOT

    # Scatter X, Y and depot
    plt.scatter(x, y, color='b')
    plt.scatter(xd, yd, color='r')

    # Grid properties
    plt.grid(color='grey', linestyle='-', linewidth=0.1)

    # Routes through customers
    for i in range(len(chromosome)):

        # Initialize graph with depot
        xc = [xd]
        yc = [yd]

        # get gene
        for y in range(len(chromosome[i])):
            # get customers coordinates
            customer_coordinate = customers[chromosome[i][y] - 1][:2]

            # append values
            xc.append(customer_coordinate[0])
            yc.append(customer_coordinate[1])

        # Add depot
        xc.append(xd)
        yc.append(yd)

        # Random colors
        def r(): return randint(0, 255)

        # Connections
        plt.plot(xc, yc, color='#%02X%02X%02X' % (r(), r(), r()))

    # Plot
    return plt.show()
