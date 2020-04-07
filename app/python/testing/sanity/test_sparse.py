import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))) # to get from API to python directory
import random
import conftest
import pandas as pd
import numpy as np
# from itertools import islice

import pytest
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
# source: Protein_2_FunctionEnum_and_Score_table_UPS_FIN
#  --> SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
#  --> Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN and Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.pickle
# Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN --> test exists
# SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN --> test exists
# SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle --> test exists
# Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle --> test exists


# compare sparse matrix loaded from binary dump to dictionary-array loaded from flat file
def test_Protein_2_FunctionEnum_and_Score_sparse_vs_flatfile_ex_1():
    """
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
    compare sparse matrix loaded from binary dump to dictionary-array loaded from flat file
    specific example (first line in Lars downloads 'Protein_2_Function_and_Score_DOID_BTO_GOCC_STS.txt.gz'
    """
    UniProtID_2_test = "NAC1_ARATH"
    funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
    assert list(funcEnum_arr) == funcEnum_list_from_sparse
    assert list(score_arr) == score_list_from_sparse

def test_Protein_2_FunctionEnum_and_Score_sparse_vs_flatfile_ex_2():
    """
    random UniProtID
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
    """
    UniProtID_2_test = conftest.get_random_human_ENSP(num_ENSPs=1, UniProt_ID=True)[0]
    funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    try:
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
    except KeyError:
        funcEnum_arr, score_arr = [], []
    assert list(funcEnum_arr) == funcEnum_list_from_sparse
    assert list(score_arr) == score_list_from_sparse

def test_Protein_2_FunctionEnum_and_Score_sparse_vs_flatfile_ex_3():
    """
    20 random UniProtID that have TM scores
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
    """
    for i in range(20):
        UniProtID_2_test = random.choice(ENSP_2_tuple_funcEnum_score_dict_keys_list)
        funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
        assert list(funcEnum_arr) == funcEnum_list_from_sparse
        assert list(score_arr) == score_list_from_sparse

def test_Protein_2_FunctionEnum_and_Score_sparse_vs_flatfile_ex_4_multiple_entries():
    """
    Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
    """
    UniProtID_2_test_list = random.sample(ENSP_2_tuple_funcEnum_score_dict_keys_list, 100)
    fg_scores_matrix, list_of_rowIndices_fg = slice_ScoresMatrix_for_given_ENSP(UniProtID_2_test_list, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)

    funcEnum_2_scores_dict = {}
    for UniProtID in UniProtID_2_test_list:
        funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID]
        for funcEnum, score in zip(funcEnum_arr, score_arr):
            if funcEnum not in funcEnum_2_scores_dict:
                funcEnum_2_scores_dict[funcEnum] = [score]
            else:
                funcEnum_2_scores_dict[funcEnum].append(score)

    m = fg_scores_matrix
    for i in range(len(m.indptr[:-1])):  # get column values
        index_row_start = m.indptr[i]
        index_row_stop = m.indptr[i + 1]
        if index_row_start == index_row_stop:
            continue
        funcEnum = i
        scores_list_sparse = sorted(m.data[index_row_start:index_row_stop])
        scores_list_ff = sorted(funcEnum_2_scores_dict[funcEnum])
        assert len(scores_list_sparse) == len(scores_list_ff)
        assert scores_list_sparse == scores_list_ff

# def test_Protein_2_FunctionEnum_and_Score_sparse_vs_flatfile_ex_debug_all_human_prots():
#     """
#     very lenghty test
#     test all human proteins, since test_Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle_vs_sparse fails
#     w
#     Protein_2_FunctionEnum_and_Score_table_UPS_FIN vs SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN
#     """
#     for UniProtID_2_test in ENSP_2_tuple_funcEnum_score_dict_keys_list[::-1]:
#         funcEnum_list_from_sparse, score_list_from_sparse = get_funcEnum_and_score_from_sparse_matrix(UniProtID_2_test, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
#         funcEnum_arr, score_arr = ENSP_2_tuple_funcEnum_score_dict[UniProtID_2_test]
#         assert list(funcEnum_arr) == funcEnum_list_from_sparse
#         assert list(score_arr) == score_list_from_sparse



