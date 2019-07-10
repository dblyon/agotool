# cython: language_level=3, nonecheck=True, boundscheck=False, wraparound=False, profile=False


import Cython
######################################
######################################
from functools import reduce
import math
import numpy as np
import pandas as pd
from cython cimport boundscheck, wraparound, cdivision, nonecheck
from fisher import pvalue
cimport cython
cimport numpy as np
ctypedef np.uint8_t uint8
from cython.parallel cimport prange
import variables, query
from collections import defaultdict
from scipy import stats
######################################

##################################################################
##################################################################
@boundscheck(False)
@wraparound(False)
cdef create_funcEnum_count_background_v2(unsigned int[::1] funcEnum_count_background,
                                         const unsigned int[:, ::1] funcEnum_index_2_associations):
    """
    without returning 'funcEnum_count' the function does inplace change of 'funcEnum_count'
    :param funcEnum_array: np.array (of variable length, with functional enumeration 
    values, uint32, 
    i.e. which functional associations 
    are given for provided user input proteins)
    :param funcEnum_count: np.array (shape of array from 0 to max enumeration of 
    functional-terms, 
    uint32, each position codes for a 
    specific functional term, the value is a count for the given user input)
    :return: None
    """
    cdef int N, i, index_, count
    N = funcEnum_index_2_associations.shape[0]

    for i in range(N):
        index_ = funcEnum_index_2_associations[i][0]
        count = funcEnum_index_2_associations[i][1]
        funcEnum_count_background[index_] = count

@boundscheck(False)
@wraparound(False)
cdef create_funcEnum_count_background_v5(unsigned int[::1] funcEnum_count_background, # uint32
                                         const unsigned int[::1] funcEnum_index_arr, # uint32
                                         const unsigned short[::1] count_arr): # uint16
    """
    create_funcEnum_count_background_v3(funcEnum_count_background, index_positions_arr, counts_arr)
    without returning 'funcEnum_count' the function does inplace change of 'funcEnum_count'
    :param funcEnum_array: np.array (of variable length, with functional enumeration 
    values, uint32, 
    i.e. which functional associations 
    are given for provided user input proteins)
    :param funcEnum_count: np.array (shape of array from 0 to max enumeration of 
    functional-terms, 
    uint32, each position codes for a 
    specific functional term, the value is a count for the given user input)
    :return: None
    """
    cdef:
        int i, N = funcEnum_index_arr.shape[0]
        unsigned int index_
        unsigned short count

    for i in range(N):
        index_ = funcEnum_index_arr[i]
        count = count_arr[i]
        funcEnum_count_background[index_] = count

def count_all_term_abundance_corrected(ui, ENSP_2_functionEnumArray_dict, funcEnum_count):
    funcEnum_count_float = np.zeros(funcEnum_count.shape[0], dtype=np.dtype("float64"))
    for proteinGroup_list, correction_factor in ui.iter_bins():
        for proteinGroup in proteinGroup_list:
            try:
                funcEnum_associations = ENSP_2_functionEnumArray_dict[proteinGroup]
            except KeyError: # no functional annotation for proteins
                continue
            count_terms_cy_abundance_corrected(correction_factor, funcEnum_associations, funcEnum_count_float)
    funcEnum_count = np.around(funcEnum_count_float).astype(dtype=np.dtype("uint32"))
    return funcEnum_count

@boundscheck(False)
@wraparound(False)
cdef count_terms_cy_abundance_corrected(double correction_factor,
                                        unsigned int[::1] funcEnum_associations,
                                        double[::1] funcEnum_count_float):
    cdef int N, i, k
    N = funcEnum_associations.shape[0]
    for i in range(N):
        k = funcEnum_associations[i]
        funcEnum_count_float[k] += correction_factor

def count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans, funcEnum_count):
    for ENSP in (ENSP for ENSP in protein_ans if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count)

@boundscheck(False)
@wraparound(False)
cdef count_terms_cy(unsigned int[::1] funcEnum_associations,
                    unsigned int[::1] funcEnum_count):
    """
    without returning 'funcEnum_count' the function does inplace change of 'funcEnum_count'
    :param funcEnum_associations: np.array (of variable length, with functional associations 
    as enumerations (instead of strings), 
    uint32, i.e. which functional associations are given for provided user input proteins)
    :param funcEnum_count: np.array (shape of array from 0 to max enumeration of functional-terms, 
    uint32, each position codes for 
    a specific functional term, the value is a count for the given user input)
    :return: None
    """
    cdef int N, i, k
    N = funcEnum_associations.shape[0]
    for i in range(N):
        k = funcEnum_associations[i]
        funcEnum_count[k] += 1

