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
            problem_instance = method()
            assert problem_instance.diagonal().sum() == 0.0  # weights to same node have to be 0
            assert problem_instance.shape[0] == problem_instance.shape[1]  # symmetric matrix
            return problem_instance
        except AttributeError:
            raise NotImplementedError(f'Metod {method_name} not implemented')

    def _load_FIVE(self):
        df = pd.read_csv(self.DATA_PATH / 'FIVE' / 'five_d.txt',
                         sep='  ',
                         header=None,
                         engine='python')
        return df.values

    def _load_ATT48(self):
        edge_valus = []
        with open(self.DATA_PATH / 'ATT48' / 'att48_d.txt', 'r') as file:
            for line in file:
                edge_valus.append([int(value) for value in re.split(r'[\s,]+', line) if value != ''])
        return np.array(edge_valus)
