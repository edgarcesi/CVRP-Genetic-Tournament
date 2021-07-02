import population
from chromosome import fitness
from data import generate_data, plot
from time import process_time

GENERATION_LIMIT = 100
"""Generation iteration limit.
"""

POPULATION_SIZE = 20
"""Number of chromosomes within the population.
"""

CROSSOVER_METHOD = 'PMX'
"""Algorithm for the crossover operation. Can be PMX, OBX or RANDOM.
"""

MUTATION_METHOD = 'INV'
"""Algorithm for the mutation operation. Can be INV, EXC or RANDOM.
"""

NUMBER_TOURNAMENT_SELECTION = 2
"""Number of chromosomes select during the tournament.
"""

PROBABILITY_ELITISM = 0.2


PROBABILITY_MUTATION = 0.4
"""Probability for a chromosome to mutate.
"""

NUMBER_VEHICLES = 4
"""Number of vehicles.
"""

CVRP_INSTANCE = ''
"""Path to a CVRP instance file.
"""
COORDINATES_DEPOT = None
"""Location on the depot.
"""


if __name__ == "__main__":
    if CVRP_INSTANCE != '':
        # Load CVRP instance
        pass
    else:
        # Generate random data
        customers, vehicles_capacity = generate_data(
            num_customers=100,
            min_distance=100,
            max_distance=150,
            min_demand=0,
            max_demand=20,
            NUMBER_VEHICLES=NUMBER_VEHICLES
        )

        # Set depot location
        COORDINATES_DEPOT = (0, 0)

    # Initialize population
    chromosomes = population.create_population(
        vehicles_capacity=vehicles_capacity,
        customers=customers
    )

    # Time
    start = process_time()

    # Evolution
    for generation in range(0, GENERATION_LIMIT):
        # Selection
        chromosomes = population.tournament_selection(
            chromosomes=chromosomes,
            customers=customers,
            COORDINATES_DEPOT=COORDINATES_DEPOT
        )

        # Crossover
        chromosomes = population.crossover(
            chromosomes=chromosomes,
            customers=customers,
            vehicles_capacity=vehicles_capacity,
            COORDINATES_DEPOT=COORDINATES_DEPOT
        )

        # Mutation
        chromosomes = population.mutation(
            chromosomes=chromosomes,
            customers=customers,
            vehicles_capacity=vehicles_capacity,
            COORDINATES_DEPOT=COORDINATES_DEPOT
        )

    # Time
    end = process_time()

    # Best chromosome
    best_chromosome = chromosomes[0]
    best_fitness = fitness(
        best_chromosome,
        customers=customers,
        COORDINATES_DEPOT=COORDINATES_DEPOT
    )

    print('\n### CONFIGURATION ###')
    print('customers : {}'.format(len(customers)))
    print('vehicles : {}'.format(NUMBER_VEHICLES))
    print('vehicles capacity: {}'.format(vehicles_capacity))

    print('\n### BEST CHROMOSOME ###')
    print(best_chromosome)

    print('\n### FITNESS ###')
    print(best_fitness)

    print('\n### TIME ###')
    print('{} s'.format(end - start))

    plot(
        customers=customers,
        chromosome=best_chromosome,
        COORDINATES_DEPOT=COORDINATES_DEPOT
    )
