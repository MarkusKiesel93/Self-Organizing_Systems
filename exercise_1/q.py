import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.problem_loaders.tsp_loader import TSPLoader
from src.algorithms.ga_queens import GeneticAlgorithmQueens

df = pd.DataFrame(np.array(np.zeros(13)))
ga = GeneticAlgorithmQueens(df, population_size=20, max_generations=10000, mutation_rate=1)
ga.run()
ga_stats = ga.fitness_df()
optimal_fitness = 1
chart = sns.lineplot(data=ga_stats, x='generation', y='fitness')
plt.ylim(optimal_fitness * 0.9, ga_stats.fitness.max() * 1.1)
chart.axhline(1, color='red', linestyle='--')
plt.show()