def collect_scores_per_term_v0(protein_AN_list, ENSP_2_tuple_funcEnum_score_dict, list_2_array=False):
    """
    ENSP_2_tuple_funcEnum_score_dict['3702.AT1G01010.1']
    (array([ 211,  252,  253,  259,  323,  354,  358,  363,  373,  395,  415,
             613,  641,  745,  746, 1077, 1809, 1896, 1897, 1899, 1901, 1992,
            2048, 2049, 2067, 2085], dtype=uint32),
     array([4.2     , 4.166357, 4.195121, 3.257143, 1.234689, 0.428571,
            0.535714, 0.214286, 0.642857, 1.189679, 0.739057, 0.214286,
            0.214286, 3.      , 3.      , 3.      , 0.535714, 3.257143,
            3.257143, 3.257143, 3.257143, 0.641885, 4.166357, 3.      ,
            1.234689, 4.195121], dtype=float32))
    funcEnum_2_scores_dict: key: functionEnumeration, val: list of scores
    """
    funcEnum_2_scores_dict = defaultdict(lambda: [])
    for protein_AN in protein_AN_list:
        try:
            funcEnum_score = ENSP_2_tuple_funcEnum_score_dict[protein_AN]
        except KeyError:
            continue
        funcEnum_arr, score_arr = funcEnum_score
        len_funcEnum_arr = len(funcEnum_arr)
        for index_ in range(len_funcEnum_arr):
            score = score_arr[index_]
            funcEnum_2_scores_dict[funcEnum_arr[index_]].append(score)
    if list_2_array:
        return {funcEnum: np.asarray(scores, dtype=np.dtype("float64")) for funcEnum, scores in funcEnum_2_scores_dict.items()}
    # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

def collect_scores_per_term_abundance_corrected(ui, ENSP_2_tuple_funcEnum_score_dict, list_2_array=False):
    funcEnum_2_scores_dict = defaultdict(lambda: [])
    for proteinGroup_list, correction_factor in ui.iter_bins():
        for proteinGroup in proteinGroup_list:
            try:
                funcEnum_score = ENSP_2_tuple_funcEnum_score_dict[proteinGroup]
            except KeyError:
                continue
            funcEnum_arr, score_arr = funcEnum_score
            len_funcEnum_arr = len(funcEnum_arr)
            for index_ in range(len_funcEnum_arr):
                score = score_arr[index_]
                funcEnum_2_scores_dict[funcEnum_arr[index_]].append(score*correction_factor)
    if list_2_array:
        return {funcEnum: np.asarray(scores, dtype=np.dtype("float64")) for funcEnum, scores in funcEnum_2_scores_dict.items()}
        # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

@boundscheck(False)
@wraparound(False)
cdef calc_pvalues(unsigned int[::1] funcEnum_count_foreground,
                   unsigned int[::1] funcEnum_count_background,
                   unsigned int foreground_n,
                   unsigned int background_n,
                   double[::1] p_values,
                   cond_multitest,
                   double[::1] effectSizes):
    cdef:
        int index_, foreground_count, background_count, a, b, c, d
        int len_functions = funcEnum_count_foreground.shape[0]
        dict fisher_dict = {}
        double p_val_uncorrected
        double odds_ratio

    for index_ in range(len_functions):
        foreground_count = funcEnum_count_foreground[index_]
        if foreground_count == 0:
            # continue and leave p-value set to 1, no multiple testing
            continue
        elif foreground_count == 1:
            # leave p-value set to 1, BUT DO multiple testing
            cond_multitest[index_] = True
        else:
            # calculate p-value and do multiple testing
            background_count = funcEnum_count_background[index_]
            cond_multitest[index_] = True
            a = foreground_count # number of proteins associated with given GO-term
            b = foreground_n - foreground_count # number of proteins not associated with GO-term
            c = background_count
            d = background_n - background_count
            p_val_uncorrected = fisher_dict.get((a, b, c, d), -1)
            if p_val_uncorrected == -1:
                p_val_uncorrected = pvalue(a, b, c, d).right_tail
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            p_values[index_] = p_val_uncorrected
            try:
                # https://stats.stackexchange.com/questions/22508/effect-size-for-fishers-exact-test
                # odds_ratio = (a * d) / (b * c) # true odds ratio
                # odds_ratio = (d / (c + d)) - (a / (a + b)) # difference in proportions
                odds_ratio = (a / (a + b)) - (c / (c + d)) # difference in proportions DBL
                # odds_ratio = (a / (a + b)) / (c / (c + d)) # from old agotool, ratio of percent in fg to percent in bg
                # odds_ratio = a
            except ZeroDivisionError:
                odds_ratio = np.nan
            effectSizes[index_] = odds_ratio
    return cond_multitest

@boundscheck(False)
@wraparound(False)
@cdivision(True)
cpdef BenjaminiHochberg_cy(double[::1] p_values,
                         unsigned int num_total_tests,
                         double[::1] p_values_corrected,
                         unsigned int[::1] indices_2_BH):
    """
    #!!! cpdef instead of cdef for scores debugging/profiling
    ein index array mit absoluten positionen, pvals absolut und pvalscorr absolut
    p_values_2_BH, p_values_2_BH.shape[0], p_values_corrected_2_BH, indices_of_p_values_2_BH)
    :param p_values: unsorted array of float
    :param num_total_test: Integer
    :param p_values_corrected: array of float (1.0 by default), shape is full function_enumeration_len NOT p_values    
    :param indices_2_BH: indices of superset, shape of array reduced to p_values_2_BH
    iterate over p_values in p_values_2_BH_sort_order
    set p_value_corrected at positions from indices_2_BH[p_values_2_BH_sort_order]
    """
    cdef:
        double prev_bh_value = 0.0
        double p_value, bh_value
        unsigned int index_2_BH, i
        unsigned int enum_counter = 1
        unsigned int N = indices_2_BH.shape[0]

    for i in range(N):
        index_2_BH = indices_2_BH[i]
        p_value = p_values[index_2_BH]
        bh_value = p_value * num_total_tests / enum_counter
        # Sometimes this correction can give values greater than 1,
        # so we set those values at 1
        bh_value = min(bh_value, 1)
        # To preserve monotonicity in the values, we take the
        # maximum of the previous value or this one, so that we
        # don't yield a value less than the previous.
        bh_value = max(bh_value, prev_bh_value)
        prev_bh_value = bh_value
        p_values_corrected[index_2_BH] = bh_value
        enum_counter += 1

