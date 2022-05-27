import numpy as np
from car_driver_data import *
import haversine as hs
from master_problem import *


def feasible_cars(new_cust, location_list):
    feasible_cars = []
    feasible_cars_keys = []
    for i in range(len(location_list)):
        cust_loc = (float(new_cust.split(',')[0]), float(new_cust.split(',')[1]))
        car_loc = (float(location_list[i][0].split(',')[0]), float(location_list[i][0].split(',')[1]))
        radius = hs.haversine(cust_loc, car_loc)
        if len(location_list[i]) <= 4 and radius <= 4:
            feasible_cars.append(location_list[i])
            feasible_cars_keys.append("car"+str(i))
    return feasible_cars, feasible_cars_keys

# Car 1 location and drop off

def loc2xy(locations):
    x = np.zeros(len(locations))
    y = np.zeros(len(locations))
    for i in range(len(locations)):
        x[i], y[i]  = locations[i].split(',')
    return x, y

def xy2loc(x,y):
    n = len(x)
    X = np.vstack([x.T, y.T])
    locations = [str(X[0][i])+","+str(X[1][i]) for i in range(n)]
    return locations


