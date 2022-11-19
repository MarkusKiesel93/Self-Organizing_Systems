from typing import List
import numpy as np
from tqdm import tqdm

from .ant import Ant


class AntSystemTSP():
    def __init__(self, problem_instance: np.ndarray, **kwargs) -> None:
        self.problem_instance: np.ndarray = problem_instance
        self.dimension: int = self.problem_instance.shape[0]
        self.nodes: np.array = np.arange(self.dimension)
        self.visibility = np.power(problem_instance, -1)  # defines the visibilit 1 / n_ij

        self.alpha = kwargs.get('alpha', 1)
        self.beta = kwargs.get('beta', 1)
        self.time = kwargs.get('time', 100)
        self.number_of_ants = ('number_of_ants', 20)

        self.trail_intensity: np.ndarray = np.full(self.problem_instance.shape, 0.001)  # tau
        self.evaporation_coefficient: int = None  # p
        self.best_fitness_at_time_point: List[float] = []

        self.debug_mode = kwargs.get('debug_mode', False)

    def run(self) -> None:
        start_target_node = 0
        ants = [Ant(self.nodes) for _ in range(self.number_of_ants)]
        # iterate time points
        for t in tqdm(np.arange(self.time), desc='Time Point: '):
            # find soultion for all ants
            fitness_all_ants = []
            for ant in ants:
                transition_probabilities = self._caluclate_transition_probabilities(ant)
                while not ant.has_finished():
                    ant.move(transition_probabilities)
                fitness_all_ants.append(self._evaluate_fitness(ant.nodes_visited))
            top_solution = np.argsort(fitness_all_ants)[0]
            self.best_fitness_at_time_point.append(fitness_all_ants[top_solution])
            self._update_pheromones()

    def _caluclate_transition_probabilities(self, ant: Ant):
        probabilities = np.zeros(self.problem_instance.shapes)
        for node_from in ant.nodes_not_visited:
            for node_to in self.nodes:
                probabilities[node_from][node_to] = (
                    np.power(self.trail_intensity[node_from][node_to], self.alpha) *
                    np.power(self.visibility[node_from][node_to], self.beta)
                )
        probabilities = probabilities.apply(lambda row: row / row.sum, axis=0)
        return probabilities

    def _update_pheromones(self):
        # apply update rule to update trail_intensity matrix after iteration
        pass