def map_funcEnum_2_ENSPs(protein_ans_list, ENSP_2_functionEnumArray_dict,
                           funcEnum_indices, foreground_ids_arr_of_string):
    """
    previously named get_foreground_IDs_arr now map_funcEnum_2_ENSPs
    for given protein_ans produce concatenate strings of ENSP associations
    :param protein_ans_list: List of String (or array), user provided ENSPs
    :param ENSP_2_functionEnumArray_dict: key: String, val: array of uint32, all ENSP to function enum associations
    :param funcEnum_indices: array of uint32, relevant func enums after filtering
    :param foreground_ids_arr_of_string: list of empty string, len of function_enumeration_len, list instead of array since len of longest string unknown and would take lots of memory
    :return: List of String of len function_enumeration_len with comma sep ENSPs at index positions coding for func enum
    """
    funcEnum_2_ENSPs_dict = {index_: [] for index_ in funcEnum_indices}
    for ENSP in protein_ans_list:
        try:
            functionEnumArray = ENSP_2_functionEnumArray_dict[ENSP]
        except KeyError: # happens since some ENSPs are without functional associations (or if single association in genome it is filtered out)
            continue
        for funcEnum in functionEnumArray:
            if funcEnum in funcEnum_2_ENSPs_dict:
                funcEnum_2_ENSPs_dict[funcEnum].append(ENSP)

    for funcEnum, ENSPs in funcEnum_2_ENSPs_dict.items():
        foreground_ids_arr_of_string[funcEnum] = ";".join(sorted(ENSPs)) # needs to be sorted otherwise grouping incorrect later on
    return foreground_ids_arr_of_string

def get_preloaded_objects_for_single_analysis(blacklisted_terms_bool_arr, function_enumeration_len=6834675, method="genome"):
    """
    funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, foreground_ids_arr_of_string, cond_filter, cond_PMIDs
    """
    funcEnum_count_foreground = np.zeros(shape=function_enumeration_len, dtype=np.dtype("uint32"))
    foreground_ids_arr_of_string = np.empty(shape=(function_enumeration_len,), dtype=object)
    blacklisted_terms_bool_arr_temp = blacklisted_terms_bool_arr.copy()
    # was uint32, but uint16 is sufficient for STRING v11, not using it for the foreground due to potential redundancy
    # or for "compare_samples" for the same reason --> keep the same
    funcEnum_count_background = np.zeros(shape=function_enumeration_len, dtype=np.dtype("uint32"))
    p_values = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
    p_values_corrected = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
    cond_multitest = np.zeros(function_enumeration_len, dtype=bool)
    cond_filter = np.ones(function_enumeration_len, dtype=bool)
    cond_PMIDs = np.zeros(function_enumeration_len, dtype=bool)
    cond_terms_reduced_with_ontology = np.zeros(function_enumeration_len, dtype=bool)
    background_ids_arr_of_string = np.empty(shape=(function_enumeration_len,), dtype=object)
    effectSizes = np.empty(function_enumeration_len, dtype=np.dtype("float64"))
    effectSizes.fill(np.nan)
    return foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes

@boundscheck(False)
@wraparound(False)
cdef filter_parents_if_same_foreground(uint8[::1] blacklisted_terms_bool_arr_temp,
                                       cond_terms_reduced_with_ontology,
                                       dict lineage_dict_enum,
                                       df):
    """    
    potential speed up using C++ types for sets, BUT data is copied so profile 

    # distutils: language = c++    
    from libcpp.vector cimport vector
    from libcpp.set cimport set 
    """
    cdef:
        unsigned int term_enum, lineage_term
        # unsigned int lineage

    for group_terms in df.sort_values(["foreground_ids", "p_value", "hierarchical_level"], ascending=[True, True, False]).groupby("foreground_ids", sort=False).apply(lambda group: group["term_enum"].values):
        group_terms_set = set(group_terms)
        for term_enum in group_terms:
            if blacklisted_terms_bool_arr_temp[term_enum] == 0: # False
                cond_terms_reduced_with_ontology[term_enum] = True
                try:
                    lineage = lineage_dict_enum[term_enum] & group_terms_set # bitwise intersection
                except KeyError: # not in hierarchy (even though it should be, but some Reactome terms are inconsistent)
                    blacklisted_terms_bool_arr_temp[term_enum] = 1 # True
                    continue
                for lineage_term in lineage:
                    blacklisted_terms_bool_arr_temp[lineage_term] = 1 # True

def multiple_testing_per_entity_type(cond_etype, cond_multitest, p_values, p_values_corrected, indices_arr):
    # select indices for given entity type and if multiple testing needs to be applied
    cond = cond_etype & cond_multitest
    # select p_values for BenjaminiHochberg
    p_values_2_BH = p_values[cond]
    num_total_tests = p_values_2_BH.shape[0]
    # select indices for BH
    indices_2_BH = indices_arr[cond]
    # sort p_values and remember indices sort order
    p_values_2_BH_sort_order = np.argsort(p_values_2_BH) # index positions of a reduced set
    indices_2_BH_of_superset = indices_2_BH[p_values_2_BH_sort_order]
    BenjaminiHochberg_cy(p_values, num_total_tests, p_values_corrected, indices_2_BH_of_superset)

