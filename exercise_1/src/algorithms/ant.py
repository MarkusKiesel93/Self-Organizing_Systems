import random


class Ant():
    def __init__(self, nodes) -> None:
        self.nodes = nodes
        self.fitness = []
        self.nodes_not_visited = self.nodes[1:]  # all nodes except start node
        self.current_node = 0

    def move(self, probabilities) -> None:
        selected_node = random.choice(self.nodes, weights=probabilities[self.current_node])
        self.nodes_not_visited.remove(selected_node)
        self.nodes_visited.append(selected_node)
        self.current_node = selected_node

    def has_finished(self):
        return len(self.nodes_not_visited) == 0