def test_Taxid_2_FunctionEnum_2_Scores_flatfile_vs_pickle():
    """
    passed
    hopefully solved, Snakemake rule was commented out and therefore Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle not updated
    Taxid_2_FunctionEnum_2_Scores_dict vs Taxid_2_FunctionEnum_2_Scores_table
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN = os.path.join(variables.TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt")
    testing r_Pickle_Taxid_2_FunctionEnum_2_Scores_dict
    """
    Taxid_2_FunctionEnum_2_Scores_dict_ff = query.get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=True, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=False)
    Taxid_2_FunctionEnum_2_Scores_dict_p = query.get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=False, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=True)
    assert sorted(Taxid_2_FunctionEnum_2_Scores_dict_ff.keys()) == sorted(Taxid_2_FunctionEnum_2_Scores_dict_p.keys())
    for taxid in Taxid_2_FunctionEnum_2_Scores_dict_ff.keys():
        FunctionEnum_2_Scores_dict_ff = Taxid_2_FunctionEnum_2_Scores_dict_ff[taxid]
        FunctionEnum_2_Scores_dict_p = Taxid_2_FunctionEnum_2_Scores_dict_p[taxid]
        for funcEnum in FunctionEnum_2_Scores_dict_ff:
            arr_ff = FunctionEnum_2_Scores_dict_ff[funcEnum]
            arr_p = FunctionEnum_2_Scores_dict_p[funcEnum]
            assert np.array_equal(arr_ff, arr_p)

def test_Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_flatfile_vs_sparse():
    """
    failed
    SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN = os.path.join(variables.TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt")
    """
    Taxid_2_FunctionEnum_2_Scores_dict_ff = query.get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=True, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=False)
    FunctionEnum_2_Scores_dict_ff = Taxid_2_FunctionEnum_2_Scores_dict_ff[9606]
    genome_scores_matrix, list_of_rowIndices_genome = slice_ScoresMatrix_for_given_ENSP(conftest.UniProt_IDs_human_list, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    m = genome_scores_matrix
    for i in range(len(m.indptr[:-1])):  # get column values
        index_row_start = m.indptr[i]
        index_row_stop = m.indptr[i + 1]
        if index_row_start == index_row_stop:
            continue
        funcEnum = i
        score_arr_sparse = m.data[index_row_start:index_row_stop]
        score_arr_ff = FunctionEnum_2_Scores_dict_ff[funcEnum]
        assert score_arr_sparse.shape[0] == score_arr_ff.shape[0]
        assert sorted(score_arr_sparse) == sorted(score_arr_ff)

def test_Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle_vs_sparse():
    """
    SparseMatrix_ENSPencoding_2_FuncEnum_UPS_FIN vs Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN_pickle
    Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN = os.path.join(variables.TABLES_DIR, "Taxid_2_FunctionEnum_2_Scores_table_UPS_FIN.txt")
    """
    Taxid_2_FunctionEnum_2_Scores_dict_p = query.get_Taxid_2_FunctionEnum_2_Scores_dict(read_from_flat_files=False, as_array_or_as_list="array", taxid_2_proteome_count=None, from_pickle=True)
    FunctionEnum_2_Scores_dict_p = Taxid_2_FunctionEnum_2_Scores_dict_p[9606]
    genome_scores_matrix, list_of_rowIndices_genome = slice_ScoresMatrix_for_given_ENSP(conftest.UniProt_IDs_human_list, ENSP_2_rowIndex_dict, CSC_ENSPencoding_2_FuncEnum)
    m = genome_scores_matrix
    for i in range(len(m.indptr[:-1])):  # get column values
        index_row_start = m.indptr[i]
        index_row_stop = m.indptr[i + 1]
        if index_row_start == index_row_stop:
            continue
        funcEnum = i
        score_arr_sparse = m.data[index_row_start:index_row_stop]
        score_arr_ff = FunctionEnum_2_Scores_dict_p[funcEnum]
        assert score_arr_sparse.shape[0] == score_arr_ff.shape[0]
        assert sorted(score_arr_sparse) == sorted(score_arr_ff)

def test_taxid_2_tuple_funcEnum_index_2_associations_counts():
    """
    snakemake r_Pickle_taxid_2_tuple_funcEnum_index_2_associations_counts_UPS_FIN
    compare pickled vs flatfile data
    """
    taxid_2_tuple_funcEnum_index_2_associations_counts_p = query.get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files=False, from_pickle=True)
    taxid_2_tuple_funcEnum_index_2_associations_counts_ff = query.get_background_taxid_2_funcEnum_index_2_associations(read_from_flat_files=True, from_pickle=False)
    assert sorted(taxid_2_tuple_funcEnum_index_2_associations_counts_p.keys()) == sorted(taxid_2_tuple_funcEnum_index_2_associations_counts_ff.keys())
    for taxid in taxid_2_tuple_funcEnum_index_2_associations_counts_ff.keys():
        funcEnum_index_2_associations_ff = taxid_2_tuple_funcEnum_index_2_associations_counts_ff[taxid]
        funcEnum_index_positions_arr_ff, counts_arr_ff = funcEnum_index_2_associations_ff
        funcEnum_index_2_associations_p = taxid_2_tuple_funcEnum_index_2_associations_counts_p[taxid]
        funcEnum_index_positions_arr_p, counts_arr_p = funcEnum_index_2_associations_p
        assert np.array_equal(funcEnum_index_positions_arr_ff, funcEnum_index_positions_arr_p)
        assert np.array_equal(counts_arr_ff, counts_arr_p)