def s_value(df, p_value_cutoff=0.05, KS_stat_cutoff=0.1, diff_proportions_cutoff=0.1):
    """
    calculate 's-value' type statistic in order to rank based on a combination of p-value and effect size
    for etypes -20, -25, and -26 (GOCC, BTO, and DOID) --> Common Language Effect Size
    for other etypes difference in ratios
    justification for cles_cutoff --> Kerby (https://doi.org/10.2466%2F11.IT.3.1) if the null is true the CLES is 50%
    justification for diff_proportions_cutoff --> unsure how to justify from lit. need be smaller than cles_cutoff
    --> changed from cles to KS_stat
    """
    # df["p_value_minlog"] = df["p_value"].apply(lambda x: -1*math.log10(x))
    min_pval = df["p_value"][df["p_value"] > 0].min()
    df["p_value_minlog"] = df["p_value"].apply(log_take_min_if_zero, args=(min_pval, ))
    df["s_value"] = 0.0
    cond_scores = df["etype"].isin([-20, -25, -26])
    p_value_cutoff = -1 * math.log10(p_value_cutoff) # test for values smaller than 0
    #     df.loc[cond_scores, "s_value"] = (df.loc[cond_scores, "p_value_minlog"] - p_value_cutoff) * abs(df.loc[cond_scores, "effectSize"] - KS_stat_cutoff)
    #     df.loc[~cond_scores, "s_value"] = (df.loc[~cond_scores, "p_value_minlog"] - p_value_cutoff) * abs(df.loc[~cond_scores, "effectSize"] - diff_proportions_cutoff)
    df["s_value"] = df["p_value_minlog"] * df["effectSize"]
    df = df.drop(columns=["p_value_minlog"])
    df["rank"] = df.groupby("etype")["s_value"].rank(ascending=False)
    return df

def log_take_min_if_zero(val, min_pval):
    try:
        return -1*math.log10(val)
    except:
        return -1*math.log10(min_pval)

def limit_to_entity_types(limit_2_entity_type, function_enumeration_len, etype_cond_dict, funcEnum_count_foreground):
    if limit_2_entity_type is not None:
        cond_limit_2_entity_type = np.zeros(function_enumeration_len, dtype=bool)
        for cond_name in ["cond_" + etype[1:] for etype in limit_2_entity_type.split(";")]:
            try:
                cond_limit_2_entity_type |= etype_cond_dict[cond_name] # add other etypes
            except KeyError: # user provided etype can be mistyped of non-existent
                pass
        # set funcEnumAssociations to zero where cond_limit_2_entity_type is False
        funcEnum_count_foreground[~cond_limit_2_entity_type] = 0

def limit_to_go_subset(etype_cond_dict, go_slim_subset, goslimtype_2_cond_dict, funcEnum_count_foreground):
    if go_slim_subset is None:
        return funcEnum_count_foreground
    cond_GO_etypes = etype_cond_dict["cond_21"] | etype_cond_dict["cond_22"] | etype_cond_dict["cond_23"]
    cond = cond_GO_etypes != goslimtype_2_cond_dict[go_slim_subset] # select all GO terms that are not slim
    # set these to count 0
    funcEnum_count_foreground[cond] = 0
    return funcEnum_count_foreground

def add_funcEnums_2_dict(protein_ans_fg, ENSP_2_functionEnumArray_dict, ENSP_2_tuple_funcEnum_score_dict):
    # add Protein 2 functionEnum info for JensenLabScore data to get foregroundIDs in DF
    for protein in protein_ans_fg:
        try: # sort is probably not necessary # potential speedup removing the sorting
            ENSP_2_functionEnumArray_dict[protein] = np.sort(np.concatenate((ENSP_2_tuple_funcEnum_score_dict[protein][0], ENSP_2_functionEnumArray_dict[protein])))
        except KeyError:
            pass # print("protein {} not in ENSP_2_tuple_funcEnum_score_dict".format(protein)) # --> simply not annotated with anything from textmining

def replace_secondary_and_primary_IDs(ans_string, secondary_2_primary_dict, invert_dict=False):
    if invert_dict:
        dict_2_use = {v: k for k, v in secondary_2_primary_dict.items()}
    else:
        dict_2_use = secondary_2_primary_dict
    ids_2_return = []
    for id_ in ans_string.split(";"): # if proteinGroup
        if id_ in dict_2_use:
            ids_2_return.append(dict_2_use[id_])
        else:
            ids_2_return.append(id_)
    return ";".join(ids_2_return)

