import re
import numpy as np
import pandas as pd

from src.config import config


class TSPLoader():
    def __init__(self, problem_name):
        self.DATA_PATH = config.DATA_PATH / 'tsp'
        self.porblem_name = problem_name

    def load_problem_instance(self) -> np.ndarray:
        method_name = f'_load_{self.porblem_name}'
        try:
            method = getattr(self, method_name)  # gets the function by method name
            problem_instance, best_solution = method()
            assert problem_instance.diagonal().sum() == 0.0  # weights to same node have to be 0
            assert problem_instance.shape[0] == problem_instance.shape[1]  # symmetric matrix
            return problem_instance, best_solution
        except AttributeError:
            raise NotImplementedError(f'Metod {method_name} not implemented')

    def _load_FIVE(self):
        path = self.DATA_PATH / 'FIVE'
        df = pd.read_csv(path / 'five_d.txt',
                         sep='  ',
                         header=None,
                         engine='python')
        best_solution = self._load_values_by_line(path / 'five_s.txt')
        return df.values, best_solution

    def _load_ATT48(self):
        path = self.DATA_PATH / 'ATT48'
        edge_valus = []
        with open(path / 'att48_d.txt', 'r') as file:
            for line in file.readlines():
                edge_valus.append([int(value) for value in re.split(r'[\s,]+', line) if value != ''])
        best_solution = self._load_values_by_line(path / 'att48_s.txt')
        return np.array(edge_valus), best_solution[:-1]

    def _load_values_by_line(self, path) -> np.array:
        values = []
        with open(path, 'r') as file:
            for line in file.readlines():
                value = line.strip()
                if len(value) > 0:
                    values.append(int(value))
        return np.array(values) - 1  # use nodes starting by zero -> use as index
