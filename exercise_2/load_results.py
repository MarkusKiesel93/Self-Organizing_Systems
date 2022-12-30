import pandas as pd
import numpy as np
from pathlib import Path

RESULTS_PATH = Path(__file__).parent / 'results'
MIN_ITERATIONS_BY_EXPERIMENT = 10
PARAM_COLUMNS = ['fitness_function', 'use_constraint', 'constraint_handling_method', 'constraint',
                 'particle_speed_limit', 'population_size', 'personal_confidence', 'swarm_confidence',
                 'particle_inertia', 'constraint_r']
RESULT_COLUMNS_ALL = ['fitness', 'optimum', 'iterations', 'optimum_reached', 'iterations_to_opt']
RESULT_COLUMNS = ['fitness', 'optimum_reached', 'iterations_to_opt']
FITNESS_FUNCTIONS = ['Shubert function', "Booth's function", 'Schwefel function']


def load_setup_1(final_df_only=True):
    NUMBER_OF_EXPERIMENTS = 27 * 228 / 3
    FOLDER = 'setup_1'
    df_full, df_params, df_results, df_to_eval = load_setup(FOLDER)
    sanity_check(df_full, df_params, df_results, df_to_eval, NUMBER_OF_EXPERIMENTS)
    sanity_check_setup_1(df_params)
    if final_df_only:
        return df_to_eval
    else:
        return df_full, df_params, df_results, df_to_eval


def load_setup_2(final_df_only=True):
    NUMBER_OF_EXPERIMENTS = 3 * 12
    FOLDER = 'setup_2'
    df_full, df_params, df_results, df_to_eval = load_setup(FOLDER)
    sanity_check(df_full, df_params, df_results, df_to_eval, NUMBER_OF_EXPERIMENTS)
    sanity_check_setup_2(df_params)
    if final_df_only:
        return df_to_eval
    else:
        return df_full, df_params, df_results, df_to_eval


def load_setup_full(folder):
    df_full = pd.concat([pd.read_csv(file_path) for file_path in (RESULTS_PATH / folder).glob('*.csv')])
    df_full.constraint_r.replace(-0.15, '-', inplace=True)  # default was used when no constraint used -> change to NAN
    df_full[PARAM_COLUMNS] = df_full[PARAM_COLUMNS].fillna('-')  # pevent ignoring nan values in params on groupby
    return df_full


def load_setup(folder):
    df_full = load_setup_full(folder)
    # normalize fitness
    df_full.fitness = df_full.fitness / df_full.optimum
    # optimum always one
    df_full.optimum = df_full.optimum / df_full.optimum
    df_params = df_full[PARAM_COLUMNS].drop_duplicates()
    df_results = df_full.groupby(PARAM_COLUMNS)[RESULT_COLUMNS_ALL].mean()
    df_to_eval = df_full.groupby(PARAM_COLUMNS)[RESULT_COLUMNS_ALL].mean().reset_index()
    return df_full, df_params, df_results, df_to_eval


def sanity_check(df_full, df_params, df_results, df_to_eval, number_of_experiments):
    # sanity check for full df
    assert df_full.notna().all(axis=None)
    assert (df_full.groupby(PARAM_COLUMNS)['number'].count() >= MIN_ITERATIONS_BY_EXPERIMENT).all()

    # sanity check params
    assert df_params.shape == (number_of_experiments, len(PARAM_COLUMNS))
    assert set(df_params.fitness_function.unique()) == set(FITNESS_FUNCTIONS)
    assert df_params[~df_params.use_constraint]\
        .replace('-', np.nan)[['constraint_handling_method', 'constraint', 'constraint_r']]\
        .isna().all(axis=None)
    assert df_params[df_params.use_constraint][['constraint_handling_method', 'constraint', 'constraint_r']]\
        .notna().all(axis=None)

    # sanity check results
    assert df_results.shape == (number_of_experiments, len(RESULT_COLUMNS_ALL))
    assert df_results.fitness.min() >= 0.0
    assert df_results.fitness.max() <= 1.0
    assert df_results.optimum.unique() == [1.0]
    assert df_results.iterations.unique() == [500.0]
    assert df_results.optimum_reached.min() >= 0.0
    assert df_results.optimum_reached.max() <= 1.0
    assert df_results.iterations_to_opt.min() >= 0
    assert df_results.iterations_to_opt.max() <= 500

    # sanity check df to eval
    assert df_to_eval.shape == (number_of_experiments, len(PARAM_COLUMNS) + len(RESULT_COLUMNS_ALL))


def sanity_check_setup_1(df_params):
    # sanity check params
    assert set(df_params.use_constraint.unique()) == set([True, False])
    assert set(df_params.constraint_handling_method.unique()) == set(['-', 'Penalty Method', 'Rejection Method'])
    assert set(df_params.constraint.unique()) == set(['-', 'Constraint 3', 'Constraint 5', 'Constraint 10'])
    assert df_params.particle_speed_limit.unique() == [13]
    assert set(df_params.population_size.unique()) == set([5, 10, 35, 80])
    assert set(df_params.personal_confidence.unique()) == set([0.5, 1.0, 1.5])
    assert set(df_params.swarm_confidence.unique()) == set([0.5, 1.0, 1.5])
    assert set(df_params.particle_inertia.unique()) == set([0.1, 0.5, 0.9])
    assert set(df_params.constraint_r.unique()) == set(['-', -1.0, -1.5, -2.0])


def sanity_check_setup_2(df_params):
    assert set(df_params.use_constraint.unique()) == set([False])
    assert set(df_params.constraint_handling_method.unique()) == set(['-'])
    assert set(df_params.constraint.unique()) == set(['-'])
    assert set(df_params.particle_speed_limit.unique()) == set([2, 10, 19])
    assert set(df_params.population_size.unique()) == set([5, 10, 35, 80])
    assert set(df_params.personal_confidence.unique()) == set([0.8])
    assert set(df_params.swarm_confidence.unique()) == set([1.6])
    assert set(df_params.particle_inertia.unique()) == set([0.3])
    assert set(df_params.constraint_r.unique()) == set(['-'])
