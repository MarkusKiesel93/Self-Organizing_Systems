from typing import List
import numpy as np


class Ant():
    def __init__(self, weights, nodes, pheromone_intensity=1, **kwargs) -> None:
        self.weights: np.ndarray = weights
        self.nodes = nodes
        self.pheromone_intensity = pheromone_intensity

        self.start_node = np.random.choice(self.nodes)
        self.current_node = self.start_node
        self.fitness: float = 0.0
        self.path: List = [self.current_node]
        self.nodes_not_visited: np.array = self.nodes[self.nodes != self.current_node]  # all nodes except start node
        self.pheromones_segregated: np.ndarray = np.zeros(self.weights.shape)
        self.probabilities: np.ndarray = None

    # reset ant values for new iteration and set probabilities for run
    def prepare(self, probabilities, **kwargs):
        self.fitness = 0.0
        self.path = [self.current_node]
        self.nodes_not_visited = self.nodes[self.nodes != self.current_node]
        self.pheromones_segregated = np.zeros(self.weights.shape)
        self.probabilities = probabilities

    # move ant from one node to another based on the transition probabilities
    def move(self) -> None:
        raise NotImplementedError('implment how ant moves')

    # determine when ant is finished
    def has_finished(self) -> bool:
        raise NotImplementedError('implment when ant finished')
