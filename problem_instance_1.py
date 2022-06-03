from random import sample
from typing import Dict
import numpy as np
from car_driver_data import *
from master_problem import *
from optimal_rollouts import *
from distance_matrix_API import *
from optimal_dropoffs import Drop

new_cust = "37.429070511839086,-122.16979819313977"
location_list =  generate_cars(20)
feasible_cars_list, feasible_cars_keys = feasible_cars(new_cust, location_list)
energy = get_energy(new_cust, feasible_cars_list)
y, min_energy = solve_master(feasible_cars_list, energy)
print("Assigned Car Id is "+ feasible_cars_keys[np.argmax(y)])
print("Assigned Car location is "+ feasible_cars_list[np.argmax(y)][0])


energy_matrix_dict = dict()
car_location = []
for i in range(len(feasible_cars_list)):
    car_location.append(feasible_cars_list[i][0])
    feasible_cars_list[i][0] = new_cust
    T_car, D_car = createDistanceMatrix(feasible_cars_list[i])
    energy_matrix_dict[feasible_cars_keys[i]] = get_energy_matrix(T_car, D_car)

sample_energy = []
for energy_matrix in energy_matrix_dict:
    # print(energy_matrix)
    # print(energy_matrix_dict[energy_matrix].shape)
    # print(energy_matrix_dict[energy_matrix])
    sample_energy = energy_matrix_dict[energy_matrix]
    drop = Drop(sample_energy)
    drop.drop_order(solver="nc-admm")
    drop.drop_order(solver="relax-round-polish")

