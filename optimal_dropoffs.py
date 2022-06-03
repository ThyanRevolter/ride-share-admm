import cvxpy as cp
import ncvx as nc
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import freeze_support
from scipy.sparse import csr_matrix
import distance_matrix_API
import random

def findTripRoute(E,curr_node,n):
    path = []
    for _ in range(n):
        path.append(curr_node)
        curr_node = E[1][curr_node]
    
    return path

def neighbor_func(Z, cur_merit):
    best_merit = np.dot(D.ravel(), Z.ravel())
    idxs = np.argmax(Z, axis=1)
    best_diff = 0
    for a in range(Z.shape[0]):
        """Swap a->b->c->d to a->c->b->d
        """
        b = idxs[a]
        c = idxs[b]
        d = idxs[c]
        diff = D[a, c] + D[b, d] - D[a, b] - D[c, d]
        if diff < best_diff:
            best_diff = diff
            a_candid = a
            b_candid = b
            c_candid = c
            d_candid = d

    if best_diff < 0:
        best_merit += diff
        Z[a_candid, c_candid] = 1
        Z[a_candid, b_candid] = 0

        Z[b_candid, d_candid] = 1
        Z[b_candid, c_candid] = 0

        Z[c_candid, b_candid] = 1
        Z[c_candid, d_candid] = 0
        # print(Z)

    return best_merit, Z



def drop_order(D, X, solver="nc-admm"):
    freeze_support()
    n = D.shape[0]
    if solver == "nc-admm":
        P_nca = nc.Tour(n)
        cost = cp.vec(D).T @ cp.vec(P_nca)
        prob = cp.Problem(cp.Minimize(cost), [])

        tic = time.perf_counter()
        val_nca, result = prob.solve(
            method="NC-ADMM",
            polish_depth=5,
            solver=cp.ECOS,
            show_progress=False,
            neighbor_func=neighbor_func,
            parallel=False,
            restarts=4,
            max_iter=25,
        )
        toc = time.perf_counter()
        print("\n### nc-admm ###")
        print(f"solve time: {toc - tic:.4f} seconds.")
        print("final value:", val_nca)
        S_nca = csr_matrix(P_nca.value)
        E_nca = [[S_nca.indptr[:-1][i] for i in range(n)],[S_nca.indices[i] for i in range(n)]]
        idx_nca = findTripRoute(E_nca,0,n)
        print("final result:") 
        print(S_nca)
        print("nc-admm route:",idx_nca)
        return idx_nca, X[:,idx_nca]
    
    if solver == "relax-round-polish":
        P_rrp = nc.Tour(n)
        cost = cp.vec(D).T @ cp.vec(P_rrp)
        prob = cp.Problem(cp.Minimize(cost), [])

        tic = time.perf_counter()
        val_rrp, result = prob.solve(
            method="relax-round-polish",
            polish_depth=5,
            solver=cp.ECOS,
            neighbor_func=neighbor_func
        )
        toc = time.perf_counter()
        print("\n### relax-round-polish ###")
        print(f"solve time: {toc - tic:.4f} seconds.")
        print("final value:", val_rrp)
        S_rrp = csr_matrix(P_rrp.value)
        E_rrp = [[S_rrp.indptr[:-1][i] for i in range(n)],[S_rrp.indices[i] for i in range(n)]]
        idx_rrp = findTripRoute(E_rrp,0,n)
        print("final result:")
        print(S_rrp)
        print("relax-round-polish route:",idx_rrp)
        return idx_rrp, X[:,idx_rrp]

