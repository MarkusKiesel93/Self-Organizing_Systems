from typing import List, Tuple, Any
import numpy as np
import pandas as pd
from tqdm import tqdm


class GeneticAltorithm():
    def __init__(self, problem_instance, **kwargs) -> None:
        self.problem_instance = problem_instance
        self.dimension = self.problem_instance.shape[0]
        self.nodes = np.arange(self.dimension)

        self.population_size = kwargs.get('population_size', 100)
        self.max_generations = kwargs.get('max_generations', 100)
        self.mutation_rate = kwargs.get('mutation_rate', 0.01)
        self.elitism_rate = kwargs.get('elitism_rate', 0.05)

        self.debug_mode = kwargs.get('debug_mode', False)

        self.population: List[Any] = []
        self.best_fitness_in_generation: List[float] = []
        self.best_solution = None

    # genetic algorithm procedure
    def run(self):
        # create initial population
        self.population = self._generate_initial_population()
        # run for max_generations
        for generation in tqdm(np.arange(self.max_generations), desc='Generation: '):
            next_population = []
            # calculate fitness and probabilities for current generation
            current_fitness, current_probabilities = self._calulate_population_fitness()
            top_solution = np.argsort(current_fitness)[0]
            self.best_fitness_in_generation.append(current_fitness[top_solution])
            self.best_solution = self.population[top_solution]

            # select elitists
            next_population.extend(self._select_elites(current_fitness))

            # generate next generation by crossover and mutation
            while len(next_population) < self.population_size:
                father = self._roulette(current_probabilities)
                mother = self._roulette(current_probabilities)
                child = self._crossover(father, mother)
                child = self._mutate(child)
                next_population.append(child)
            if self.debug_mode:
                print(f'Generation: {generation + 1}')
                print(f'Top fitness: {current_fitness[top_solution]}')
                print(f'Solution: {self.population[top_solution]}')
            self.population = next_population

    def fitness_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            'generation': np.arange(1, self.max_generations + 1),
            'fitness': self.best_fitness_in_generation
        })

    # calulates the fitness of the whole population
    # it also returns the probabilities according to the fitness needed for roulette wheel selection
    def _calulate_population_fitness(self) -> Tuple[np.array, np.array]:
        population_fitness = np.zeros(self.population_size)
        for i, chromosome in enumerate(self.population):
            population_fitness[i] = self._evaluate_fitness(chromosome)
        minimization_fitness = np.ones(self.population_size) / population_fitness
        return population_fitness, minimization_fitness / minimization_fitness.sum()

    # get the best performing chromosomes based on the fitness
    def _select_elites(self, fitness: List[float]) -> List[List[int]]:
        nuber_of_elites = int(self.population_size * self.elitism_rate)
        if nuber_of_elites > 0:
            elite_index = np.argsort(fitness)[:nuber_of_elites]
            elites = [self.population[i] for i in elite_index]
            assert nuber_of_elites == len(elites)
            return elites
        else:
            return []

    # select a chromosome based on the fitness (probabilitie)
    def _roulette(self, fitness_probabilities) -> np.array:
        index_selected = np.random.choice(np.arange(self.population_size), p=fitness_probabilities)
        return self.population[index_selected]

    def _evaluate_fitness(self, chromosome: np.array) -> float:
        raise NotImplementedError('implment fitness function in concrete problem implementation')

    def _generate_initial_population(self) -> List[Any]:
        raise NotImplementedError('implment population generation in concrete problem implementation')

    def _mutate(self, chromosome: np.array) -> np.array:
        raise NotImplementedError('implment mutation logic in concrete problem implementation')

    def _crossover(self, mother: np.array, father: np.array) -> np.array:
        raise NotImplementedError('implment crossover logic in concrete problem implementation')
