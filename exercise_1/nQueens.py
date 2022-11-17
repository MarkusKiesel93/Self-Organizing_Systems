import numpy as np
from geneticalgorithm import geneticalgorithm as ga

N = 12


def attacks_diagonal(queens, queen, queen_col, direction=1):
    attacks = 0
    row = queen - (queen_col * direction)
    # print(f"Checking for queen_col: {queen_col}")
    for col in range(0, N):
        # print(f"({row}|{col}): {queens[col]}")

        if queen_col == col:
            row += direction
            continue

        if row < 0 or row >= N:
            row += direction
            continue

        if queens[col] == row:
            attacks += 1

        row += direction

    return attacks


def attacks_horizontal(queens, queen):
    queens_in_same_row = 0
    for another_queen in queens:
        if another_queen == queen:
            queens_in_same_row += 1

    if queens_in_same_row > 1:
        return 1

    return 0


def f(queens):
    attacks = 0
    for col in range(0, N):
        queen = queens[col]  # row
        attacks += attacks_horizontal(queens, queen)
        attacks += attacks_diagonal(queens, queen, col)
        attacks += attacks_diagonal(queens, queen, col, -1)

    return attacks


# print(f([7, 2, 0, 6, 1, 4, 3, 5, ]))
# if True:
#     exit(0)

varbound = np.array([[0, N - 1]] * N)

# print(varbound)

algorithm_param = {'max_num_iteration': 1000,
                   'population_size': 100,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

model = ga(function=f, dimension=N, variable_type='int', variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)

model.run()
