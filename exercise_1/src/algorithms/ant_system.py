from typing import List
import numpy as np
import pandas as pd
from tqdm import tqdm

from .ant import Ant


class AntSystem():
    def __init__(self, ant_class: Ant, problem_instance: np.ndarray, **kwargs) -> None:
        self.ant_class = ant_class
        self.problem_instance: np.ndarray = problem_instance
        self.dimension: int = self.problem_instance.shape[0]
        self.nodes: np.array = np.arange(self.dimension)
        self.visibility = np.power(problem_instance.astype('float64'), -1, where=(problem_instance != 0.0))  # 1/n_ij

        self.alpha = kwargs.get('alpha', 1)
        self.beta = kwargs.get('beta', 1)
        self.time = kwargs.get('time', 100)
        self.evaporation_coefficient: int = kwargs.get('evaporation_coefficient', 0.7)
        self.number_of_ants = kwargs.get('number_of_ants', 20)
        self.debug_mode = kwargs.get('debug_mode', False)

        self.trail_intensity: np.ndarray = np.full(self.problem_instance.shape, 0.001)  # tau
        self.best_fitness_at_time_point: List[float] = []

    def run(self) -> None:
        ants = [self.ant_class(self.problem_instance, self.nodes) for _ in range(self.number_of_ants)]
        # iterate time points
        for t in tqdm(np.arange(self.time), desc='Time Point: '):
            # recalculate transition probabilities because of pheromone updates
            transition_probabilities = self._caluclate_transition_probabilities()
            # find soultion for all ants
            fitness_all_ants = []
            for ant in ants:
                ant.prepare(transition_probabilities)
                while not ant.has_finished():
                    ant.move()
                fitness_all_ants.append(ant.fitness)
            # evaluate ants
            top_ant = np.argsort(fitness_all_ants)[0]
            self.best_fitness_at_time_point.append(fitness_all_ants[top_ant])
            # print info
            if self.debug_mode:
                print(f'Time Point: {t + 1}')
                print(f'Top fitness: {fitness_all_ants[top_ant]}')
                print(f'Solution: {ants[top_ant].path}')
            # update pheromones
            self._update_pheromones(ants)

    def fitness_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            'time_point': np.arange(1, self.time + 1),
            'fitness': self.best_fitness_at_time_point
        })

    # todo: why calculated by ant k ?
    # todo: it seems to me the information is the same for all ants
    # todo: maybe only consider whicht nodes already visited by ant and resacel probabilities in Ant?
    def _caluclate_transition_probabilities(self):
        probabilities = np.zeros(self.problem_instance.shape)
        # nominator for each inedx i, j
        for node_from in self.nodes:
            for node_to in self.nodes:
                probabilities[node_from][node_to] = (
                    np.power(self.trail_intensity[node_from][node_to], self.alpha) *
                    np.power(self.visibility[node_from][node_to], self.beta)
                )
        # denominator -> devide by sum in row -> get probabilities
        probabilities /= probabilities.sum(axis=1, keepdims=True)
        return probabilities

    # apply update rule to update trail_intensity matrix after iteration
    def _update_pheromones(self, ants):
        pheromone_updates_all_ants = np.zeros(self.problem_instance.shape)
        # collect pheromons over all ants
        for ant in ants:
            pheromone_updates_all_ants += ant.pheromones_segregated
        # evaporate pheromones
        self.trail_intensity *= self.evaporation_coefficient
        # add newly segregated pheromones
        self.trail_intensity += pheromone_updates_all_ants
