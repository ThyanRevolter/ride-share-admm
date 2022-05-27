import numpy as np
from car_driver_data import *
from master_problem import *
from optimal_rollouts import *

new_cust = "37.429070511839086,-122.16979819313977"
location_list =  generate_cars(20)
cars_list, feasible_cars_keys = feasible_cars(new_cust, location_list)
energy = get_energy(new_cust, cars_list)
y, min_energy = solve_master(cars_list, energy)
print("Assigned Car Id is "+feasible_cars_keys[np.argmax(y)])
print("Assigned Car location is "+cars_list[np.argmax(y)][0])

