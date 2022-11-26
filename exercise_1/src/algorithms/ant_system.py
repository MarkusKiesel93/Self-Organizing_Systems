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

        visibility_choice = kwargs.get("visibility", "distance")
        if visibility_choice == "distance":
            self.visibility = np.maximum(np.power(problem_instance.astype('float64'), -1, where=(problem_instance != 0.0)), 0)  # 1/n_ij
        elif visibility_choice == "saving_function":
            # n_ij = d_i0 + d_0j - g* d_ij + f * |d_i0 - d_0j|
            f = kwargs.get("f", 2)
            g = kwargs.get("g", 2)
            di0 = np.zeros_like(problem_instance)
            d0j = np.zeros_like(problem_instance)
            di0[:,:] = problem_instance[:,0]
            di0 = di0.T

            d0j[:,:] = problem_instance[0,:]

            self.visibility = di0 + d0j - problem_instance.astype('float64') * g + f * np.absolute(di0 - d0j)

        self.candidate_ratio = kwargs.get("candidate_ratio")
        self.best_rate = kwargs.get("best_rate", 0.1)
        self.trail_update = kwargs.get("trail_update", "all")
        self.alpha = kwargs.get('alpha', 1)
        self.beta = kwargs.get('beta', 1)
        self.time = kwargs.get('time', 100)
        self.evaporation_coefficient: float = kwargs.get('evaporation_coefficient', 0.7)
        self.pheromone_intensity = kwargs.get('pheromone_intensity', 1)
        self.number_of_ants = kwargs.get('number_of_ants', 20)
        self.debug_mode = kwargs.get('debug_mode', False)

        self.trail_intensity: np.ndarray = np.full(self.problem_instance.shape, 0.001)  # tau
        self.best_fitness_at_time_point: List[float] = []
        self.best_path: List[int] = []

        # vrp constraints
        self.demand = kwargs.get('demand', None)
        self.capacity = kwargs.get('capacity', None)

    def run(self) -> None:
        # create ants
        ants = [self.ant_class(
            self.problem_instance,
            self.nodes,
            pheromone_intensity=self.pheromone_intensity,
            count=i,
            demand=self.demand,
            capacity=self.capacity,
            alpha=self.alpha,
            beta=self.beta
            ) for i in range(self.number_of_ants)]
        # iterate time points
        for t in tqdm(np.arange(self.time), desc='Time Point: '):
            # recalculate transition probabilities because of pheromone updates
            transition_probabilities = self._caluclate_transition_probabilities()
            # find soultion for all ants
            self._fitness_all_ants = []
            for ant in ants:
                ant.prepare(transition_probabilities)
                while not ant.has_finished():
                    ant.move(self.candidate_ratio)
                self._fitness_all_ants.append(ant.fitness)
            # evaluate ants
            self._top_ant = np.argsort(self._fitness_all_ants)[0]

            # store historical best path
            if t == 0 or self._fitness_all_ants[self._top_ant] < np.min(self.best_fitness_at_time_point):
                self.best_path = ants[self._top_ant].path
                self.best_pheromones = ants[self._top_ant].pheromones_segregated

            self.best_fitness_at_time_point.append(self._fitness_all_ants[self._top_ant])

            # print info
            if self.debug_mode:
                print(f'Time Point: {t + 1}')
                print(f'Top fitness: {self._fitness_all_ants[self._top_ant]}')
                print(f'Trail intensity: {self.trail_intensity}')
                print(f'Visibility: {self.visibility}')
                print(f'Solution: {ants[self._top_ant].path}')
            # update pheromones
            self._update_pheromones(ants, trail_update=self.trail_update, best_rate=self.best_rate)

    def fitness_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            'time_point': np.arange(1, self.time + 1),
            'fitness': self.best_fitness_at_time_point
        })

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
        return np.maximum(0,probabilities)

    # apply update rule to update trail_intensity matrix after iteration
    def _update_pheromones(self, ants, trail_update="all", best_rate=0.1):

        # collect pheromons over all ants
        if trail_update == "all":
            pheromone_updates = np.zeros(self.problem_instance.shape)
            
            for ant in ants:
                pheromone_updates += ant.pheromones_segregated

        # collect pheromons only from best ant    
        elif trail_update == "best":
            pheromone_updates = ants[self._top_ant].pheromones_segregated * len(ants) # scale pheromone intensity
        
        # collect pheromons from best_rate * len(ants) ants + ellitist ant
        elif trail_update == "elitist":
            best_rate =best_rate
            best_num = best_rate * len(ants)

            # use pheromones from best ants
            pheromone_updates = np.zeros_like(self.problem_instance)
            ranked_ants = np.argsort(self._fitness_all_ants)
            for e in range(int(best_num)-1):
                pheromone_updates += ants[ranked_ants[e]].pheromones_segregated 

            # use elitist ant
            pheromone_updates += self.best_pheromones * (len(ants) - best_num)

        # evaporate pheromones
        self.trail_intensity *= (1 - self.evaporation_coefficient)
        
        # add newly segregated pheromones
        self.trail_intensity += pheromone_updates
       