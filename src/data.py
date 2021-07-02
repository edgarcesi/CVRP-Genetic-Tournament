from random import randint, random
from math import pi, sqrt, cos, sin
import matplotlib.pyplot as plt
from distinctipy import distinctipy


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
        r = randint(min_distance, max_distance) * sqrt(random())
        t = 2 * pi * random()
        x = r * cos(t)
        y = r * sin(t)

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

    # Scatter customers and depot
    plt.scatter(x, y, s=70, color='k', marker="1", zorder=3)
    plt.scatter(xd, yd, s=70, color='k', marker="o", zorder=3)

    # Grid properties
    plt.grid(color='grey', linestyle='-', linewidth=0.05)

    # Random route colors
    colors = distinctipy.get_colors(len(chromosome))

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

        # Route
        plt.plot(xc, yc, c=colors[i], zorder=-1)

    # Plot
    return plt.show()
