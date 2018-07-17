import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pandas as pd
import numpy as np
from itertools import zip_longest
import pytest

import variables

# def test_backtracking(pqo):
#     an = "P31946"
#     #!!! ToDo change to ENSP
#     # this test does not make sense for denormalized STRING version of DB having
#     functions_set_no_backtracking = pqo.get_association_dict([an], "all_GO", "basic", backtracking=False)[an]
#     functions_set_with_backtracking = pqo.get_association_dict([an], "all_GO", "basic", backtracking=True)[an]


### performance testing with and without backtracking
# In [5]: len(ans)
# Out[5]: 201
#
# In [6]: %timeit pqo.get_association_dict(ans, "all_GO", "basic", backtracking=False)
# 17 ms ± 952 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
#
# In [7]: %timeit pqo.get_association_dict(ans, "all_GO", "basic", backtracking=True)
# 32.3 ms ± 1.13 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
#
# In [9]: len(ans2)
# Out[9]: 2001
#
# In [10]: %timeit pqo.get_association_dict(ans2, "all_GO", "basic", backtracking=True)
# 169 ms ± 11.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
#
# In [11]: %timeit pqo.get_association_dict(ans2, "all_GO", "basic", backtracking=False)
# 65 ms ± 1.19 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)