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

    def _crossover(self, mother: np.array, father: np.array) -> List[np.array]:
        # create child from cossover of father and mother
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        father_gene_indices = np.array([val < cutoff_from or val > cutoff_to for val in range(self.dimension)])
        mother_gene_indices = ~father_gene_indices  # inverse indices of fahter
        first_child = np.copy(mother)
        first_child[father_gene_indices] = father[father_gene_indices]
        first_child = self._repair_chromosom(first_child, mother_gene_indices, father_gene_indices)
        second_child = np.copy(father)
        second_child[mother_gene_indices] = mother[mother_gene_indices]
        second_child = self._repair_chromosom(second_child, father_gene_indices, mother_gene_indices)
        return [first_child, second_child]

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
