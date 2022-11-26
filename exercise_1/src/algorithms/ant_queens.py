import random

import numpy as np

from .ant import Ant


class AntQueens(Ant):
    def __init__(self, weights, nodes, **kwargs) -> None:
        super().__init__(weights, nodes, **kwargs)
        self.N = weights.shape[0]
        self.visited = []
        self.threats = np.ones((self.N, self.N))
        self.alpha = kwargs.get('alpha', 1)
        self.beta = kwargs.get('beta', 1)

    def prepare(self, probabilities, **kwargs):
        super().prepare(probabilities)
        self.path = []
        self.visited = []
        self.threats = np.ones((self.N, self.N))

    def move(self, candidate_ratio=1) -> None:
        i = len(self.path)
        index_in_column = self.next_move(self.weights[:][i], self.threats[:][i], self.visited)
        self.pheromones_segregated[i][index_in_column] = self.pheromone_intensity
        self.visited.append(index_in_column)
        self.updated_threats(index_in_column, i, self.threats)
        self.path.append(index_in_column)

    def has_finished(self) -> bool:
        if len(self.path) == self.N:
            self.fitness = self.evaluate_path(self.path, self.threats)
            self.pheromones_segregated /= self.fitness
            # if self.fitness == self.N:
            #     print(f'Solution with fitness {self.fitness}: {self.path}')
            return True
        return False

    def updated_threats(self, row, column, threats):
        for j in range(1, self.N - column):
            threats[row][column + j] += 1
            if row + j < self.N:
                threats[row + j][column + j] += 1
            if row - j >= 0:
                threats[row - j][column + j] += 1

    def next_move(self, pheromone, threats, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        colomn_prob = pheromone ** self.alpha * ((1.0 / threats) ** self.beta)
        norm_colomn_prob = colomn_prob / colomn_prob.sum()

        move = np.random.choice(range(self.N), 1, p=norm_colomn_prob)[0]
        return move

    def evaluate_path(self, path, threats):
        res = 0
        for column in range(len(path)):
            row = path[column]
            res += threats[row][column]
        return res
