"""Define some fixtures to use in the project."""

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pandas as pd
import numpy as np
import random

import query, userinput

@pytest.fixture(scope='session')
def pqo():
    """
    get pqo (Persistent Query Object)
    """
    return query.PersistentQueryObject()

@pytest.fixture(scope='session')
def pqo_STRING():
    """
    get pqo (Persistent Query Object)
    """
    return query.PersistentQueryObject_STRING()

@pytest.fixture(scope='session')
def get_something():
    """A session scope fixture."""
    return "Bubu was here"


taxid_list = [9606, 10090, 4932, 511145,
              1038869, 32051]
taxname_list = ["Homo sapiens", "Mus musculus", "Saccharomyces cerevisiae", "Escherichia coli str. K-12 substr. MG1655",
                "Paraburkholderia mimosarum",
                "Synechococcus sp. WH 7803"]

@pytest.fixture(params=taxid_list, ids=taxname_list, scope="session")
def TaxIDs(request):
    return request.param

@pytest.fixture(scope="session")
def random_foreground_background(TaxIDs):
    taxid = TaxIDs
    background = query.get_proteins_of_taxid(taxid)
    foreground = random.sample(background, 200)
    return foreground, background, taxid

@pytest.fixture(scope="session")
def ui_genome(random_foreground_background):
    foreground, background = random_foreground_background
    ui = userinput.U

