# http://vrp.galgos.inf.puc-rio.br/index.php/en/plotted-instances?data=A-n32-k5
from typing import Tuple

import glob
import os
import re
import numpy as np
import pandas as pd

import scipy
import scipy.spatial as sp
from src.config import config


class VRPLoader():
    def __init__(self, problem_name):
        self.DATA_PATH = config.DATA_PATH / 'vrp'
        self.problem_name = problem_name

    def load_problem_instance(self) -> np.ndarray:
        path = self.DATA_PATH / self.problem_name
        if not os.path.exists(f"{path}.vrp"):
            raise ValueError(f"Invalid choice {self.problem_name}. Should be one of {[os.path.basename(x).split('.')[0] for x in glob.glob(f'{self.DATA_PATH}/*.vrp')]}")

        coordinates, demand, capacity = self._load_values_by_line(f"{path}.vrp")
        best_solution, cost = self._load_solution(f"{path}.sol")
        
        distance = sp.distance.cdist(coordinates, coordinates, 'euclidean')
            
        assert distance.diagonal().sum() == 0.0  # weights to same node have to be 0
        assert distance.shape[0] == distance.shape[1]  # symmetric matrix
        return coordinates, distance, demand, capacity, best_solution, cost
       

    def _load_solution(self, path):
        routes = []
        with open(path, 'r') as file:
            for line in file.readlines():
                if line.startswith("Cost"):
                    return routes, float(line.split()[1])

                routes.append(np.array(line.split(":")[1].strip().split()))
        
        raise ValueError("Invalid solution format. Did not find the total cost")

    def _load_values_by_line(self, path) -> Tuple[np.array, np.array]:
        coordinates = []
        demand = []
        capacity = 0
        mode = None
        with open(path, 'r') as file:
            for line in file.readlines():
                line = line.strip()

                # skip comment section
                if mode is None:
                    if line.startswith("CAPACITY"):
                       capacity = int(line.split(":")[1].strip())
                       continue
                    if line == "NODE_COORD_SECTION":
                        mode = "COORD"
                        continue

                # read in coordinates
                if mode == "COORD":
                    if line == "DEMAND_SECTION":
                        mode = "DEMAND"
                        continue

                    if len(line) > 0:
                        coord = line.split()
                        coordinates.append([int(coord[1]), int(coord[2])])
                
                # read in demand
                if mode == "DEMAND":
                    if line == "DEPOT_SECTION":
                        break
                    if len(line) > 0:
                        dem = line.split()
                        demand.append(int(dem[1]))

        return np.array(coordinates), np.array(demand), capacity