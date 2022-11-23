import numpy as np

from .ant import Ant


class AntTSP(Ant):
    def __init__(self, weights, nodes, **kwargs) -> None:
        super().__init__(weights, nodes, **kwargs)

    # move ant from one node to another based on the transition probabilities
    def move(self) -> None:
        # use probabilitys at current node -> only consider not visited nodes
        probabilities_at_current_node = self.probabilities[self.current_node]
        proabilities_not_visited = probabilities_at_current_node[self.nodes_not_visited]
        proabilities_not_visited /= proabilities_not_visited.sum()  # rescale to norm 1
        selected_node = np.random.choice(self.nodes_not_visited, p=proabilities_not_visited)
        # update values
        self.path.append(selected_node)
        self.fitness += self.weights[self.current_node][selected_node]
        self.pheromones_segregated[self.current_node][selected_node] = self.pheromone_intensity
        self.nodes_not_visited = self.nodes_not_visited[self.nodes_not_visited != selected_node]
        self.current_node = selected_node
        # move back to start if finished
        if self.has_finished():
            self.fitness += self.weights[self.current_node][self.start_node]
            self.pheromones_segregated /= self.fitness  # self.weights[self.current_node][selected_node]
            self.current_node = self.start_node

    # determine when ant is finished
    def has_finished(self) -> bool:
        return len(self.nodes_not_visited) == 0
