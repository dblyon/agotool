# cython: language_level=3, nonecheck=True, boundscheck=False, wraparound=False, profile=False

import numpy as np
np.get_include()
from cython cimport boundscheck, wraparound, cdivision, nonecheck
cimport cython
cimport numpy as np
ctypedef np.uint8_t uint8

from fisher import pvalue
import pandas as pd

import variables, query


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

# @boundscheck(False)
# @wraparound(False)
# cdef create_funcEnum_count_background_v4(unsigned int[::1] funcEnum_count_background, # uint32
#                                          const unsigned int[::1] funcEnum_index_arr, # uint32
#                                          const unsigned short[::1] count_arr): # uint16
#     """
#     create_funcEnum_count_background_v3(funcEnum_count_background, index_positions_arr, counts_arr)
#     without returning 'funcEnum_count' the function does inplace change of 'funcEnum_count'
#     :param funcEnum_array: np.array (of variable length, with functional enumeration
#     values, uint32,
#     i.e. which functional associations
#     are given for provided user input proteins)
#     :param funcEnum_count: np.array (shape of array from 0 to max enumeration of
#     functional-terms,
#     uint32, each position codes for a
#     specific functional term, the value is a count for the given user input)
#     :return: None
#     """
#     cdef:
#         int i, N = funcEnum_index_arr.shape[0]
#         unsigned short index_
#         unsigned short count

#     for i in range(N):
#         index_ = funcEnum_index_arr[i]
#         count = count_arr[i]
#         funcEnum_count_background[index_] = count

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

@boundscheck(False)
@wraparound(False)
cdef calc_pvalues(unsigned int[::1] funcEnum_count_foreground,
                   unsigned int[::1] funcEnum_count_background,
                   unsigned int foreground_n,
                   unsigned int background_n,
                   double[::1] p_values,
                   cond_multitest):
    """
    modify values of pvalues array via memory view, return conditionaly bool array of index positions 
    that will be corrected for multiple testing
    """
    cdef:
        int index_, foreground_count, background_count, a, b, c, d
        int len_functions = funcEnum_count_foreground.shape[0]
        dict fisher_dict = {}
        double p_val_uncorrected

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
            # if a == c and b == d:
            #    p_val_uncorrected = 1.0
            # else:
            p_val_uncorrected = fisher_dict.get((a, b, c, d), -1)
            if p_val_uncorrected == -1:
                p_val_uncorrected = pvalue(a, b, c, d).right_tail
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            p_values[index_] = p_val_uncorrected
    return cond_multitest

