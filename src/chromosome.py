from itertools import chain
from random import sample
from utils import reorder_array, change_position_array, distance


def fitness(chromosome, customers, DEPOT_COORDINATE):
    fitness = 0

    for i in range(len(chromosome)):
        routes = []

        # Add depot at route start
        routes.append(DEPOT_COORDINATE)

        # Retrieve routes customers
        for y in range(len(chromosome[i])):
            customer_coordinate = \
                customers[chromosome[i][y] - 1][:2]
            routes.append(customer_coordinate)

        # Add depot at route end
        routes.append(DEPOT_COORDINATE)

        # Calculate chromosome fitness
        for i in range(len(routes) - 1):
            fitness += distance(routes[i], routes[i + 1])

    return fitness


def obx(chromosome1, chromosome2, num_customers):
    # Define cut points
    positions = sample(range(0, num_customers), 3)

    # Concat chromosomes
    concatenated_chromosome1 = list(chain.from_iterable(chromosome1))
    concatenated_chromosome2 = list(chain.from_iterable(chromosome2))
    positions.sort()

    # Modify gene
    a = reorder_array(
        concatenated_chromosome1,
        concatenated_chromosome2,
        positions
    )
    b = reorder_array(
        concatenated_chromosome2,
        concatenated_chromosome1,
        positions
    )

    return a, b


def pmx(chromosome1, chromosome2, num_customers):
    chromosomes_length = len(chromosome1)

    # get gene_size
    gene_size = int(num_customers / chromosomes_length)

    # get cut points
    cuts_points = sample(
        range(1, chromosomes_length * gene_size - 1),
        3
    )
    cuts_points.append(0)
    cuts_points.append(chromosomes_length * gene_size)
    cuts_points.sort()

    # Concat chromosomes
    concatenated_chromosome1 = list(chain.from_iterable(chromosome1))
    concatenated_chromosome2 = list(chain.from_iterable(chromosome2))

    # First child
    a = change_position_array(
        concatenated_chromosome1,
        concatenated_chromosome2,
        cuts_points
    )

    # Second child
    b = change_position_array(
        concatenated_chromosome2,
        concatenated_chromosome1,
        cuts_points
    )

    return a, b
