import cvxpy as cp
import ncvx as nc
import numpy
import time
from multiprocessing import freeze_support

# Problem data
m = 30; n = 20; k = 6
numpy.random.seed(1)
A = numpy.random.randn(m, n)
b = numpy.random.randn(m, 1)

def run():
    # NC-ADMM heuristic.
    x = nc.Card(n, k, 1)
    objective = cp.sum_squares(A @ x - b)
    prob = cp.Problem(cp.Minimize(objective), [])
    prob.solve(method="relax-round-polish") #"NC-ADMM"
    print(f"Objective = {objective.value}")
    print(f"x = \n{x.value}")

if __name__ == "__main__":
    freeze_support()
    run()