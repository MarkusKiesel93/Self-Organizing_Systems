import pandas as pd

from src.config import config


class TspLoader():
    def __init__(self):
        self.DATA_PATH = config.DATA_PATH / 'tsp'

    def load_problem_instance(self, type):
        method_name = f'_load_{type}'
        try:
            method = getattr(self, method_name) # gets the function by method name
            return method()
        except AttributeError:
            raise NotImplementedError(f'Metod {method_name} not implemented')

    def _load_FIVE(self):
        df = pd.read_csv(self.DATA_PATH / 'FIVE' / 'five_d.txt',
                         sep='  ',
                         header=None,
                         engine='python')
        return df.values
