import random

import numpy as np

from .ant import Ant


class AntQueens(Ant):
    def __init__(self, weights, nodes) -> None:
        super().__init__(weights, nodes)
        self.N = weights.shape[0]
        self.visited = []
        self.threats = np.ones((self.N, self.N))
        self.alpha = 1  # TODO
        self.beta = 1  # TODO

    def prepare(self, probabilities):
        super().prepare(probabilities)
        self.path = []
        self.visited = []
        self.threats = np.ones((self.N, self.N))
        print(f'P')
        print(probabilities)
        print(self.weights)

    # move ant from one node to another based on the transition probabilities
    def move(self) -> None:
        i = len(self.path) - 1
        index_in_column = self.next_move(self.probabilities[:][i], self.threats[:][i], self.visited)
        self.pheromones_segregated[i][index_in_column] = self.Q
        self.visited.append(index_in_column)
        self.updated_threats(index_in_column, i, self.threats)
        self.path.append(index_in_column)

    # determine when ant is finished
    def has_finished(self) -> bool:
        if len(self.path) == self.N:
            self.fitness = self.eval_tour(self.path, self.threats)
            self.pheromones_segregated /= self.fitness  # self.weights[self.current_node][selected_node]
            print(f'F: {self.fitness}')
            print(self.path)
            print(self.pheromones_segregated)
            return True
        return False

    def updated_threats(self, row, column, threats):
        for j in range(1, self.N - column):
            threats[row][column + j] += 1  # update row
            if row + j < self.N:  # update lower diagonal
                threats[row + j][column + j] += 1
            if row - j >= 0:  # update upper diagonal
                threats[row - j][column + j] += 1

    def next_move(self, pheromone, threats, visited):
        pheromone = np.copy(pheromone)  # Careful: python passes arguments "by-object"; pheromone is mutable
        pheromone[list(visited)] = 0
        colomn_prob = pheromone ** self.alpha * ((1.0 / threats) ** self.beta)
        norm_colomn_prob = colomn_prob / colomn_prob.sum()

        move = np.random.choice(range(self.N), 1, p=norm_colomn_prob)[0]
        return move

    def eval_tour(self, path, threats):
        res = 0
        for column in range(len(path)):
            row = path[column]
            res += threats[row][column]
        return res
