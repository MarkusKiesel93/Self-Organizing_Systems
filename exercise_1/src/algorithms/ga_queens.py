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
        for col in range(0, self.dimension):
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
        attacks = len(chromosome)
        for col in range(0, self.dimension):
            queen = chromosome[col]  # row
            attacks += self.attacks_horizontal(chromosome, queen)
            attacks += self.attacks_diagonal(chromosome, queen, col)
            attacks += self.attacks_diagonal(chromosome, queen, col, -1)

        return attacks

    def _generate_initial_population(self) -> List[np.array]:
        population = []
        for i in range(self.population_size):
            population.append(np.random.random_integers(0, self.dimension - 1, self.dimension))
        return population

    def _mutate(self, chromosome: np.array) -> np.array:
        # mutate by given chance
        if random.random() < self.mutation_rate:
            mutated_chromosome = np.copy(chromosome)
            # ensure swap performed
            while True:
                index_from = random.choice(self.nodes)
                index_to = random.choice(self.nodes)
                if index_from != index_to:
                    mutated_chromosome[index_from] = chromosome[index_to]
                    mutated_chromosome[index_to] = chromosome[index_from]
                    return mutated_chromosome
        else:
            return chromosome

    def _crossover(self, mother: np.array, father: np.array) -> np.array:
        # create child from cossover of father and mother
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        father_gene_indices = np.array([val < cutoff_from or val > cutoff_to for val in range(self.dimension)])
        mother_gene_indices = ~father_gene_indices  # inverse indices of fahter
        first_child = np.copy(mother)
        first_child[father_gene_indices] = father[father_gene_indices]
        first_child = self._repair_chromosom(first_child)
        second_child = np.copy(father)
        second_child[mother_gene_indices] = mother[mother_gene_indices]
        second_child = self._repair_chromosom(second_child)
        return [first_child, second_child]

    def _repair_chromosom(self, chromosom):
        genes_not_used = np.setdiff1d(self.nodes, chromosom)
        np.random.shuffle(genes_not_used)
        genes_not_used_index = 0
        if genes_not_used.size > 0:
            used_gene = np.zeros(len(self.nodes))
            for i in range(len(self.nodes)):
                gene = chromosom[i]
                if used_gene[gene - 1] > 0:
                    selected_gene = genes_not_used[genes_not_used_index]
                    chromosom[i] = selected_gene
                    genes_not_used_index += 1

                used_gene[gene - 1] += 1

        assert set(chromosom) == set(self.nodes)  # check if valid solution
        return chromosom
