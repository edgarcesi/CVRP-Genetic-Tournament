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


def load_instance(path):
    # Retrieve file
    file = open(path)

    # File content
    content = file.readlines()

    # Instance name
    _, d = content[0].split(' : ', 1)
    name = d.strip()

    # Instance number of vehicles
    data = content[1].split(' : ', 1)[1]

    trucks = data.split()[6]
    fleet = int(trucks[:len(trucks)-1].strip())

    # Instance optimal
    data = content[1].split(' : ', 1)[1]
    optimal = data.split()[9]
    optimal = int(optimal[:len(optimal) - 1].strip())

    # Instance dimension
    _, d = content[3].split(' : ', 1)
    dimension = int(d.strip())

    # Instance capacity
    _, d = content[5].split(' : ', 1)
    capacity = int(d.strip())

    # Where to stop reading file coordinates
    coorend = int(content[3].split(' : ', 1)[1])

    # Instance coordinates
    x = []
    y = []

    for i in range(7, 7 + coorend):
        xy = content[i].strip().split(None, 2)[1:]
        x.append(xy[0])
        y.append(xy[1])

    # Instance demands
    d = []

    for i in range(8 + coorend, 8 + coorend + coorend):
        _, description = content[i].split(' ', 1)
        d.append(description.strip())

    # Instance customers
    customers = [tuple([int(x[i]), int(y[i]), int(d[i])]) for i in range(len(x))]

    # Instance depot
    depot = customers.pop(0)[:2]

    return name, dimension, fleet, capacity, depot, customers, optimal
