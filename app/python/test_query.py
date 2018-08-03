import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pandas as pd
import numpy as np
from itertools import zip_longest
import pytest
import random

import variables, ratio, query, run



def test_precomputed_associations_counts(pqo_STRING, TaxIDs):
    taxid = TaxIDs
    ENSPs_proteome = query.get_proteins_of_taxid(taxid)
    # A
    etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, etype_2_background_n = query.get_association_2_count_ANs_background_split_by_entity(taxid)
    etype_2_association_dict = pqo_STRING.get_association_dict_split_by_category(set(ENSPs_proteome))
    for etype in variables.entity_types_with_data_in_functions_table:
        # B
        association_2_count_dict, association_2_ANs_dict, ans_counter = ratio.count_terms_v3(set(ENSPs_proteome), etype_2_association_dict[etype])
        assert association_2_count_dict == etype_2_association_2_count_dict_background[etype]
        assert association_2_ANs_dict == etype_2_association_2_ANs_dict_background[etype]

def test_foreground_is_subset_of_background(pqo_STRING, random_foreground_background):
    foreground, background, taxid = random_foreground_background
    # ENSPs_proteome = query.get_proteins_of_taxid(taxid)
    # ENSPs_foreground = random.sample(ENSPs_proteome, 200)
    etype_2_association_dict_background = pqo_STRING.get_association_dict_split_by_category(background)
    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    for etype in variables.entity_types_with_data_in_functions_table:
        assert etype_2_association_dict_foreground[etype].items() <= etype_2_association_dict_background[etype].items()

def test_association_2_count_dict(pqo_STRING, random_foreground_background):
    foreground, background, taxid = random_foreground_background
    etype_2_association_dict_background = pqo_STRING.get_association_dict_split_by_category(background)
    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    for etype in variables.entity_types_with_data_in_functions_table:
        association_2_count_dict_background, association_2_ANs_dict_background, ans_counter_background = ratio.count_terms_v3(set(background), etype_2_association_dict_background[etype])
        association_2_count_dict_foreground, association_2_ANs_dict_foreground, ans_counter_foreground = ratio.count_terms_v3(set(foreground), etype_2_association_dict_foreground[etype])

        dag = run.pick_dag_from_entity_type_and_basic_or_slim(etype, "basic", pqo_STRING)
        assoc_dict_foreground = etype_2_association_dict_foreground[etype]
        association_2_count_dict_foreground_v2, association_2_ANs_dict_foreground_v2, foreground_n_v2 = ratio.count_terms_manager(set(foreground), assoc_dict_foreground, dag, etype)

        assoc_dict_background = etype_2_association_dict_background[etype]
        association_2_count_dict_background_v2, association_2_ANs_dict_background_v2, background_n_v2 = ratio.count_terms_manager(set(background), assoc_dict_background, dag, etype)

        for association, foreground_count in association_2_count_dict_foreground.items():
            assert association in association_2_count_dict_background
            assert association in association_2_ANs_dict_background

            assert association in association_2_count_dict_foreground_v2
            assert association in association_2_ANs_dict_foreground_v2

            assert association in association_2_count_dict_background_v2
            assert association in association_2_ANs_dict_background_v2



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