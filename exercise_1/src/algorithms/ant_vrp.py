from typing import List
import numpy as np

from .ant import Ant


class AntVRP(Ant):
    def __init__(self, weights, nodes, count, demand, capacity, **kwargs) -> None:
        super().__init__(weights, nodes, **kwargs)
        self.demand = demand
        self.max_capacity = capacity
        self.capacity = self.max_capacity
        self.start_node = self.nodes[count % self.nodes.shape[0]] # one ant per node if #ants == nodes
        self.current_node = self.start_node
        self.path: List = [self.current_node]
        self.nodes_not_visited: np.array = self.nodes[self.nodes != self.current_node]  # all nodes except start node
        self.fitness: float = self.weights[0][self.current_node] # all routes must start from depot

    # move ant from one node to another based on the transition probabilities
    def move(self) -> None:
        # use probabilitys at current node -> only consider not visited nodes + depot
        probabilities_at_current_node = self.probabilities[self.current_node]

        nodes_not_visited_next = self.nodes_not_visited[self.demand[self.nodes_not_visited] <= self.capacity]
        if not 0 in nodes_not_visited_next:
            nodes_not_visited_next = np.insert(nodes_not_visited_next,0,0)

        probabilities_not_visited = probabilities_at_current_node[nodes_not_visited_next]
        probabilities_not_visited /= probabilities_not_visited.sum()  # rescale to norm 1
        selected_node = np.random.choice(nodes_not_visited_next, p=probabilities_not_visited)
        # update values
        self.path.append(selected_node)
        self.fitness += self.weights[self.current_node][selected_node]
        self.pheromones_segregated[self.current_node][selected_node] = self.pheromone_intensity
        self.nodes_not_visited = self.nodes_not_visited[self.nodes_not_visited != selected_node]
        self.current_node = selected_node
        self.capacity -= self.demand[selected_node]

        # refresh capacity when depot was visited
        if selected_node == 0:
            self.capacity = self.max_capacity

        # move back to start if finished
        if self.has_finished():
            self.fitness += self.weights[self.current_node][self.start_node]
            self.pheromones_segregated /= self.fitness  # self.weights[self.current_node][selected_node]
            self.current_node = self.start_node

    # determine when ant is finished
    def has_finished(self) -> bool:
        return len(self.nodes_not_visited) == 0
