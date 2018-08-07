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

### STRING examples
# Example #1 Protein name: trpA; Organism: Escherichia coli K12_MG1655
ENSPs_1 = ['511145.b1260', '511145.b1261', '511145.b1262', '511145.b1263', '511145.b1264', '511145.b1812', '511145.b2551', '511145.b3117', '511145.b3360', '511145.b3772', '511145.b4388']
taxid_1 = 511145
# Example #2 Protein name: CDC15; Organism: Saccharomyces cerevisiae
ENSPs_2 = ['4932.YAR019C', '4932.YFR028C', '4932.YGR092W', '4932.YHR152W', '4932.YIL106W', '4932.YJL076W', '4932.YLR079W', '4932.YML064C', '4932.YMR055C', '4932.YOR373W', '4932.YPR119W']
taxid_2 = 4932
# Example #3 Protein name: smoothened; Organism: Mus musculus
ENSPs_3 = ['10090.ENSMUSP00000001812', '10090.ENSMUSP00000002708', '10090.ENSMUSP00000021921', '10090.ENSMUSP00000025791', '10090.ENSMUSP00000026474', '10090.ENSMUSP00000030443', '10090.ENSMUSP00000054837', '10090.ENSMUSP00000084430', '10090.ENSMUSP00000099623', '10090.ENSMUSP00000106137', '10090.ENSMUSP00000107498']
taxid_3 = 10090