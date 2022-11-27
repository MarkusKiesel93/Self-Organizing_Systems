from typing import List, Tuple
import random
import math
import optuna

import numpy as np
import scipy.spatial
import python_tsp.exact # https://github.com/fillipe-gsm/python-tsp

from tqdm import tqdm
from dataclasses import dataclass
from .ga import GeneticAltorithm

@dataclass
class Solution:
    chromosome:str
    fitness:float
    unfitness:float


class GeneticAltorithmVRP(GeneticAltorithm):
    def __init__(self, problem_instance, coordinates, demand, capacity, **kwargs) -> None:
        super().__init__(problem_instance, **kwargs)
        self.depot = coordinates[0]
        self.coordinates = coordinates[1:]
        self.dimension = self.coordinates.shape[0]
        self.demand = demand[1:] # remove depot demand
        self.total_demand = np.sum(demand)
        self.capacity = capacity
        self.num_vehicles = 0

    # genetic algorithm procedure
    def run(self, trial=None):
        # create initial population
        self.population = self._generate_initial_population()
        # run for max_generations
        for generation in tqdm(np.arange(self.max_generations), desc='Generation: '):
            next_population = []
            # calculate fitness and probabilities for current generation
            current_fitness, current_probabilities = self._calulate_population_fitness()
            top_solution = np.argsort(current_fitness)[0]
            self.best_fitness_in_generation.append(current_fitness[top_solution])
            self.best_chromosome = self.population[top_solution]

            # select elitists
            next_population.extend(self._select_elites(current_fitness))
            
            # generate next generation by crossover and mutation
            while len(next_population) < self.population_size:
                father = self._roulette(current_probabilities)
                mother = self._roulette(current_probabilities)
                child = self._crossover(father, mother)
                child = self._mutate(child)
                next_population.append(child)
            if self.debug_mode:
                print(f'Generation: {generation + 1}')
                print(f'Top fitness: {current_fitness[top_solution]}')
                print(f'Solution: {self.population[top_solution]}')
            self.population = next_population

            # report score for pruning
            if not trial is None:
                trial.report(current_fitness[top_solution], generation)

                if trial.should_prune():
                    raise optuna.TrialPruned()

    def _get_paths(self, chromosome) -> Tuple[List[np.ndarray], float]:
        """
        Returns a list of the vehicle paths and the total travel distance
        """
        paths = []
        total_distance = 0
        for v in range(self.num_vehicles):
            vehicle_coordinates_ind  = np.nonzero(chromosome == v)
            vehicle_coordinates  = self.coordinates[vehicle_coordinates_ind]
            index_helper = np.arange(chromosome.shape[0])[vehicle_coordinates_ind]
            # catch simple case with one city in vehicle list
            if vehicle_coordinates.shape[0] == 1:
                total_distance += 2*np.linalg.norm(vehicle_coordinates - self.depot)
                paths.append([0, index_helper[vehicle_coordinates] + 1])
                continue

            vehicle_coordinates = np.insert(vehicle_coordinates, 0, self.depot, axis=0)
            index_helper += 1
            index_helper = np.insert(index_helper, 0, 0, axis=0)
            
            distance_matrix = scipy.spatial.distance.cdist(vehicle_coordinates, vehicle_coordinates, 'euclidean')
            route, distance = python_tsp.exact.solve_tsp_dynamic_programming(distance_matrix)
            total_distance += distance

            paths.append(index_helper[route])
        return paths, total_distance

    def _calulate_population_fitness(self) -> Tuple[np.array, np.array]:
        population_fitness = np.zeros(self.population_size)
        for i in range(len(self.population)):
            population_fitness[i] = self.population[i].fitness
        minimization_fitness = np.ones(self.population_size) / population_fitness
        return population_fitness, minimization_fitness / minimization_fitness.sum()

    def _evaluate_fitness(self, chromosome: np.array) -> float:
        total_distance = 0.0
        for v in range(self.num_vehicles):
            vehicle_coordinates = self.coordinates[chromosome==v]

            # catch simple case with one city in vehicle list
            if vehicle_coordinates.shape[0] == 1:
                total_distance += 2*np.linalg.norm(vehicle_coordinates - self.depot)
                continue

            # add depot to every vehicle's path
            vehicle_coordinates = np.insert(vehicle_coordinates, 0, self.depot, axis=0)
            distance_matrix = scipy.spatial.distance.cdist(vehicle_coordinates, vehicle_coordinates, 'euclidean')
        
            _, distance = python_tsp.exact.solve_tsp_dynamic_programming(distance_matrix)
            total_distance += distance

        return total_distance

    def _evaluate_unfitness(self, chromosome: np.ndarray) -> float:
        """ 
        calculate unfitness as ratio of overloaded demand 
        per vehicle (overload / total demand) summed over allvehicles
        """
        total_unfitness = 0.0
        for v in range(self.num_vehicles):
            total_unfitness += max((np.sum(self.demand[chromosome == v]) - self.capacity) / self.total_demand, 0) # get overloading
        return total_unfitness

    def _generate_initial_population(self) -> List[Solution]:
        population = []

        # get approximative tsp solution
        distance_matrix = scipy.spatial.distance.cdist(self.coordinates, self.coordinates, 'euclidean')
        np.fill_diagonal(distance_matrix, np.inf)

        current_pos = 0
        tsp_path = [current_pos]

        visited_cities = 0
        while visited_cities < self.dimension - 1:
            next_position = np.argmin(distance_matrix[current_pos, :])
            distance_matrix[:, next_position] = np.inf
            tsp_path.append(next_position)

            current_pos = next_position
            visited_cities += 1

        # sweep
        # get sweep behavior
        self.num_vehicles = int(math.ceil(self.total_demand / self.capacity))
        tightness = self.total_demand / (self.capacity * self.num_vehicles)
        violation_threshold = 0.9 if tightness < 0.95 else 0.75

        # generate chromosomes
        for _ in range(self.population_size):
            chromosome = np.zeros((self.dimension), dtype=np.int0)
            start = random.randint(0, self.dimension-1)
            current_ind = start
            visited_cities = 0
            for v in range(self.num_vehicles):
                route_capacity = self.capacity

                # add until constraint violation occurs (of finished)
                while route_capacity > 0 and visited_cities < self.dimension:
                    #print(f"Set vehilce {v} at route index {current_ind} and route pos {tsp_path[current_ind]}")
                    chromosome[tsp_path[current_ind]] = v
                    route_capacity -= self.demand[tsp_path[current_ind]]
                    current_ind = (current_ind + 1) % (self.dimension)
                    visited_cities += 1
                
                # constraint violation rule 
                if route_capacity < 0:
                    rc = (route_capacity + self.demand[tsp_path[current_ind]]) / self.demand[tsp_path[current_ind]]

                    # remove last customer
                    if rc < violation_threshold:
                        current_ind = current_ind - 1 if current_ind > 0 else self.dimension - 1
                        visited_cities -= 1

                        #print(f"Remove last customer at ind {current_ind}")
                        # for last vehicle, add customer to first vehicle
                        if v == self.num_vehicles - 1:
                            chromosome[tsp_path[current_ind]] = 0 

            chromosome = self._reorder_vehicles(chromosome)

            fitness = self._evaluate_fitness(chromosome)
            unfitness = self._evaluate_unfitness(chromosome)
            solution = Solution(chromosome, fitness, unfitness)
            population.append(solution)

        
        return population

    # mutation by swapping the position of one node
    def _mutate(self, solution: Solution) -> Solution:
        # mutate by given chance
        if random.random() < self.mutation_rate:
            mutated_chromosome = np.copy(solution.chromosome)
            # ensure swap performed
            while True:
                index_from = random.randint(0, len(mutated_chromosome)-1)
                index_to = random.randint(0, len(mutated_chromosome)-1)
                if index_from != index_to:
                    mutated_chromosome[index_from] = solution.chromosome[index_to]
                    mutated_chromosome[index_to] = solution.chromosome[index_from]
                    mutated_fitness = self._evaluate_fitness(mutated_chromosome)
                    mutated_unfitness = self._evaluate_unfitness(mutated_chromosome)
                    return Solution(mutated_chromosome, mutated_fitness, mutated_unfitness)
        else:
            return solution

    def _crossover(self, mother: np.array, father: np.array) -> Solution:
        # create child from cossover of father and mother
        cutoff_from = random.randint(0, int(self.dimension / 2) - 1)
        cutoff_to = random.randint(int(self.dimension / 2), self.dimension - 1)
        outer_gene_indices = np.array([val < cutoff_from or val > cutoff_to for val in range(self.dimension)])
        
        child1_chromosomes = np.copy(mother.chromosome)
        child1_chromosomes[outer_gene_indices] = father.chromosome[outer_gene_indices]

        child2_chromosomes = np.copy(father.chromosome)
        child2_chromosomes[outer_gene_indices] = mother.chromosome[outer_gene_indices]

        child1_complete = not self._missing_genes(child1_chromosomes)
        child2_complete = not self._missing_genes(child2_chromosomes)

        if (child1_complete and child2_complete):
            # rank by unfitness, break tie with fitness
            child1_unfitness = self._evaluate_unfitness(child1_chromosomes)
            child2_unfitness = self._evaluate_unfitness(child2_chromosomes)
            if child1_unfitness < child2_unfitness:
                child_fitness = self._evaluate_fitness(child1_chromosomes)
                return Solution(child1_chromosomes, child_fitness, child1_unfitness)
            elif child2_unfitness < child1_unfitness:
                child_fitness = self._evaluate_fitness(child2_chromosomes)
                return Solution(child2_chromosomes, child_fitness, child2_unfitness)
            else:
                child1_fitness = self._evaluate_fitness(child1_chromosomes)
                child2_fitness = self._evaluate_fitness(child2_chromosomes)
                if child1_fitness <= child2_fitness:
                    return Solution(child1_chromosomes, child1_fitness, child1_unfitness)
                else:
                    return Solution(child2_chromosomes, child2_fitness, child2_unfitness) 
        elif child1_complete:
            child_unfitness = self._evaluate_unfitness(child1_chromosomes)
            child_fitness = self._evaluate_fitness(child1_chromosomes)
            return Solution(child1_chromosomes, child_fitness, child_unfitness)
        elif child2_complete:
            child_unfitness = self._evaluate_unfitness(child2_chromosomes)
            child_fitness = self._evaluate_fitness(child2_chromosomes)
            return Solution(child2_chromosomes, child_fitness, child_unfitness)
        else:
            # uniform crossover
            random_indices = random.randint(0,1,(self.dimension,))
            child_chromosomes = np.copy(mother.chromosome)
            child_chromosomes[random_indices] = father.chromosome[random_indices]
            child_unfitness = self._evaluate_unfitness(child_chromosomes)
            child_fitness = self._evaluate_fitness(child_chromosomes)
            return Solution(child_chromosomes, child_fitness, child_unfitness)

    def _mean_vehicle_depot_distance(self, chromosome:np.ndarray) -> np.ndarray:
        """
        Calculate mean distance of cities visited by a vehicle from the depot. 
        """
        mean_distance = np.zeros((self.num_vehicles,2), dtype=np.float32)
        for v in range(self.num_vehicles):
            visited_cities = self.coordinates[chromosome == v]
            mean_distance[v,:] = np.mean(visited_cities, axis=0) - self.depot # correct for depot not at 0,0
        return mean_distance
        
    def _get_polar_angle(self, positions):
        angles = np.arctan2(positions[:,1], positions[:,0])
        angles[angles < 0] += 2*np.pi
        return angles


    def _reorder_vehicles(self, chromosome:np.ndarray):
        """
        sort vehicles by polar angle
        """
        sorted_chromosome = chromosome.copy()
        polar_angles = self._get_polar_angle(self._mean_vehicle_depot_distance(chromosome))
        sort_indices = np.argsort(polar_angles)
        for i in range(len(sort_indices)):
            sorted_chromosome[chromosome == sort_indices[i]] = i

        return sorted_chromosome

    def _adjust_vehicles(self, parent1, parent2):
        """ adjust vehicle numbering before crossover """
        angles1 = self._get_polar_angle(self._mean_vehicle_depot_distance(parent1))
        angles2 = self._get_polar_angle(self._mean_vehicle_depot_distance(parent2))
        if abs(angles1[0] - angles2[1]) < abs(angles1[0] - angles2[0]):
            adjusted_parent1 = parent1.copy()
            adjusted_parent1 += 1
            adjusted_parent1[np.max(adjusted_parent1)] = 0
            return adjusted_parent1, parent2
        elif abs(angles2[0] - angles1[1]) < abs(angles1[0] - angles2[0]):
            adjusted_parent2 = parent2.copy()
            adjusted_parent2 += 1
            adjusted_parent2[np.max(adjusted_parent2)] = 0
            return parent1, adjusted_parent2
        
        return parent1, parent2

    def _missing_genes(self, chromosome:np.ndarray) -> bool:
        vehicles = np.unique(chromosome)
        if not 0 in vehicles:
            return True
        if not self.num_vehicles - 1 in vehicles:
            return True
        if np.any(np.diff(vehicles) > 1):
            return True

        return False
