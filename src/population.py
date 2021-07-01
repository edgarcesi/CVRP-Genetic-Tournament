from math import floor
import numpy as np
from itertools import chain
from random import random, sample
from copy import deepcopy
from chromosome import fitness, pmx, obx
from utils import create_shuffle_array


def create_population(
    POPULATION_SIZE,
    vehicles_capacity,
    customers
):
    # Initialization
    chromosomes = np.array([
        create_shuffle_array(len(customers)) for _ in range(POPULATION_SIZE)
    ])

    # Chromosomes validity
    chromosomes = separate_by_capacity(
        chromosomes,
        vehicles_capacity,
        customers
    )

    return chromosomes


def separate_by_capacity(
    chromosomes,
    vehicles_capacity,
    customers
):
    new_chromosomes = []

    for chromosome in chromosomes:
        new_chromosome = []
        gene = []
        total_demand = 0

        for node in chromosome:
            demand = customers[node][2]

            # We only care about the chromosome parts respecting
            # the capacity constraint
            if (total_demand + demand) > vehicles_capacity:
                # Add new gene to the new chromosome
                new_chromosome.append(gene.copy())

                # Reset total demand
                total_demand = 0

                # Clear gene
                del gene[:]

            # Update total demand
            total_demand += demand

            # Add node to gene
            gene.append(node)

        # Append new gene to new chromosome
        new_chromosome.append(gene.copy())

        new_chromosomes.append(new_chromosome)

    return new_chromosomes


def elistism(
    chromosomes,
    PROBABILITY_ELITISM
):
    elites = []

    while len(chromosomes) < floor(PROBABILITY_ELITISM * len(chromosomes)) + 1:
        best = chromosomes[0]
        pos = 0
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i]) < fitness(best):
                pos = i
                best = chromosomes[i]
        elites.append(
            np.array(list(chain.from_iterable(best.copy())))
        )
        chromosomes = np.delete(chromosomes, [pos], axis=0)

    return elites


def crossover(
    chromosomes,
    customers,
    vehicles_capacity,
    CROSSOVER_METHOD,
    PROBABILITY_ELITISM
):
    crossed_chromosomes = []
    chromosomes_copy = chromosomes.copy()

    # Elitism
    crossed_chromosomes = elistism(chromosomes, PROBABILITY_ELITISM)

    # Number of chromosomes to create
    num_chromosomes = len(chromosomes)

    if num_chromosomes % 2 == 0:
        num_chromosomes = int(num_chromosomes / 2)
    else:
        crossed_chromosomes.append(
            np.array(list(chain.from_iterable(chromosomes[0]))))
        np.delete(chromosomes, 0)
        num_chromosomes = int((num_chromosomes - 1) / 2)

    # Breeding process
    for _ in range(num_chromosomes):
        positions = sample(range(0, len(chromosomes_copy)), 2)

        # Crossover
        if CROSSOVER_METHOD == 'RANDOM':
            if random() >= 0.5:
                aa, bb = pmx(
                    deepcopy(chromosomes_copy[positions[0]]),
                    deepcopy(chromosomes_copy[positions[1]]),
                    len(customers)
                )
            else:
                aa, bb = obx(
                    deepcopy(chromosomes_copy[positions[0]]),
                    deepcopy(chromosomes_copy[positions[1]]),
                    len(customers)
                )

        elif CROSSOVER_METHOD == 'PMX':
            aa, bb = pmx(
                deepcopy(chromosomes_copy[positions[0]]),
                deepcopy(chromosomes_copy[positions[1]]),
                len(customers)
            )
        elif CROSSOVER_METHOD == 'OBX':
            aa, bb = obx(
                deepcopy(chromosomes_copy[positions[0]]),
                deepcopy(chromosomes_copy[positions[1]]),
                len(customers)
            )

        # append selected
        crossed_chromosomes.append(aa.copy())
        crossed_chromosomes.append(bb.copy())

    # return
    return separate_by_capacity(
        crossed_chromosomes,
        vehicles_capacity,
        customers
    )


