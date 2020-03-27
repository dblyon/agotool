import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import random
import conftest
# import pandas as pd
# import numpy as np
# from itertools import islice

from scipy import sparse
import pickle

import variables, query


### load data
Protein_2_FunctionEnum_and_Score_table_UPS = variables.TABLES_DICT_SNAKEMAKE["Protein_2_FunctionEnum_and_Score_table"]
ENSP_2_tuple_funcEnum_score_dict = query.get_proteinAN_2_tuple_funcEnum_score_dict(read_from_flat_files=True, fn=Protein_2_FunctionEnum_and_Score_table_UPS)
ENSP_2_tuple_funcEnum_score_dict_keys_list = list(ENSP_2_tuple_funcEnum_score_dict.keys())

CSC_ENSPencoding_2_FuncEnum_UPS_FIN = variables.tables_dict["CSC_ENSPencoding_2_FuncEnum"]
CSC_ENSPencoding_2_FuncEnum = sparse.load_npz(CSC_ENSPencoding_2_FuncEnum_UPS_FIN)

with open(variables.tables_dict["ENSP_2_rowIndex_dict"], "rb") as fh_ENSP_2_rowIndex_dict:
    ENSP_2_rowIndex_dict = pickle.load(fh_ENSP_2_rowIndex_dict)
with open(variables.tables_dict["rowIndex_2_ENSP_dict"], "rb") as fh_rowIndex_2_ENSP_dict:
    rowIndex_2_ENSP_dict = pickle.load(fh_rowIndex_2_ENSP_dict)


### funtions, helpers
def slice_ScoresMatrix_for_given_ENSP(protein_AN_set, ENSP_2_rowIndex_dict, matrix):
    """
    produces 2D array
    number of rows corresponds to number of proteins if in ENSP_2_Score_dict
    number of columns corresponds to number of funcEnum of KS_etype; encoded as funcEnumIndex range(0, max(cond_KS_etypes)+1)
    """
    list_of_rowIndices = []
    for ENSP in protein_AN_set:
        try:
            rowIndex = ENSP_2_rowIndex_dict[ENSP]
        except KeyError:
            continue
        list_of_rowIndices.append(rowIndex)
    return matrix[list_of_rowIndices], list_of_rowIndices

def get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_get, ENSP_2_rowIndex_dict=ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum=CSC_ENSPencoding_2_FuncEnum):
    # grab data for specific UniProtID
    fg_scores_matrix, list_of_rowIndices_fg = slice_ScoresMatrix_for_given_ENSP([UniProtID_2_get], ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    funcEnum_list, score_list = [], []
    m = fg_scores_matrix
    for i in range(len(m.indptr[:-1])):  # get column values
        index_row_start = m.indptr[i]
        index_row_stop = m.indptr[i + 1]
        if index_row_start == index_row_stop:
            continue
        # funcEnum_2_score_from_matrix.append([i, m.data[index_row_start:index_row_stop][0]])
        funcEnum_list.append(i)
        score_list.append(m.data[index_row_start:index_row_stop][0])
    return funcEnum_list, score_list


### tests
# compare sparse matrix loaded from binary dump to dictionary-array loaded from flat file
def test_sparse_vs_flatfile_ex_1():
    """
    compare sparse matrix loaded from binary dump to dictionary-array loaded from flat file
    specific example (first on Lars downloads 'Protein_2_Function_and_Score_DOID_BTO_GOCC_STS.txt.gz'
    """
    UniProtID_2_test = "NAC1_ARATH"
    funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
    assert list(funcEnum_arr) == funcEnum_list_from_sparse
    assert list(score_arr) == score_list_from_sparse

def test_sparse_vs_flatfile_ex_2():
    """
    random UniProtID
    """
    UniProtID_2_test = conftest.get_random_human_ENSP(num_ENSPs=1, UniProt_ID=True)[0]
    funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    try:
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
    except KeyError:
        funcEnum_arr, score_arr = [], []
    assert list(funcEnum_arr) == funcEnum_list_from_sparse
    assert list(score_arr) == score_list_from_sparse

def test_sparse_vs_flatfile_ex_3():
    """
    20 random UniProtID that have TM scores
    """
    for i in range(20):
        UniProtID_2_test = random.choice(ENSP_2_tuple_funcEnum_score_dict_keys_list)
        funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
        assert list(funcEnum_arr) == funcEnum_list_from_sparse
        assert list(score_arr) == score_list_from_sparse

def test_Taxid_
