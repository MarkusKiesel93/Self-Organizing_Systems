from src.algorithms.ant_system import AntSystem
from src.algorithms.ant_queens import AntQueens
import numpy as np

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.algorithms.alex.gh import AntforTSP


n = 8
Nant = 10
Niter = 10 ** 4
rho = 0.85
tries = 10
percent_of_best_path_to_deposit = 0.3

aco = AntforTSP(n, Nant, Niter, rho, alpha=1, beta=1,
                percent_of_best_path_to_deposit=percent_of_best_path_to_deposit)
((path, f), iter_found) = aco.run()

stats_df = aco.fitness_df()
optimal_fitness = n
chart = sns.lineplot(data=stats_df, x='time_point', y='fitness')
plt.ylim(optimal_fitness * 0.9, stats_df.fitness.max() * 1.1)
chart.axhline(optimal_fitness, color='red', linestyle='--')
plt.show()