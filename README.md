Need to make two changes to packages being used:

1. In ncvx/ncvx/admm_problem.py : changed Line 471 -
    sltn = noncvx_vars[0].z.value.A.copy()
    to
    sltn = np.asarray(noncvx_vars[0].z.value).copy()
    https://github.com/cvxgrp/ncvx/pull/22#issue-1249529623
    
2. Translated the 'z' cone constraint to 'f' in format_and_copy_cone(cone) function
   SCS's core programs in C consider 'f' as the number of linear equality constraints 
   (primal zero, dual free) even though the new version on the website reflects this 
   as 'z'. Turns out they both are the same cone constraints. So, I made this 
   modification so that if we get 'z' it is still processed as 'f'.
   https://github.com/ajfriend/cyscs/pull/4#issue-1249817619
