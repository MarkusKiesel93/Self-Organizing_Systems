from typing import List
import random
import numpy as np

from .ga import GeneticAltorithm


class GeneticAltorithmTSP(GeneticAltorithm):
    def __init__(self, problem_instance, **kwargs) -> None:
        super().__init__(problem_instance, **kwargs)

    def _evaluate_fitness(self, chromosome: np.array) -> float:
        assert len(chromosome) == self.problem_instance.shape[0]
        weights = []
        for i in range(len(chromosome)):
            from_node = chromosome[i]
            # current node to next node
            if i < len(chromosome) - 1:
                to_node = chromosome[i + 1]
            # last node to first node
            else:
                to_node = chromosome[0]
            weights.append(self.problem_instance[from_node][to_node])
        return sum(weights)

    def _generate_initial_population(self) -> List[np.array]:
        population = []
        population_route_matrix = []
        disimilarity_goal = 0.95
        for _ in range(int(self.population_size * 0.2)):
            chromosome = np.random.permutation(self.dimension)
            route_matrix = self._to_route_matrix(chromosome)
            population.append(chromosome)
            population_route_matrix.append(route_matrix)
        while len(population) < self.population_size:
            chromosome = np.random.permutation(self.dimension)
            route_matrix = self._to_route_matrix(chromosome)
            mean_disimilarity = np.mean(
                [self._route_matrix_disimilarity(route_matrix, rm) for rm in population_route_matrix])
            if mean_disimilarity >= disimilarity_goal:
                population.append(chromosome)
                population_route_matrix.append(route_matrix)
            else:
                disimilarity_goal -= 0.001
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

    def _crossover(self, mother: np.array, father: np.array) -> List[np.array]:
        children = []
        # create child from cossover of father and mother
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        father_gene_indices = np.array([val < cutoff_from or val > cutoff_to for val in range(self.dimension)])
        mother_gene_indices = ~father_gene_indices  # inverse indices of fahter
        first_child = np.copy(mother)
        first_child[father_gene_indices] = father[father_gene_indices]
        first_child = self._repair_chromosom(first_child, mother_gene_indices, father_gene_indices)
        children.append(first_child)
        if self.two_children_per_crossover:
            second_child = np.copy(father)
            second_child[mother_gene_indices] = mother[mother_gene_indices]
            second_child = self._repair_chromosom(second_child, father_gene_indices, mother_gene_indices)
            children.append(second_child)
        return children

    # correct child genes to get valid solution
    def _repair_chromosom(self, chromosom, gene_indices_primary, gene_indices_secondary):
        genes_not_used = np.setdiff1d(self.nodes, chromosom)
        if genes_not_used.size > 0:
            # correct only fahter part of solution
            for i in self.nodes[gene_indices_secondary]:
                if chromosom[i] in chromosom[gene_indices_primary]:
                    selected_gene = np.random.choice(genes_not_used)
                    genes_not_used = genes_not_used[genes_not_used != selected_gene]
                    chromosom[i] = selected_gene
        assert set(chromosom) == set(self.nodes)  # check if valid solution
        return chromosom

    def _to_route_matrix(self, chromosome) -> np.ndarray:
        route_matrix = np.zeros((self.dimension, self.dimension))
        for i in range(1, self.dimension):
            route_matrix[chromosome[i-1]][chromosome[i]] = 1
        route_matrix[chromosome[-1]][chromosome[0]] = 1
        return route_matrix

    def _route_matrix_disimilarity(self, route_matrix_a, route_matrix_b):
        ones_where_not_same_edge = np.abs(route_matrix_a - route_matrix_b)
        # sum at most 2 * dimension -> all edges different
        return ones_where_not_same_edge.sum() / (2 * self.dimension)