def filter_stuff(args_dict, protein_ans_fg, p_values_corrected, foreground_ids_arr_of_string, funcEnum_count_foreground, year_arr, p_values, indices_arr, ENSP_2_functionEnumArray_dict, cond_filter, etype_cond_dict, cond_PMIDs, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids):
    FDR_cutoff = args_dict["FDR_cutoff"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    filter_PMID_top_n = args_dict["filter_PMID_top_n"]
    if FDR_cutoff is not None:
        cond_filter = p_values_corrected <= FDR_cutoff
    if filter_foreground_count_one is True:  # remove terms without only one annotation
        cond_filter &= funcEnum_count_foreground > 1
    else:  # remove terms without any annotation
        cond_filter &= funcEnum_count_foreground > 0
    if filter_PMID_top_n is not None:
        cond_PMID_2_filter = cond_filter & etype_cond_dict["cond_56"]  # -56
        df_PMID = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_PMID_2_filter].view(), "year": year_arr[cond_PMID_2_filter].view(), "p_value": p_values[cond_PMID_2_filter].view(), "FDR": p_values_corrected[cond_PMID_2_filter].view(), "indices_arr": indices_arr[cond_PMID_2_filter].view()})
        indices_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])["indices_arr"].values[:filter_PMID_top_n]
        for index_ in indices_PMID:
            cond_PMIDs[index_] = True
    else:  # since no filtering use all PMIDs
        cond_PMIDs = cond_filter & etype_cond_dict["cond_56"]
    cond_etypes_with_ontology_filtered = cond_etypes_with_ontology & cond_filter  # {-21, -22, -23, -51, -57}
    cond_etypes_rem_foreground_ids_filtered = cond_etypes_rem_foreground_ids & cond_filter  # remaining etypes -52, -53, -54, -55
    cond_IDs_2_query = cond_PMIDs | cond_etypes_with_ontology_filtered | cond_etypes_rem_foreground_ids_filtered
    ### get foreground IDs of relevant subset --> array for entire data set
    funcEnum_indices_for_IDs = indices_arr[cond_IDs_2_query]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_fg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, foreground_ids_arr_of_string)
    return foreground_ids_arr_of_string, funcEnum_indices_for_IDs, cond_etypes_with_ontology_filtered, cond_etypes_rem_foreground_ids_filtered, cond_filter

def add_protein_groups_to_ENSP_2_functionEnumArray_dict(ENSP_2_functionEnumArray_dict, all_unique_proteinGroups):
    """
    for all protein groups
    """
    for proteinGroup in all_unique_proteinGroups:
        if proteinGroup not in ENSP_2_functionEnumArray_dict:
            functionEnumArray_list = []
            for protein in proteinGroup.split(";"):
                try:
                    functionEnumArray_list.append(ENSP_2_functionEnumArray_dict[protein])
                except KeyError: # no functional annotation for given protein
                    pass
            try:
                ENSP_2_functionEnumArray_dict[proteinGroup] = reduce(np.union1d, functionEnumArray_list)
            except TypeError: # empty list
                #ENSP_2_functionEnumArray_dict[proteinGroup] = False #np.array(dtype=np.dtype("uint32"))
                pass
    return ENSP_2_functionEnumArray_dict

def KolmogorovSmirnov(foreground_n, background_n, funcEnum_2_scores_dict_fg, funcEnum_2_scores_dict_bg, p_values, cond_multitest, effectSizes, FDR_cutoff, funcEnum_count_foreground, funcEnum_count_background, is_overrepresented=True):
    for funcEnum, scores_fg in funcEnum_2_scores_dict_fg.items():
        scores_bg = funcEnum_2_scores_dict_bg[funcEnum]
        scores_bg = list(scores_bg) # for genome method
        len_scores_fg = len(scores_fg)
        number_of_zeros_2_fill = foreground_n - len_scores_fg
        if number_of_zeros_2_fill > 0:
            scores_fg = [0]*number_of_zeros_2_fill + scores_fg
        len_scores_bg = len(scores_bg)
        number_of_zeros_2_fill = background_n - len_scores_bg
        if number_of_zeros_2_fill > 0:
            scores_bg = [0]*number_of_zeros_2_fill + scores_bg
        statistic, pvalue = stats.ks_2samp(scores_fg, scores_bg)
        if pvalue <= FDR_cutoff:
            is_greater = np.median(scores_fg) > np.median(scores_bg)
        else:
            is_greater = None
        if is_overrepresented and is_greater:
            p_values[funcEnum] = pvalue
            effectSizes[funcEnum] = statistic
        else:
            # p_values[funcEnum] = 1 # should already be the default
            pass
        cond_multitest[funcEnum] = True
        funcEnum_count_foreground[funcEnum] = len_scores_fg # number of scores, important for BH
        funcEnum_count_background[funcEnum] = len_scores_bg