def tournament_selection(
    chromosomes,
    customers,
    COORDINATES_DEPOT,
    NUMBER_TOURNAMENT_SELECTION,
    PROBABILITY_ELITISM
):
    selection = []

    # Select by elitism
    while len(selection) < floor(PROBABILITY_ELITISM * len(chromosomes)) + 1:
        # Take first chromosome as reference
        best = chromosomes[0]
        index = 0

        # Compare all chromosomes to keep the best one
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i], customers, COORDINATES_DEPOT) \
                    < fitness(best, customers, COORDINATES_DEPOT):
                index = i
                best = chromosomes[i]

        selection.append(best.copy())
        chromosomes = np.delete(chromosomes, [index], axis=0)

    # Gene recombination
    for _ in range(0, len(chromosomes)):

        # Pick random positions
        positions = sample(
            range(0, len(chromosomes)),
            NUMBER_TOURNAMENT_SELECTION
        )

        # Define genes to compare
        compare = chromosomes[positions[0]]

        # Keep best genes
        for position in positions:
            if fitness(chromosomes[position], customers, COORDINATES_DEPOT) \
                    < fitness(compare, customers, COORDINATES_DEPOT):
                compare = chromosomes[position]

        selection.append(compare)

    return selection


def mutation(
    chromosomes,
    customers,
    vehicles_capacity,
    COORDINATES_DEPOT,
    PROBABILITY_ELITISM,
    PROBABILITY_MUTATION,
    MUTATION_METHOD
):
    mutated_chromosomes = []

    # Elitism
    while len(mutated_chromosomes) \
            < floor(PROBABILITY_ELITISM * len(chromosomes)) + 1:
        best = chromosomes[0]
        pos = 0
        for i in range(len(chromosomes)):
            if fitness(chromosomes[i], customers, COORDINATES_DEPOT) \
                    < fitness(best, customers, COORDINATES_DEPOT):
                pos = i
                best = chromosomes[i]
        mutated_chromosomes.append(
            np.array(list(chain.from_iterable(best.copy())))
        )
        chromosomes = np.delete(chromosomes, [pos], axis=0)

    # Number of chromosomes to create
    num_chromosomes = len(chromosomes)

    # Mutate chromosomes
    for a in range(num_chromosomes):
        if random() <= PROBABILITY_MUTATION:
            if MUTATION_METHOD == 'RANDOM':
                if random() <= 0.5:
                    pass
                else:
                    pass
            elif MUTATION_METHOD == 'EXC':

                # get cut positions
                positions = sample(range(0, len(customers)), 2)

                # sort postions
                positions.sort()

                # concatenate
                concatenated_chromosome = np.array(
                    list(chain.from_iterable(chromosomes[a])))

                # get and reverse range
                aux = np.copy(concatenated_chromosome)[positions[0]]

                # set reversed interval
                concatenated_chromosome[positions[0]] \
                    = concatenated_chromosome[positions[1]]

                # set seconda value
                concatenated_chromosome[positions[1]] = aux

                # set new value
                mutated_chromosomes.append(concatenated_chromosome)

            # if reverse
            elif MUTATION_METHOD == 'INV':

                # get cut positions
                positions = sample(range(1, len(customers) - 1), 2)

                # sort postions
                positions.sort()

                # concatenate
                concatenated_chromosome = np.array(
                    list(chain.from_iterable(chromosomes[a])))

                # get and reverse range
                aux = np.copy(concatenated_chromosome)[
                    positions[0]:(positions[1] + 1)]

                # set seconda value
                concatenated_chromosome[positions[0]:(
                    positions[1] + 1)], = np.fliplr([aux])

                # set new value
                mutated_chromosomes.append(concatenated_chromosome)
        else:
            mutated_chromosomes.append(
                np.array(list(chain.from_iterable(chromosomes[a])))
            )

    # return
    return separate_by_capacity(
        mutated_chromosomes,
        vehicles_capacity,
        customers
    )
