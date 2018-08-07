import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pandas as pd
import numpy as np
from itertools import zip_longest
import pytest
import random
from ast import literal_eval


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

def test_ENSP_overlap_of_DB():
    """
    - ENSPs of taxid_2_protein_table are the superset of ENSPs of protein_2_function_table

    foreground with functional association also has to be in the precomputed background
    TaxID_2_Protein_table_STRING: ENSPs expected to be the superset of Protein_2_Function_table_STRING
    Protein_2_Function_table_STRING
    Function_2_ENSP_table_STRING
    """
    for taxid in query.get_taxids():
        ensp_taxid_2_protein = set(query.get_proteins_of_taxid(taxid))
        ensp_protein_2_function = {ele[0] for ele in query.get_results_of_statement("SELECT protein_2_function.an FROM protein_2_function WHERE protein_2_function.an ~ '^{}\.'".format(taxid))}
        # ensp_function_2_ensp = None
        len_ensp_taxid_2_protein = len(ensp_taxid_2_protein)
        len_ensp_protein_2_function = len(ensp_protein_2_function)
        assert len_ensp_taxid_2_protein >= len_ensp_protein_2_function
        assert len(ensp_taxid_2_protein.intersection(ensp_protein_2_function)) == len_ensp_protein_2_function
        assert len(ensp_taxid_2_protein.union(ensp_protein_2_function)) == len_ensp_taxid_2_protein

def test_(pqo_STRING):
    """
    all functional associations of given taxid and ensp from protein_2_function need be present in function_2_ensp
    """
    # generator to retrieve row by row from table is not supported by psycopg2 module that accesses PostgreSQL for python
    # therefore reading table used for DB generation 'copy from file'
    taxid_2_etype_2_association_2_count_dict_background = pqo_STRING.taxid_2_etype_2_association_2_count_dict_background
    fn = variables.TABLES_DIR("Protein_2_Function_table_STRING.txt")
    with open(fn, "r") as fh:
        for line in fh:
            ENSP, association_array, etype = line.strip().split()
            taxid = int(ENSP[:ENSP.find(".")])
            etype = int(etype)
            association_array = literal_eval(association_array)
            # assert len(association_array) ==
            association_2_count_dict = taxid_2_etype_2_association_2_count_dict_background[taxid][etype]


