import population
from chromosome import fitness
from data import generate_data, plot, load_instance
from time import process_time
from tqdm import trange
from numpy import VisibleDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=VisibleDeprecationWarning)

GENERATION_LIMIT = 100
"""Generation iteration limit.
"""

POPULATION_SIZE = 50
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

NUMBER_VEHICLES = 5
"""Number of vehicles.
"""

CVRP_INSTANCE = 'data/A-n32-k5.vrp'
"""Path to a CVRP instance file.
"""
COORDINATES_DEPOT = None
"""Location on the depot.
"""


if __name__ == "__main__":
    if CVRP_INSTANCE is not None:
        # Load CVRP instance
        name_instance, num_customers, num_vehicles, vehicles_capacity, depot, \
            customers, optimal_solution = load_instance(path=CVRP_INSTANCE)

        # Set depot location
        COORDINATES_DEPOT = depot
        # Set number of vehicles
        NUMBER_VEHICLES = num_vehicles

    else:
        # Generate random data
        customers, vehicles_capacity = generate_data(
            num_customers=1000,
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

    print('\n### CONFIGURATION ###')
    if CVRP_INSTANCE is not None:
        print('name : {}'.format(name_instance))
    print('customers : {}'.format(len(customers)))
    print('vehicles : {}'.format(NUMBER_VEHICLES))
    print('vehicles capacity: {}\n'.format(vehicles_capacity))

    # Time
    start = process_time()

    # Evolution
    for generation in trange(GENERATION_LIMIT):
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

    print('\n### BEST CHROMOSOME ###')
    print(best_chromosome)
    print(len(best_chromosome))

    print('\n### FITNESS ###')
    print(best_fitness)

    print('\n### TIME ###')
    print('{} s'.format(end - start))

    plot(
        customers=customers,
        chromosome=best_chromosome,
        COORDINATES_DEPOT=COORDINATES_DEPOT
    )
