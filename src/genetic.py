import population
from chromosome import fitness
import data

GENERATION_LIMIT = 20
"""Generation iteration limit.
"""

POPULATION_SIZE = 5
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

CVRP_INSTANCE = ''
"""Path to a CVRP instance file.
"""

if __name__ == "__main__":
    if CVRP_INSTANCE != '':
        # Load CVRP instance
        pass
    else:
        # Generate random data
        depot, customers, vehicles_capacity = data.generate_data(
            num_customers=100,
            min_distance=5,
            max_distance=20,
            min_demand=0,
            max_demand=20
        )

    # Initialize population
    chromosomes = population.create_population(
        POPULATION_SIZE=POPULATION_SIZE,
        vehicles_capacity=vehicles_capacity,
        customers=customers
    )

    # Evolution
    for generation in range(0, GENERATION_LIMIT):
        # Selection
        chromosomes = population.tournament_selection(
            chromosomes=chromosomes,
            customers=customers,
            COORDINATES_DEPOT=depot,
            NUMBER_TOURNAMENT_SELECTION=NUMBER_TOURNAMENT_SELECTION,
            PROBABILITY_ELITISM=PROBABILITY_ELITISM
        )

        # Crossover
        chromosomes = population.crossover(
            chromosomes=chromosomes,
            customers=customers,
            vehicles_capacity=vehicles_capacity,
            CROSSOVER_METHOD=CROSSOVER_METHOD,
            PROBABILITY_ELITISM=PROBABILITY_ELITISM
        )

        # Mutation
        chromosomes = population.mutation(
            chromosomes=chromosomes,
            customers=customers,
            vehicles_capacity=vehicles_capacity,
            COORDINATES_DEPOT=depot,
            PROBABILITY_ELITISM=PROBABILITY_ELITISM,
            PROBABILITY_MUTATION=PROBABILITY_MUTATION,
            MUTATION_METHOD=MUTATION_METHOD
        )

    # Best chromosome
    best_chromosome = chromosomes[0]
    best_fitness = fitness(
        best_chromosome,
        customers=customers,
        DEPOT_COORDINATE=depot
    )

    print(best_chromosome)
    print(best_fitness)