def run_enrichment_cy(ui, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, low_memory=False):
    if not low_memory:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, ENSP_2_tuple_funcEnum_score_dict, Taxid_2_FunctionEnum_2_Scores_dict, goslimtype_2_cond_dict = static_preloaded_objects
    else:  # missing: description_arr, category_arr, ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, ENSP_2_tuple_funcEnum_score_dict, Taxid_2_FunctionEnum_2_Scores_dict, goslimtype_2_cond_dict = static_preloaded_objects
    foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes = preloaded_objects_per_analysis
    em = ui.enrichment_method
    foreground_n = ui.get_foreground_n()

    if em == "genome":
        taxid = args_dict["taxid"]
        background_n = taxid_2_proteome_count[taxid]
    else:
        background_n = ui.get_background_n()
    protein_ans_fg = ui.get_foreground_an_set()
    if ui.enrichment_method in {"abundance_correction", "compare_samples"}:
        protein_ans_bg = ui.get_background_an_set()
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(ui.get_all_individual_AN(), dict_2_array=True)
    ### add protein groups to ENSP_2_functionEnumArray_dict
    ENSP_2_functionEnumArray_dict = add_protein_groups_to_ENSP_2_functionEnumArray_dict(ENSP_2_functionEnumArray_dict, ui.get_all_unique_proteinGroups())

    ## count foreground
    count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_fg, funcEnum_count_foreground)

    ### count background
    if em == "genome":
        if not low_memory:
            funcEnum_index_2_associations = taxid_2_tuple_funcEnum_index_2_associations_counts[taxid]
            index_positions_arr, counts_arr = funcEnum_index_2_associations
            create_funcEnum_count_background_v5(funcEnum_count_background, index_positions_arr, counts_arr)
        else:
            background_counts_list = query.get_background_count_array(taxid)
            funcEnum_index_2_associations = np.asarray(background_counts_list, dtype=np.dtype("uint32"))
            funcEnum_index_2_associations.flags.writeable = False
            create_funcEnum_count_background_v2(funcEnum_count_background, funcEnum_index_2_associations)
    elif em == "abundance_correction":
        funcEnum_count_background = count_all_term_abundance_corrected(ui, ENSP_2_functionEnumArray_dict, funcEnum_count_background)
        background_n = foreground_n
    else:
        count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_bg, funcEnum_count_background) # error ToDo debug

    ## limit to given entity types
    limit_to_entity_types(args_dict["limit_2_entity_type"], function_enumeration_len, etype_cond_dict, funcEnum_count_foreground)
    limit_to_go_subset(etype_cond_dict, args_dict["go_slim_subset"], goslimtype_2_cond_dict, funcEnum_count_foreground)

    ### calculate Fisher p-values and get bool array for multiple testing
    cond_multitest = calc_pvalues(funcEnum_count_foreground, funcEnum_count_background, foreground_n, background_n, p_values, cond_multitest, effectSizes)

    ### Jensenlab Scores KS test
    funcEnum_2_scores_dict_fg = collect_scores_per_term_v0(protein_ans_fg, ENSP_2_tuple_funcEnum_score_dict)
    if em == "abundance_correction":
        funcEnum_2_scores_dict_bg = collect_scores_per_term_abundance_corrected(ui, ENSP_2_tuple_funcEnum_score_dict)
    elif em == "genome":
        ### precomputed ToDo
        # ToDo check that taxid in list of taxids with precomputed backgrounds
        funcEnum_2_scores_dict_bg = Taxid_2_FunctionEnum_2_Scores_dict[taxid] # taxid is an Integer
    else:
        funcEnum_2_scores_dict_bg = collect_scores_per_term_v0(protein_ans_bg, ENSP_2_tuple_funcEnum_score_dict)
    try:
        KolmogorovSmirnov(foreground_n, background_n, funcEnum_2_scores_dict_fg, funcEnum_2_scores_dict_bg, p_values, cond_multitest, effectSizes, args_dict["FDR_cutoff"], funcEnum_count_foreground, funcEnum_count_background, is_overrepresented=True)
    except KeyError: # e.g. enrichment_method "genome" using different taxon for foreground than background
        args_dict["ERROR_taxid"] = "ERROR_taxid: 'taxid': {}. Please make sure you've selected the correct NCBI TaxID for your input proteins. The UniProt reference proteome for the TaxID exists, but seems not to match your input proteins.".format(args_dict["taxid"])
        return args_dict

    ### multiple testing per entity type, save results preformed p_values_corrected
    for etype_name, cond_etype in etype_cond_dict.items():
        multiple_testing_per_entity_type(cond_etype, cond_multitest, p_values, p_values_corrected, indices_arr)

    add_funcEnums_2_dict(protein_ans_fg, ENSP_2_functionEnumArray_dict, ENSP_2_tuple_funcEnum_score_dict)
    foreground_ids_arr_of_string, funcEnum_indices_for_IDs, cond_etypes_with_ontology_filtered, cond_etypes_rem_foreground_ids_filtered, cond_filter = filter_stuff(args_dict, protein_ans_fg, p_values_corrected, foreground_ids_arr_of_string, funcEnum_count_foreground, year_arr, p_values, indices_arr, ENSP_2_functionEnumArray_dict, cond_filter, etype_cond_dict, cond_PMIDs, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids)
    if em in {"compare_samples"}:
        background_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_bg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, background_ids_arr_of_string)

    ### filter etypes with ontologies --> cond_terms_reduced_with_ontology
    df_with_ontology = pd.DataFrame({"term_enum": indices_arr[cond_etypes_with_ontology_filtered].view(), "foreground_ids": foreground_ids_arr_of_string[cond_etypes_with_ontology_filtered].view(), "hierarchical_level": hierlevel_arr[cond_etypes_with_ontology_filtered].view(), "p_value": p_values[cond_etypes_with_ontology_filtered].view(), "foreground_count": funcEnum_count_foreground[cond_etypes_with_ontology_filtered].view(), "etype": entitytype_arr[cond_etypes_with_ontology_filtered].view()})
    filter_parents = args_dict["filter_parents"]
    if filter_parents:  # only for etypes with ontology, but since foreground IDs needed get them for all
        ### modifies cond_terms_reduced_with_ontology inplace
        filter_parents_if_same_foreground(blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, lineage_dict_enum, df_with_ontology)
    else:  # since no filtering done use all etypes with ontology
        cond_terms_reduced_with_ontology = cond_filter & cond_etypes_with_ontology

    ### calc ratio in foreground, count foreground / len(protein_ans)
    ratio_in_foreground = funcEnum_count_foreground / foreground_n
    ratio_in_background = funcEnum_count_background / background_n

    ### concatenate filtered results
    cond_2_return = cond_PMIDs | cond_terms_reduced_with_ontology | cond_etypes_rem_foreground_ids_filtered
    if not low_memory:
        df_2_return = pd.DataFrame({"term": functionalterm_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "p_value": p_values[cond_2_return].view(),
                                    "FDR": p_values_corrected[cond_2_return].view(),
                                    "category": category_arr[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "description": description_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "ratio_in_background": ratio_in_background[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view(),
                                    "effectSize": effectSizes[cond_2_return].view()})
    else:
        df_2_return = pd.DataFrame({"term": functionalterm_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "p_value": p_values[cond_2_return].view(),
                                    "FDR": p_values_corrected[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "ratio_in_background": ratio_in_background[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view(),
                                    "effectSize": effectSizes[cond_2_return].view(),
                                    "funcEnum": indices_arr[cond_2_return].view()})
        df_2_return["category"] = df_2_return["etype"].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return["description"] = df_2_return["funcEnum"].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])

    cols_2_return_sort_order = ['etype', 'term', 'hierarchical_level', 'description', 'year', 'p_value', 'FDR', 'effectSize', 'ratio_in_foreground', 'ratio_in_background', 'foreground_count', 'foreground_n', 'background_count', 'background_n', 'foreground_ids', 'background_ids', 's_value', 'rank', 'funcEnum', 'category']
    if em == "compare_samples":
        df_2_return["background_ids"] = background_ids_arr_of_string[cond_2_return].view()
    else:
        cols_2_return_sort_order.remove("background_ids")
    df_2_return = s_value(df_2_return)
    df_2_return = ui.translate_primary_back_to_secondary(df_2_return)
    df_2_return["foreground_n"] = foreground_n
    df_2_return["background_n"] = background_n
    #     df_2_return = df_2_return[variables.cols_sort_order_compare_samples + ["effectSize"]]
    return df_2_return[cols_2_return_sort_order]

def run_characterize_foreground_cy(ui, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, low_memory=False):
    if not low_memory:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, ENSP_2_tuple_funcEnum_score_dict, Taxid_2_FunctionEnum_2_Scores_dict, goslimtype_2_cond_dict = static_preloaded_objects
    else:  # missing: description_arr, category_arr, ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, ENSP_2_tuple_funcEnum_score_dict, Taxid_2_FunctionEnum_2_Scores_dict, goslimtype_2_cond_dict = static_preloaded_objects
    foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes = preloaded_objects_per_analysis
    em = ui.enrichment_method
    foreground_n = ui.get_foreground_n()

    protein_ans_fg = ui.get_foreground_an_set()
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(ui.get_all_individual_AN(), dict_2_array=True)
    ### add protein groups to ENSP_2_functionEnumArray_dict
    ENSP_2_functionEnumArray_dict = add_protein_groups_to_ENSP_2_functionEnumArray_dict(ENSP_2_functionEnumArray_dict, ui.get_all_unique_proteinGroups())

    ## count foreground
    count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_fg, funcEnum_count_foreground)

    ## limit to given entity types
    limit_to_entity_types(args_dict["limit_2_entity_type"], function_enumeration_len, etype_cond_dict, funcEnum_count_foreground)
    limit_to_go_subset(etype_cond_dict, args_dict["go_slim_subset"], goslimtype_2_cond_dict, funcEnum_count_foreground)

    ### Jensenlab Scores KS test
    funcEnum_2_scores_dict_fg = collect_scores_per_term_v0(protein_ans_fg, ENSP_2_tuple_funcEnum_score_dict)

    add_funcEnums_2_dict(protein_ans_fg, ENSP_2_functionEnumArray_dict, ENSP_2_tuple_funcEnum_score_dict)

    ### calc ratio in foreground, count foreground / len(protein_ans)
    ratio_in_foreground = funcEnum_count_foreground / foreground_n

    ### concatenate filtered results
    if args_dict["filter_foreground_count_one"]:
        cond_2_return = funcEnum_count_foreground > 0
    try:
        privileged = args_dict["privileged"]
    except KeyError:
        privileged = False
    if not privileged:
        # remove KEGG unless privileged
        cond_kegg = etype_cond_dict["cond_52"]
        cond_2_return = cond_2_return & ~cond_kegg

    funcEnum_indices_for_IDs = indices_arr[cond_2_return]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_fg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, foreground_ids_arr_of_string)
    if not low_memory:
        df_2_return = pd.DataFrame({"term": functionalterm_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "category": category_arr[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "description": description_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view()})
    else:
        df_2_return = pd.DataFrame({"term": functionalterm_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "funcEnum": indices_arr[cond_2_return].view()})
        df_2_return["category"] = df_2_return["etype"].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return["description"] = df_2_return["funcEnum"].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])

    cols_2_return_sort_order = ['etype', 'term', 'hierarchical_level', 'description', 'year','ratio_in_foreground', 'foreground_count', 'foreground_n', 'foreground_ids', 'funcEnum', 'category']
    df_2_return = ui.translate_primary_back_to_secondary(df_2_return)
    df_2_return["foreground_n"] = foreground_n
    #     df_2_return = df_2_return[variables.cols_sort_order_compare_samples + ["effectSize"]]
    return df_2_return[cols_2_return_sort_order]

