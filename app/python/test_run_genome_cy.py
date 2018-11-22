import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pytest
import requests
import ast

import variables



def test_filter_parents():
    """
    if filter parents is False there should be equal or more results than if the filter is True
    :return:
    """
    FDR_cutoff = 0.05
    filter_foreground_count_one = True
    filter_parents = False
    res_filter_parents_false = None

    FDR_cutoff = 0.05
    filter_foreground_count_one = True
    filter_parents = True
    res_filter_parents_True = None

    assert res_filter_parents_false.shape[0] >= res_filter_parents_true.shape[0]






