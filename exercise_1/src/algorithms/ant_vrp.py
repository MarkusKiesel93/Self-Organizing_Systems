from typing import List
import numpy as np

from .ant import Ant


class AntVRP(Ant):
    def __init__(self, weights, nodes, count, demand, capacity, **kwargs) -> None:
        super().__init__(weights, nodes, **kwargs)
        self.demand = demand
        self.max_capacity = capacity
        self.count = count
        self.prepare(probabilities=None)

    def prepare(self, probabilities):
        self.pheromones_segregated = np.zeros(self.weights.shape)
        self.probabilities = probabilities

        self.start_node = self.nodes[self.count % self.nodes.shape[0]] # one ant per node if #ants == nodes
        self.current_node = self.start_node
        self.capacity = self.max_capacity - self.demand[self.current_node]
        if self.current_node == 0:
            self.path: List = [self.current_node]
        else:
            self.path: List = [0, self.current_node]
        self.nodes_not_visited: np.array = self.nodes[self.nodes != self.current_node]  # all nodes except start node
        self.fitness: float = self.weights[0][self.current_node] # all routes must start from depot

    # move ant from one node to another based on the transition probabilities
    def move(self, candidate_ratio=1) -> None:

        # use probabilitys at current node -> only consider not visited nodes + depot
        probabilities_at_current_node = self.probabilities[self.current_node]

        # use candidates to only consider nearest nodes
        candidate_index = int(candidate_ratio * len(self.nodes))
        distances = np.argsort(self.weights[self.current_node][self.nodes_not_visited])[:candidate_index]
        candidates = self.nodes_not_visited[distances]

        # only consider nodes that fullfil the constraint
        nodes_not_visited_next = candidates[self.demand[candidates] <= self.capacity]
        if not 0 in nodes_not_visited_next:
            nodes_not_visited_next = np.insert(nodes_not_visited_next,0,0) # always be able to go back to the depot
        
        if len(nodes_not_visited_next) == 1: # only depot left
            selected_node = nodes_not_visited_next[0]
        else:
            probabilities_not_visited = probabilities_at_current_node[nodes_not_visited_next]
            probability_sum = probabilities_not_visited.sum()
            if probability_sum == 0:
                probabilities_not_visited = None # draw randomly (uniform) if no option is prefered
            else:
                probabilities_not_visited /= probability_sum  # rescale to norm 1

            selected_node = np.random.choice(nodes_not_visited_next, p=probabilities_not_visited)

        self.pheromones_segregated[self.current_node][selected_node] += self.pheromone_intensity
        self.nodes_not_visited = self.nodes_not_visited[self.nodes_not_visited != selected_node]
        
        # update values
        self.path.append(selected_node)
        self.fitness += self.weights[self.current_node][selected_node]
        self.current_node = selected_node
        self.capacity -= self.demand[selected_node]

        # refresh capacity when depot was visited
        if selected_node == 0:
            self.capacity = self.max_capacity

        # move back to start if finished
        if self.has_finished():
            self.fitness += self.weights[self.current_node][0] # close loop
            self.path.append(0)
            self.pheromones_segregated /= self.fitness  
            
    # determine when ant is finished
    def has_finished(self) -> bool:
        return len(self.nodes_not_visited) == 0