# def cles(lessers, greaters):
#     """
#     proportion of favorable pairs (McGraw and Wong (1992))

#     # code from https://github.com/ajschumacher/cles
#     # explanation from https://janhove.github.io/reporting/2016/11/16/common-language-effect-sizes
#     the probability that a score sampled at random from one distribution will be greater than a score
#     sampled from some other distribution.

#     https://stats.stackexchange.com/questions/124501/mann-whitney-u-test-confidence-interval-for-effect-size
#     this is the proportion of sample pairs that supports a stated hypothesis

#     Common-Language Effect Size
#     Probability that a random draw from `greater` is in fact greater
#     than a random draw from `lesser`.
#     Args:
#       lesser, greater: Iterables of comparables.
#     """
#     if len(lessers) == 0 and len(greaters) == 0:
#         raise ValueError('At least one argument must be non-empty')
#     # These values are a bit arbitrary, but make some sense.
#     # (It might be appropriate to warn for these cases.)
#     if len(lessers) == 0:
#         return 1
#     if len(greaters) == 0:
#         return 0
#     numerator = 0
#     lessers, greaters = sorted(lessers), sorted(greaters)
#     lesser_index = 0
#     for greater in greaters:
#         while lesser_index < len(lessers) and lessers[lesser_index] < greater:
#             lesser_index += 1
#         numerator += lesser_index  # the count less than the greater
#     denominator = len(lessers) * len(greaters)
#     # return float(numerator) / denominator # python 2
#     return numerator / denominator # python 3

