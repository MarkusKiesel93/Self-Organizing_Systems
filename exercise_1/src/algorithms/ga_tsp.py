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
        for i in range(self.population_size):
            population.append(np.random.permutation(self.dimension))
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
        child = np.full(self.dimension, -1, np.int32)
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        mother_genes_index = np.arange(cutoff_from, cutoff_to + 1)
        child[mother_genes_index] = mother[mother_genes_index]
        # todo: improve cluttered code (should work more efficently with numpy operations)
        for i in range(len(child)):
            if child[i] < 0:
                if father[i] not in child:
                    child[i] = father[i]
        genes_not_used_from_fahter = []
        for gene in father:
            if gene not in mother[mother_genes_index] and gene not in child:
                genes_not_used_from_fahter.append(gene)
        for i in range(len(child)):
            if child[i] < 0:
                if len(genes_not_used_from_fahter) > 0:
                    child[i] = genes_not_used_from_fahter.pop(0)
        genes_not_used = list(set(self.nodes).difference(set(child)))
        for gene in set(self.nodes).difference(set(child)):
            if child[i] < 0:
                child[i] = genes_not_used.pop(0)
        assert (child >= 0).all()
        return child
