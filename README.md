# An Energy-Efficient Ride-Sharing Algorithm Using Distributed Convex Optimization
### Authors: [Shashvat Jayakrishnan](www.github.com/ShashvatJK) and [Adhithyan Sakthivelu](www.github.com/ThyanRevolter)
#### This is our project as part of the [EE 364B - Convex Optimization II](https://web.stanford.edu/class/ee364b/) class at Stanford University - Spring 2022.

Packages that need to be installed before running our project:
1. [CVXPY](https://github.com/cvxpy/cvxpy)
2. [NCVX](https://github.com/cvxgrp/ncvx)
3. [SCSPROX](https://github.com/bettbra/scsprox)
4. [CYSCS](https://github.com/ajfriend/cyscs)

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
   
Finally, let's run our Ride-sharing Algorithm!
