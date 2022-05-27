import cvxpy as cp
import ncvx as nc
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import freeze_support
import cyscs as scs
from scipy.sparse import csr_matrix
import distance_matrix_API
# This example is described in Section 6.4 of the NCVX paper.

# Traveling salesman problem.
#np.random.seed(1)
plt.close()
# n=5

# # Get locations.
# x = np.random.uniform(-1, 1, size=(n, 1))
# y = np.random.uniform(-1, 1, size=(n, 1))
# X = np.vstack([x.T, y.T])

# # Make distance matrix.
# D = np.zeros((n, n))
# for i in range(n):
#     for j in range(n):
#         D[i, j] = cp.norm(X[:, i] - X[:, j]).value

x = np.array([37.42004765994148, 37.42608322860995, 37.43232913771922, 37.443228634712966, 37.41794560488438])
y = np.array([-122.20270570225145, -122.1588178069173, -122.18699513497546, -122.15464077643587, -122.126188456268])
n = len(x)
X = np.vstack([x.T, y.T])
locations = [str(X[0][i])+","+str(X[1][i]) for i in range(n)]
# p1 = "37.42608322860995,-122.1588178069173"

# # location 2 Oak creek
# p2 = "37.43232913771922,-122.18699513497546"

# # location 3 HP garage 
# p3 = "37.443228634712966,-122.15464077643587"

# # location 4 Goodwill
# p4 = "37.41794560488438,-122.126188456268"

# # location of car SLAC
# c = "37.42004765994148,-122.20270570225145"

# locations = [c, p1, p2, p3, p4]

T, D = distance_matrix_API.createDistanceMatrix(locations)
D[:,0] = 0
print(D)
print(T)

def findTripRoute(E,curr_node,n):
    path = []
    for i in range(n):
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


def run():
    # Approximate solution with nc-admm
    P_nca = nc.Tour(n)
    cost = cp.vec(D).T @ cp.vec(P_nca)
    prob = cp.Problem(cp.Minimize(cost), [])

    tic = time.perf_counter()
    val, result = prob.solve(
        method="NC-ADMM",
        polish_depth=5,
        solver=cp.SCS,
        show_progress=False,
        neighbor_func=neighbor_func,
        parallel=True,
        restarts=4,
        max_iter=25,
    )
    toc = time.perf_counter()
    print("\n### nc-admm ###")
    print(f"solve time: {toc - tic:.4f} seconds.")
    print("final value:", val)
    S_nca = csr_matrix(P_nca.value)
    E_nca = [[S_nca.indptr[:-1][i] for i in range(n)],[S_nca.indices[i] for i in range(n)]]
    idx_nca = findTripRoute(E_nca,0,n)
    print("final result:") 
    print(S_nca)
    print("nc-admm route:",idx_nca)

    # Approximate solution with relax-round-polish
    P_rrp = nc.Tour(n)
    cost = cp.vec(D).T @ cp.vec(P_rrp)
    prob = cp.Problem(cp.Minimize(cost), [])

    tic = time.perf_counter()
    val, result = prob.solve(
        method="relax-round-polish",
        polish_depth=5,
        solver=cp.SCS,
        neighbor_func=neighbor_func
    )
    toc = time.perf_counter()
    print("\n### relax-round-polish ###")
    print(f"solve time: {toc - tic:.4f} seconds.")
    print("final value:", val)
    S_rrp = csr_matrix(P_rrp.value)
    E_rrp = [[S_rrp.indptr[:-1][i] for i in range(n)],[S_rrp.indices[i] for i in range(n)]]
    idx_rrp = findTripRoute(E_rrp,0,n)
    print("final result:")
    print(S_rrp)
    print("relax-round-polish route:",idx_rrp)

    # # Plotting
    # ordered_nca = (X @ P_nca.T).value
    # ordered_rrp = (X @ P_rrp.T).value
    # print(X)

    for i in range(n-1):
        if i == n-2:
            plt.plot(
                [X[0, idx_nca[i]], X[0, idx_nca[i+1]]],
                [X[1, idx_nca[i]], X[1, idx_nca[i+1]]],
                color="red",
                marker="o",
                markerfacecolor="black",
                markeredgecolor="black",
                linestyle='-.',
                label="nc-admm"
            )
            plt.legend()
        else:
            plt.plot(
                [X[0, idx_nca[i]], X[0, idx_nca[i+1]]],
                [X[1, idx_nca[i]], X[1, idx_nca[i+1]]],
                color="red",
                marker="o",
                markerfacecolor="black",
                markeredgecolor="black",
                linestyle='-.'
            )
        
    for j in range(n-1):
        if j == n-2:
            plt.plot(
                [X[0, idx_rrp[j]], X[0, idx_rrp[j+1]]],
                [X[1, idx_rrp[j]], X[1, idx_rrp[j+1]]],
                color="blue",
                marker="o",
                markerfacecolor="black",
                markeredgecolor="black",
                linestyle=':',
                label="relax-round-polish"
            )
            plt.legend()
           
        else:
            plt.plot(
                [X[0, idx_rrp[j]], X[0, idx_rrp[j+1]]],
                [X[1, idx_rrp[j]], X[1, idx_rrp[j+1]]],
                color="blue",
                marker="o",
                markerfacecolor="black",
                markeredgecolor="black",
                linestyle=':'
            )
        plt.text(X[0, j],X[1, j]-0.005,"Loc "+str(j),ha='center',va='bottom')
        #plt.annotate("DropLoc "+str(j),(X[0, j],X[1, j]),xytext=(0,10),ha='center')
        
    plt.text(X[0, n-1],X[1, n-1]-0.005,"Loc "+str(n-1),ha='center',va='bottom')
    #plt.annotate("DropLoc "+str(n-1),(X[0, n-1],X[1, n-1]),xytext=(0,10),ha='center')
    plt.show()


if __name__ == "__main__":
    freeze_support()
    run()