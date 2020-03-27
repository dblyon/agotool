import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
import pandas as pd
import pytest, random
import numpy as np
from itertools import islice
from io import StringIO
import requests
import conftest

import variables, query

url_local = r"http://127.0.0.1:5000/api"



def test_random_contiguous_input_yields_results():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "genome", "taxid": 9606})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0

### tests for enrichment_method genome
def test_FG_count_not_larger_than_FG_n():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=100, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["FG_count"] <= df["FG_n"]
    assert cond.all()

def test_FG_count_not_larger_than_BG_count():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df = pd.read_csv(StringIO(response.text), sep='\t')
    assert df.shape[0] > 0
    cond = df["FG_count"] <= df["BG_count"]
    assert cond.all()

# genome and compare_samples should yield the same results if given the same input
def test_genome_same_as_compare_samples():
    fg_string = conftest.get_random_human_ENSP(num_ENSPs=200, UniProt_ID=True, contiguous=True, joined_for_web=True)
    response = requests.post(url_local, params={"output_format": "tsv", "enrichment_method": "genome", "taxid": 9606},
        data={"foreground": fg_string})
    df_genome = pd.read_csv(StringIO(response.text), sep='\t')

    bg_string = "%0d".join(conftest.UniProt_IDs_human_list)
    response = requests.post(url_local, params={"output_format": "tsv", "foreground": fg_string, "enrichment_method": "compare_samples", "taxid": 9606}, data={"foreground": fg_string, "background": bg_string})
    df_compare_samples = pd.read_csv(StringIO(response.text), sep='\t')

    # assert BG_n and BG_count between
    cond_BG_count = df_compare_samples["BG_count"] == df_genome["BG_count"]
    assert cond_BG_count.all()

    cond_BG_n = df_compare_samples["BG_n"] == df_genome["BG_n"]
    assert cond_BG_n.all()


    # assert df.shape[0] > 0
    # cond = df["FG_count"] <= df["BG_count"]
    # assert cond.all()

# check expected terms for specific input (e.g. reviewer query on Haemoglobin)
def test_expected_terms_in_output():
    pytest.fail()

# check that ENSP and UniProtIDs give same results
def test_ENSP_vs_UniProtID():
    pytest.fail()


# examples from webpage need to work
def test_web_example_1():
    pytest.fail()

def test_web_example_2():
    pytest.fail()

def test_web_example_3():
    pytest.fail()

