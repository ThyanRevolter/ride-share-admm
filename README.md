# An Energy-Efficient Ride-Sharing Algorithm Using Distributed Convex Optimization
### Authors: [Shashvat Jayakrishnan](www.github.com/ShashvatJK) (MS in EE '23) and [Adhithyan Sakthivelu](www.github.com/ThyanRevolter) (MS in CEE (AE) '23)
#### This is our project as part of the [EE 364B - Convex Optimization II](https://web.stanford.edu/class/ee364b/) class at Stanford University - Spring 2022.  

#### [Poster](https://office365stanford-my.sharepoint.com/:p:/g/personal/adhiths_stanford_edu/EdDQXM0uWsdCp8Bkde5YV_oBCUFgS_J8s4KaIo_UY5x0cw?e=zpqAZz) | [Paper](https://office365stanford-my.sharepoint.com/:p:/g/personal/adhiths_stanford_edu/EdDQXM0uWsdCp8Bkde5YV_oBCUFgS_J8s4KaIo_UY5x0cw?e=zpqAZz)
---

### Preliminaries

---

Packages that need to be installed before running our project:
- [CVXPY](https://github.com/cvxpy/cvxpy)
- [NCVX](https://github.com/cvxgrp/ncvx)
- [SCSPROX](https://github.com/bettbra/scsprox)
- [CYSCS](https://github.com/ajfriend/cyscs)

Next, before running this code,  you need to make two changes to package files being used: 

(Note: These are pull requests submitted by us to the respective repositories to correct errors that we found in their code files that prevented a smooth running of the Travelling Salesperson Problem (TSP) implementation)

1. In [ncvx/admm_problem.py](https://github.com/cvxgrp/ncvx/blob/master/ncvx/admm_problem.py) : changed Line 471 -
    sltn = noncvx_vars[0].z.value.A.copy()
    to
    sltn = np.asarray(noncvx_vars[0].z.value).copy()
    https://github.com/cvxgrp/ncvx/pull/22#issue-1249529623
    
2. Translated the 'z' cone constraint to 'f' in [cyscs/_util.py](https://github.com/ajfriend/cyscs/blob/master/cyscs/_util.py) 's format_and_copy_cone(cone) function
   SCS's core programs in C consider 'f' as the number of linear equality constraints 
   (primal zero, dual free) even though the new version on the website reflects this 
   as 'z'. Turns out they both are the same cone constraints. So, I made this 
   modification so that if we get 'z' it is still processed as 'f'.
   https://github.com/ajfriend/cyscs/pull/4#issue-1249817619  
     
---

### Let's Begin!

---

Finally, we can run our Ride-sharing Algorithm!

Clone this repository and run the `problem_instance_1.py` file. 

- You should see a random passenger location being generated along with an existing cluster of vehicles driving nearby.
- The algorithm filters our prospective pick-up vehicles by performing local feasibility checks based on a energy-efficency based variation of TSP.
- Once the feasible vehicles are found, the final pick-up vehicle is decided by solving a master optimization (MILP) which minimizes the energy required to perform the pick-up.
- While the rider gets matched with the best vehicle, all the vehicles follow the optimal drop-off order obtained from the TSP to drop-off the passengers.
- The algorithm is centered around energy-efficiency in the pick-up and drop-off phase of ride-sharing trips while incorporating decentralized decision making.