@boundscheck(False)
@wraparound(False)
@cdivision(True)
cdef BenjaminiHochberg_cy(double[::1] p_values,
                         unsigned int num_total_tests,
                         double[::1] p_values_corrected,
                         unsigned int[::1] indices_2_BH):
    """
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
    if method == "genome":
        # was uint32, but uint16 is sufficient for STRING v11, not using it for the foreground due to potential redundancy
        # or for "compare_samples" for the same reason --> keep the same
        funcEnum_count_background = np.zeros(shape=function_enumeration_len, dtype=np.dtype("uint32"))
        p_values = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
        p_values_corrected = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
        blacklisted_terms_bool_arr_temp = blacklisted_terms_bool_arr.copy()
        cond_multitest = np.zeros(function_enumeration_len, dtype=bool)
        cond_filter = np.ones(function_enumeration_len, dtype=bool)
        cond_PMIDs = np.zeros(function_enumeration_len, dtype=bool)
        cond_terms_reduced_with_ontology = np.zeros(function_enumeration_len, dtype=bool)
        # 11
        return funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, foreground_ids_arr_of_string, cond_filter, cond_PMIDs
    elif method == "characterize_foreground":
        # 2
        return funcEnum_count_foreground, foreground_ids_arr_of_string
    elif method == "compare_samples":
        funcEnum_count_background = np.zeros(shape=function_enumeration_len, dtype=np.dtype("uint32"))
        p_values = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
        p_values_corrected = np.ones(shape=function_enumeration_len, dtype=np.dtype("float64"))
        blacklisted_terms_bool_arr_temp = blacklisted_terms_bool_arr.copy()
        cond_multitest = np.zeros(function_enumeration_len, dtype=bool)
        cond_filter = np.ones(function_enumeration_len, dtype=bool)
        cond_PMIDs = np.zeros(function_enumeration_len, dtype=bool)
        cond_terms_reduced_with_ontology = np.zeros(function_enumeration_len, dtype=bool)
        background_ids_arr_of_string = np.empty(shape=(function_enumeration_len,), dtype=object)
        # 12
        return foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs
    else:
        raise NotImplementedError

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


def run_characterize_foreground_cy(protein_ans, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, low_memory=False):
    """
    get_preloaded_objects_for_single_analysis --> funcEnum_count_foreground, foreground_ids_arr_of_string
    get_static_preloaded_objects --> year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count_dict, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict
    """
    if not low_memory:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count, taxid_2_funcEnum_index_2_associations, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects
    else: # missing: description_arr, category_arr, ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects

    foreground_n = len(protein_ans)
    funcEnum_count_foreground, foreground_ids_arr_of_string = preloaded_objects_per_analysis

    ## count foreground
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(protein_ans.tolist(), dict_2_array=True)
    for ENSP in (ENSP for ENSP in protein_ans if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count_foreground)

    ## limit to given entity types
    limit_2_entity_type = args_dict["limit_2_entity_type"]
    if limit_2_entity_type is not None:
        cond_limit_2_entity_type = np.zeros(function_enumeration_len, dtype=bool)
        for cond_name in ["cond_" + etype[1:] for etype in limit_2_entity_type.split(";")]:
            try:
                cond_limit_2_entity_type |= etype_cond_dict[cond_name] # add other etypes
            except KeyError: # user provided etype can be mistyped of non-existent
                pass
        # set funcEnumAssociations to zero where cond_limit_2_entity_type is False
        funcEnum_count_foreground[~cond_limit_2_entity_type] = 0

    ### calc ratio in foreground, count foreground / len(protein_ans)
    ratio_in_foreground = funcEnum_count_foreground / foreground_n

    ### Filter results
    cond_2_return = funcEnum_count_foreground > 0
    try:
        privileged = args_dict["privileged"]
    except KeyError:
        privileged = False
    if not privileged:
        # remove KEGG unless privileged
        cond_kegg = etype_cond_dict["cond_52"]
        cond_2_return = cond_2_return & ~cond_kegg

    ### get foregroundIDs
    funcEnum_indices_for_foregroundIDs = indices_arr[cond_2_return]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_foregroundIDs, foreground_ids_arr_of_string)

    ### concatenate results
    if not low_memory:
        df_2_return = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "term": functionalterm_arr[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "category": category_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "description": description_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view()})
    else:
        df_2_return = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "ratio_in_foreground": ratio_in_foreground[cond_2_return].view(),
                                    "term": functionalterm_arr[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "funcEnum": indices_arr[cond_2_return].view()})
        df_2_return["category"] = df_2_return["etype"].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return["description"] = df_2_return["funcEnum"].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])
    return df_2_return[variables.cols_sort_order_charcterize]

def run_compare_samples_cy(protein_ans_fg, protein_ans_bg, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, low_memory=False):
    if not low_memory:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects
    else: # missing: description_arr, category_arr, ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects
    foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs = preloaded_objects_per_analysis

    foreground_n = len(protein_ans_fg)
    background_n = len(protein_ans_bg)
    ## count foreground
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(protein_ans_fg.tolist() + protein_ans_bg.tolist(), dict_2_array=True) # previously ENSP_2_funcEnumAssociations now ENSP_2_functionEnumArray_dict
    for ENSP in (ENSP for ENSP in protein_ans_fg if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count_foreground)
    ## count background
    for ENSP in (ENSP for ENSP in protein_ans_bg if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count_background)

    ## limit to given entity types
    limit_2_entity_type = args_dict["limit_2_entity_type"]
    if limit_2_entity_type is not None:
        cond_limit_2_entity_type = np.zeros(function_enumeration_len, dtype=bool)
        for cond_name in ["cond_" + etype[1:] for etype in limit_2_entity_type.split(";")]:
            try:
                cond_limit_2_entity_type |= etype_cond_dict[cond_name] # add other etypes
            except KeyError: # user provided etype can be mistyped of non-existent
                pass
        # set funcEnumAssociations to zero where cond_limit_2_entity_type is False
        funcEnum_count_foreground[~cond_limit_2_entity_type] = 0

    ### calculate p-values and get bool array for multiple testing
    cond_multitest = calc_pvalues(funcEnum_count_foreground, funcEnum_count_background, foreground_n, background_n, p_values, cond_multitest)

    ### multiple testing per entity type, save results preformed p_values_corrected
    for etype_name, cond_etype in etype_cond_dict.items():
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

    ### FILTER
    FDR_cutoff = args_dict["FDR_cutoff"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    filter_PMID_top_n = args_dict["filter_PMID_top_n"]
    filter_parents = args_dict["filter_parents"]

    if FDR_cutoff is not None:
        cond_filter = p_values_corrected <= FDR_cutoff

    if filter_foreground_count_one is True:  # remove terms without only one annotation
        cond_filter &= funcEnum_count_foreground > 1
    else: # remove terms without any annotation
        cond_filter &= funcEnum_count_foreground > 0

    if filter_PMID_top_n is not None:
        cond_PMID_2_filter = cond_filter & etype_cond_dict["cond_56"] # -56
        df_PMID = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_PMID_2_filter].view(),
                                "year": year_arr[cond_PMID_2_filter].view(),
                                "p_value": p_values[cond_PMID_2_filter].view(),
                                "FDR": p_values_corrected[cond_PMID_2_filter].view(),
                                "indices_arr": indices_arr[cond_PMID_2_filter].view()})
        indices_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])["indices_arr"].values[:filter_PMID_top_n]
        for index_ in indices_PMID:
            cond_PMIDs[index_] = True
    else: # since no filtering use all PMIDs
        cond_PMIDs = cond_filter & etype_cond_dict["cond_56"]

    ### get foregroundIDs for
    ##  - indices_PMID -56
    ##  - cond_etypes_with_ontology & cond_filter {-21, -22, -23, -51, -57}
    ##  - cond_etypes_rem_foreground_ids -52, -53, -54, -55
    cond_etypes_with_ontology_filtered = cond_etypes_with_ontology & cond_filter # {-21, -22, -23, -51, -57}
    cond_etypes_rem_foreground_ids_filtered = cond_etypes_rem_foreground_ids & cond_filter # remaining etypes -52, -53, -54, -55
    cond_IDs_2_query = cond_PMIDs | cond_etypes_with_ontology_filtered | cond_etypes_rem_foreground_ids_filtered
    ### get foreground IDs of relevant subset --> array for entire data set
    funcEnum_indices_for_IDs = indices_arr[cond_IDs_2_query]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_fg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, foreground_ids_arr_of_string)
    background_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_bg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, background_ids_arr_of_string)

    ### filter etypes with ontologies --> cond_terms_reduced_with_ontology
    df_with_ontology = pd.DataFrame({"term_enum": indices_arr[cond_etypes_with_ontology_filtered].view(),
                                     "foreground_ids": foreground_ids_arr_of_string[cond_etypes_with_ontology_filtered].view(),
                                     "hierarchical_level": hierlevel_arr[cond_etypes_with_ontology_filtered].view(),
                                     "p_value": p_values[cond_etypes_with_ontology_filtered].view(),
                                     "foreground_count": funcEnum_count_foreground[cond_etypes_with_ontology_filtered].view(),
                                     "etype": entitytype_arr[cond_etypes_with_ontology_filtered].view()})

    if filter_parents: # only for etypes with ontology, but since foreground IDs needed get them for all
        ### modifies cond_terms_reduced_with_ontology inplace
        filter_parents_if_same_foreground(blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, lineage_dict_enum, df_with_ontology)
    else: # since no filtering done use all etypes with ontology
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
                                    "background_ids": background_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view()})
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
                                    "background_ids": background_ids_arr_of_string[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view(),
                                    "funcEnum": indices_arr[cond_2_return].view()})
        df_2_return["category"] = df_2_return["etype"].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return["description"] = df_2_return["funcEnum"].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])

    df_2_return["foreground_n"] = foreground_n
    df_2_return["background_n"] = background_n
    return df_2_return[variables.cols_sort_order_compare_samples]

def run_genome_cy(taxid, protein_ans, background_n, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, low_memory=False, debug=False):
    if not low_memory:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, ENSP_2_functionEnumArray_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects
    else:
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict = static_preloaded_objects
    funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, foreground_ids_arr_of_string, cond_filter, cond_PMIDs = preloaded_objects_per_analysis
    foreground_n = len(protein_ans)
    ## count background
    if not low_memory:
        funcEnum_index_2_associations = taxid_2_tuple_funcEnum_index_2_associations_counts[taxid]
        index_positions_arr, counts_arr = funcEnum_index_2_associations
        create_funcEnum_count_background_v5(funcEnum_count_background, index_positions_arr, counts_arr)# v4 v5
    else:
        background_counts_list = query.get_background_count_array(taxid)
        funcEnum_index_2_associations = np.asarray(background_counts_list, dtype=np.dtype("uint32"))
        funcEnum_index_2_associations.flags.writeable = False
        create_funcEnum_count_background_v2(funcEnum_count_background, funcEnum_index_2_associations)

    ## count foreground
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(protein_ans, dict_2_array=True) # previously ENSP_2_funcEnumAssociations now ENSP_2_functionEnumArray_dict
    for ENSP in (ENSP for ENSP in protein_ans if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count_foreground)

    ## limit to given entity types
    limit_2_entity_type = args_dict["limit_2_entity_type"]
    if limit_2_entity_type is not None:
        cond_limit_2_entity_type = np.zeros(function_enumeration_len, dtype=bool)
        for cond_name in ["cond_" + etype[1:] for etype in limit_2_entity_type.split(";")]:
            try:
                cond_limit_2_entity_type |= etype_cond_dict[cond_name] # add other etypes
            except KeyError: # user provided etype can be mistyped of non-existent
                pass
        # set funcEnumAssociations to zero where cond_limit_2_entity_type is False
        funcEnum_count_foreground[~cond_limit_2_entity_type] = 0

    ### calculate p-values and get bool array for multiple testing
    cond_multitest = calc_pvalues(funcEnum_count_foreground, funcEnum_count_background, foreground_n, background_n, p_values, cond_multitest)
    ### multiple testing per entity type, save results preformed p_values_corrected
    for etype_name, cond_etype in etype_cond_dict.items():
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

    ### FILTER
    FDR_cutoff = args_dict["FDR_cutoff"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    filter_PMID_top_n = args_dict["filter_PMID_top_n"]
    filter_parents = args_dict["filter_parents"]
    # if FDR_cutoff is not None:
    #     cond_filter = p_values_corrected <= FDR_cutoff
    # elif filter_foreground_count_one is not None and FDR_cutoff is None:
    #     cond_filter = funcEnum_count_foreground > 1
    if FDR_cutoff is not None:
        cond_filter = p_values_corrected <= FDR_cutoff

    if filter_foreground_count_one is True:  # remove terms without only one annotation
        cond_filter &= funcEnum_count_foreground > 1
    else: # remove terms without any annotation
        cond_filter &= funcEnum_count_foreground > 0

    if filter_PMID_top_n is not None:
        cond_PMID_2_filter = cond_filter & etype_cond_dict["cond_56"] # -56
        df_PMID = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_PMID_2_filter].view(),
                                "year": year_arr[cond_PMID_2_filter].view(),
                                "p_value": p_values[cond_PMID_2_filter].view(),
                                "FDR": p_values_corrected[cond_PMID_2_filter].view(),
                                "indices_arr": indices_arr[cond_PMID_2_filter].view()})
        indices_PMID = df_PMID.sort_values(["FDR", "year", "p_value", "foreground_count"], ascending=[True, False, True, False])["indices_arr"].values[:filter_PMID_top_n]
        for index_ in indices_PMID:
            cond_PMIDs[index_] = True
    else: # since no filtering use all PMIDs
        cond_PMIDs = cond_filter & etype_cond_dict["cond_56"]
    cond_etypes_with_ontology_filtered = cond_etypes_with_ontology & cond_filter # cond_etypes_with_ontology {-21, -22, -23, -51, -57}
    cond_etypes_rem_foreground_ids_filtered = cond_etypes_rem_foreground_ids & cond_filter # remaining etypes cond_etypes_rem_foreground_ids -52, -53, -54, -55
    cond_foregroundIDs_2_query = cond_PMIDs | cond_etypes_with_ontology_filtered | cond_etypes_rem_foreground_ids_filtered # indices_PMID -56
    ### get foreground IDs of relevant subset --> array for entire data set
    funcEnum_indices_for_foregroundIDs = indices_arr[cond_foregroundIDs_2_query]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_foregroundIDs, foreground_ids_arr_of_string)

    ### modifies cond_terms_reduced_with_ontology inplace
    if filter_parents:
        df_with_ontology = pd.DataFrame({"term_enum": indices_arr[cond_etypes_with_ontology_filtered].view(),
                             "foreground_ids": foreground_ids_arr_of_string[cond_etypes_with_ontology_filtered].view(),
                             "hierarchical_level": hierlevel_arr[cond_etypes_with_ontology_filtered].view(),
                             "p_value": p_values[cond_etypes_with_ontology_filtered].view(),
                             "foreground_count": funcEnum_count_foreground[cond_etypes_with_ontology_filtered].view(),
                             "etype": entitytype_arr[cond_etypes_with_ontology_filtered].view()})
        filter_parents_if_same_foreground(blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, lineage_dict_enum, df_with_ontology)
    else: # since no filtering done use all etypes with ontology
        cond_terms_reduced_with_ontology = cond_filter & cond_etypes_with_ontology

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
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view()})
    else:
        df_2_return = pd.DataFrame({"term": functionalterm_arr[cond_2_return].view(),
                                    "hierarchical_level": hierlevel_arr[cond_2_return].view(),
                                    "p_value": p_values[cond_2_return].view(),
                                    "FDR": p_values_corrected[cond_2_return].view(),
                                    "etype": entitytype_arr[cond_2_return].view(),
                                    "foreground_count": funcEnum_count_foreground[cond_2_return].view(),
                                    "background_count": funcEnum_count_background[cond_2_return].view(),
                                    "foreground_ids": foreground_ids_arr_of_string[cond_2_return].view(),
                                    "year": year_arr[cond_2_return].view(),
                                    "funcEnum": indices_arr[cond_2_return].view()})
        df_2_return["category"] = df_2_return["etype"].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return["description"] = df_2_return["funcEnum"].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])
    if taxid in kegg_taxid_2_acronym_dict:
        # alternative code
        # cond_2_return & etype_cond_dict["cond_52"] --> cond_KEGG_2_change
        # get a copy of that data and change it and concatenate with remaining results
        acronym = kegg_taxid_2_acronym_dict[taxid]
        cond = df_2_return["etype"] == -52 # KEGG
        df_2_return.loc[cond, "term"] = df_2_return.loc[cond, "term"].apply(lambda s: s.replace("map", acronym))

    cond_STRING_clusters = df_2_return["etype"] == -78 # STRING_cluters, remove taxid prefix
    df_2_return.loc[cond_STRING_clusters, "term"] = df_2_return.loc[cond_STRING_clusters, "term"].apply(lambda s: s.split("_")[1])
    return df_2_return[variables.cols_sort_order_genome]