# @boundscheck(False)
# @wraparound(False)
# cpdef cles_cy(double[::1] lessers, double[::1] greaters):
#     cdef int len_lessers, len_greaters
#     len_lessers = len(lessers)
#     len_greaters = len(greaters)
#     if len_lessers == 0 and len_greaters == 0:
#         raise ValueError('At least one argument must be non-empty')
#     # These values are a bit arbitrary, but make some sense.
#     # (It might be appropriate to warn for these cases.)
#     if len_lessers == 0:
#         return 1
#     if len_greaters == 0:
#         return 0

#     cdef int numerator = 0
#     cdef int denominator
#     cdef int greater_index = 0
#     cdef int lesser_index = 0
#     cdef double greater
#     lessers = np.sort(lessers)
#     greaters = np.sort(greaters)

#     for greater_index in range(len_greaters):
#         greater = greaters[greater_index]
#         while lesser_index < len_lessers and lessers[lesser_index] < greater:
#             lesser_index += 1
#         numerator += lesser_index  # the count less than the greater
#     denominator = len_lessers * len_greaters
#     return numerator / denominator # python 3
# def MannWhitneyU_v2(foreground_ENSPs, background_ENSPs, ENSP_2_tuple_funcEnum_score_dict, etype_cond_dict, p_values, cond_multitest, effectSizes, low=-0.002, high=0.002, fill_zeros_background=False):
#     funcEnum_2_scores_dict_fg = collect_scores_per_term_v0(foreground_ENSPs, ENSP_2_tuple_funcEnum_score_dict)
#     funcEnum_2_scores_dict_bg = collect_scores_per_term_v0(background_ENSPs, ENSP_2_tuple_funcEnum_score_dict) #!!! replace precomputed

#     ### one sided test --> overrepresented
#     for funcEnum, scores_fg in funcEnum_2_scores_dict_fg.items():
#         scores_bg = funcEnum_2_scores_dict_bg[funcEnum]
#         scores_fg, scores_bg = add_noise_2_scores(scores_fg, scores_bg, len(foreground_ENSPs), len(background_ENSPs), low, high, fill_zeros_background)
#         U, pval = stats.mannwhitneyu(scores_fg, scores_bg, use_continuity=True, alternative="greater")
#         p_values[funcEnum] = pval
#         cond_multitest[funcEnum] = True
#         effectSize = cles(scores_bg, scores_fg)
#         effectSizes[funcEnum] = effectSize

# def add_noise_2_scores(scores_fg, scores_bg, len_foreground_ENSPs, len_background_ENSPs, low=-0.002, high=0.002, fill_zeros_background=False):
#     len_scores_fg = len(scores_fg)
#     len_scores_bg = len(scores_bg)
#     scores_fg_noisy = np.array(scores_fg) + np.random.uniform(low, high, len_scores_fg)
#     number_of_zeros_2_fill = len_foreground_ENSPs - len_scores_fg
#     if number_of_zeros_2_fill > 0:
#         zeros_fg_noisy = np.random.uniform(low, high, number_of_zeros_2_fill)
#         scores_fg_v2 = np.concatenate((scores_fg_noisy, zeros_fg_noisy))
#     else:
#         scores_fg_v2 = scores_fg_noisy
#     scores_bg_noisy = np.array(scores_bg) + np.random.uniform(low, high, len_scores_bg)
#     if fill_zeros_background: # background as large as number of genes in genome
#         number_of_zeros_2_fill = len_background_ENSPs - len_scores_bg # too large
#     else: # background roughly as large as foreground
#         number_of_zeros_2_fill = len_foreground_ENSPs - len_scores_bg
#     if number_of_zeros_2_fill > 0:
#         zeros_bg_noisy = np.random.uniform(low, high, number_of_zeros_2_fill)
#         scores_bg_v2 = np.concatenate((scores_bg_noisy, zeros_bg_noisy))
#     else:
#         scores_bg_v2 = scores_bg_noisy
#     return scores_fg_v2, scores_bg_v2