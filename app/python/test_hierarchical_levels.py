import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pytest
# import requests
# import ast
import variables, ratio, userinput, run # query
import create_SQL_tables_snakemake as cst
# from collections import defaultdict



@pytest.fixture()
def child_2_direct_parents_and_term_2_level_dict_interpro():
    fn = os.path.join(variables.DOWNLOADS_DIR, "interpro_parent_2_child_tree.txt")
    child_2_parent_dict, term_2_level_dict = cst.get_child_2_direct_parents_and_term_2_level_dict_interpro(fn)
    return child_2_parent_dict, term_2_level_dict

def test_RCTM_hierarchies(child_2_direct_parents_and_term_2_level_dict_interpro):
    child_2_parent_dict, term_2_level_dict = child_2_direct_parents_and_term_2_level_dict_interpro

    term = "IPR000276"
    level = 1
    parent = set()
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000018"
    level = 2
    parent = {"IPR000276"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000025"
    level = 2
    parent = {"IPR000276"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR002280"
    level = 3
    parent = {"IPR000025"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR027459"
    level = 3
    parent = {"IPR000025"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR002278"
    level = 4
    parent = {"IPR027459"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000142"
    level = 2
    parent = {"IPR000276"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000204"
    level = 2
    parent = {"IPR000276"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000248"
    level = 2
    parent = {"IPR000276"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR000174"
    level = 3
    parent = {"IPR000355"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

    term = "IPR001053"
    level = 3
    parent = {"IPR000355"}
    assert term_2_level_dict[term] == level
    assert child_2_parent_dict[term] == parent

