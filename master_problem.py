import cvxpy as cp
from kiwisolver import Solver
import numpy as np
from distance_matrix_API import *

def get_energy(new_cust, feasible_locations_list):
    a, b, c, k = 2, 1, 4, 20
    n_feas = len(feasible_locations_list)
    D_feas ,T_feas = np.zeros(n_feas), np.zeros(n_feas)
    for i in range(n_feas):
        T_feas[i], D_feas[i] = get_distance(new_cust,feasible_locations_list[i][0])
    avg_speed = np.divide(D_feas, T_feas)
    energy = np.multiply((np.square(avg_speed)*a + avg_speed*b + np.ones(n_feas)*c), D_feas) + np.ones(n_feas)*k
    energy = np.where(np.isnan(energy), 0, energy)
    return energy

def get_energy_matrix(T_matrix, D_matrix):
    a, b, c, k = .02, .1, .4, 20
    n = D_matrix.shape[0]
    avg_speed = np.divide(D_matrix, T_matrix)
    energy = np.multiply((np.square(avg_speed)*a + avg_speed*b + np.ones(n)*c), D_matrix) + np.ones(n)*k
    energy = np.where(np.isnan(energy), 0, energy)
    return energy

def solve_master(feasible_locations_list, energy):
    n = len(feasible_locations_list)
    y = cp.Variable(n, integer=True)
    constr = [cp.sum(y) == 1]
    constr += [y[i] >=0 for i in range(n)]
    objective = cp.Problem(cp.Minimize(energy.T@y), constr)
    objective.solve(solver=cp.GLPK_MI)
    return y.value, objective.value
