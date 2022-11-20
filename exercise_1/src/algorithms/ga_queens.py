from typing import List
import random
import numpy as np

from .ga import GeneticAltorithm


class GeneticAlgorithmQueens(GeneticAltorithm):
    def __init__(self, problem_instance, **kwargs) -> None:
        super().__init__(problem_instance, **kwargs)

    def attacks_diagonal(self, queens, queen, queen_col, direction=1):
        attacks = 0
        row = queen - (queen_col * direction)
        # print(f"Checking for queen_col: {queen_col}")
        for col in range(0, self.dimension):
            # print(f"({row}|{col}): {queens[col]}")

            if queen_col == col:
                row += direction
                continue

            if row < 0 or row >= self.dimension:
                row += direction
                continue

            if queens[col] == row:
                attacks += 1

            row += direction

        return attacks

    def attacks_horizontal(self, queens, queen):
        queens_in_same_row = 0
        for another_queen in queens:
            if another_queen == queen:
                queens_in_same_row += 1

        if queens_in_same_row > 1:
            return 1

        return 0

    def _evaluate_fitness(self, chromosome: np.array) -> float:
        attacks = 0
        for col in range(0, self.dimension):
            queen = chromosome[col]  # row
            attacks += self.attacks_horizontal(chromosome, queen)
            attacks += self.attacks_diagonal(chromosome, queen, col)
            attacks += self.attacks_diagonal(chromosome, queen, col, -1)

        return attacks

    def _generate_initial_population(self) -> List[np.array]:
        population = []
        for i in range(self.population_size):
            population.append(np.random.random_integers(0, self.dimension, self.dimension))
        return population

    # mutation by swapping the position of one node
    def _mutate(self, chromosome: np.array) -> np.array:
        # mutate by given chance
        if random.random() < self.mutation_rate:
            mutated_chromosome = np.copy(chromosome)
            # ensure swap performed
            while True:
                indx_from = random.choice(self.nodes)
                index_to = random.choice(self.nodes)
                if indx_from != index_to:
                    mutated_chromosome[indx_from] = chromosome[index_to]
                    mutated_chromosome[index_to] = chromosome[indx_from]
                    return mutated_chromosome
        else:
            return chromosome

    def _crossover(self, mother: np.array, father: np.array) -> np.array:
        # create child from cossover of father and mother
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        father_gene_indices = np.array([val < cutoff_from or val > cutoff_to for val in range(self.dimension)])
        mother_gene_indices = ~father_gene_indices  # inverse indices of fahter
        child = np.copy(mother)
        child[father_gene_indices] = father[father_gene_indices]
        # correct child genes to get valid solution
        genes_not_used = list(set(self.nodes).difference(set(child)))
        if len(genes_not_used) > 0:
            # correct only fahter part of solution
            for i in self.nodes[father_gene_indices]:
                if child[i] in child[mother_gene_indices]:
                    child[i] = genes_not_used.pop(0)
        # assert set(child) == set(self.nodes)  # check if valid solution
        return child
