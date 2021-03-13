# cython: language_level=3, nonecheck=True, boundscheck=False, wraparound=False, profile=False
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

import Cython
######################################
######################################
# from functools import reduce
# import math
# import pandas as pd
# from cython cimport boundscheck, wraparound, cdivision, nonecheck
# from fisher import pvalue
# cimport numpy as np
# from cython.parallel cimport prange
# import variables, query
# from collections import defaultdict
# from scipy import stats
######################################
##################################################################
##################################################################
##################################################################
import pandas as pd
import numpy as np
cimport numpy as np
ctypedef np.uint8_t uint8
from functools import reduce
import math
from cython cimport boundscheck, wraparound, cdivision
# cimport cython
from collections import defaultdict
from fisher import pvalue
import variables, query
import colnames as cn


def run_enrichment_cy(ncbi, ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=False, debug=False):
    if not low_memory:
        ENSP_2_functionEnumArray_dict, year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, etype_2_num_functions_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, goslimtype_2_cond_dict = static_preloaded_objects
    else:  # missing: ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, etype_2_num_functions_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, goslimtype_2_cond_dict = static_preloaded_objects
    foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes, over_under_int_arr, over_under_arr_of_string = preloaded_objects_per_analysis
    em = ui.enrichment_method
    foreground_n = ui.get_foreground_n()
    args_dict = ui.args_dict
    background_n = ui.get_background_n()
    protein_ans_fg = ui.get_foreground_an_set()
    taxid = args_dict["taxid"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    p_value_cutoff = args_dict["p_value_cutoff"]

    if ui.enrichment_method in {"abundance_correction", "compare_samples"}: # , "compare_groups"
        protein_ans_bg = ui.get_background_an_set()
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(ui.get_all_individual_AN(), dict_2_array=True)
    ### add protein groups to ENSP_2_functionEnumArray_dict
    ENSP_2_functionEnumArray_dict = add_protein_groups_to_ENSP_2_functionEnumArray_dict(ENSP_2_functionEnumArray_dict, ui.get_all_unique_proteinGroups())

    count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_fg, funcEnum_count_foreground)

    ### count background
    if em == "genome":
        funcEnum_index_2_associations = taxid_2_tuple_funcEnum_index_2_associations_counts[taxid]
        funcEnum_index_positions_arr, counts_arr = funcEnum_index_2_associations
        create_funcEnum_count_background_v3(funcEnum_count_background, funcEnum_index_positions_arr, counts_arr)
    elif em == "abundance_correction":
        funcEnum_count_background = count_all_term_abundance_corrected(ui, ENSP_2_functionEnumArray_dict, funcEnum_count_background)
        background_n = foreground_n
    elif em == "compare_samples":
        count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_bg, funcEnum_count_background)
    else:
        args_dict["ERROR enrichment_method"] = "The 'enrichment_method' you've provided: '{}' doesn't exist / isn't implemented.".format(args_dict["enrichment_method"])
        return args_dict

    ## limit to given entity types
    cond_limit_2_entity_type = limit_to_entity_types(args_dict["limit_2_entity_type"], function_enumeration_len, etype_cond_dict, funcEnum_count_foreground)
    limit_to_go_subset(etype_cond_dict, args_dict["go_slim_subset"], goslimtype_2_cond_dict, funcEnum_count_foreground)
    o_or_u_or_both_encoding = args_dict["o_or_u_or_both_encoding"]

    ### calculate Fisher p-values and get bool array for multiple testing

    calc_pvalues(funcEnum_count_foreground, funcEnum_count_background, foreground_n, background_n, p_values, cond_multitest, effectSizes, over_under_int_arr, o_or_u_or_both_encoding)

    ### "over/under"
    if o_or_u_or_both_encoding == 1: # overrepresented
        over_under_arr_of_string[over_under_int_arr == 1] = "o"
    elif o_or_u_or_both_encoding == 0: # both
        over_under_arr_of_string[over_under_int_arr == 1] = "o"
        over_under_arr_of_string[over_under_int_arr == 2] = "u"
    elif o_or_u_or_both_encoding == 2: # underrepresented
        over_under_arr_of_string[over_under_int_arr == 2] = "u"
    else: # check already done above
        return args_dict
    ### multiple testing per entity type, save results preformed p_values_corrected
    if args_dict["multiple_testing_per_etype"]:
        for etype_name, cond_etype in etype_cond_dict.items():
            if args_dict["multiple_testing_stringency"] == "A":
                num_total_tests = p_values[cond_etype & cond_multitest].shape[0] # sum(cond_etype & cond_multitest) is prohibitively slow!
            else:
                num_total_tests = etype_2_num_functions_dict[etype_name]
            multiple_testing_per_entity_type(cond_etype, cond_multitest, p_values, p_values_corrected, indices_arr, num_total_tests)
    else:
        cond_all = np.ones(function_enumeration_len, dtype=bool)
        if args_dict["multiple_testing_stringency"] == "A":
            num_total_tests = sum(cond_multitest)
        else:
            num_total_tests = cond_all.shape[0]
        multiple_testing_per_entity_type(cond_all, cond_multitest, p_values, p_values_corrected, indices_arr, num_total_tests)


    ### Filter stuff
    foreground_ids_arr_of_string, funcEnum_indices_for_IDs, cond_etypes_with_ontology_filtered, cond_etypes_rem_foreground_ids_filtered, cond_filter = filter_stuff(args_dict, protein_ans_fg, p_values_corrected, foreground_ids_arr_of_string, funcEnum_count_foreground, year_arr, p_values, indices_arr, ENSP_2_functionEnumArray_dict, cond_filter, etype_cond_dict, cond_PMIDs, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, over_under_int_arr)
    if debug:
        return foreground_ids_arr_of_string
    if em in {"compare_samples"}:
        background_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_bg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, background_ids_arr_of_string)

    ### filter etypes with ontologies --> cond_terms_reduced_with_ontology
    df_with_ontology = pd.DataFrame({"term_enum": indices_arr[cond_etypes_with_ontology_filtered].view(), "foreground_ids": foreground_ids_arr_of_string[cond_etypes_with_ontology_filtered].view(), "hierarchical_level": hierlevel_arr[cond_etypes_with_ontology_filtered].view(), "p_value": p_values[cond_etypes_with_ontology_filtered].view(), "foreground_count": funcEnum_count_foreground[cond_etypes_with_ontology_filtered].view(), "etype": entitytype_arr[cond_etypes_with_ontology_filtered].view()})
    if args_dict["filter_parents"]: # only for etypes with ontology, but since foreground IDs needed get them for all
        filter_parents_if_same_foreground(blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, lineage_dict_enum, df_with_ontology) # modifies cond_terms_reduced_with_ontology inplace
    else: # since no filtering done use all etypes with ontology
        cond_terms_reduced_with_ontology = cond_filter & cond_etypes_with_ontology
    ### concatenate filtered results
    cond_2_return = cond_PMIDs | cond_terms_reduced_with_ontology | cond_etypes_rem_foreground_ids_filtered

    df_2_return = pd.DataFrame({cn.term: functionalterm_arr[cond_2_return].view(),
                            cn.hierarchical_level: hierlevel_arr[cond_2_return].view(),
                            cn.p_value: p_values[cond_2_return].view(),
                            cn.FDR: p_values_corrected[cond_2_return].view(),
                            cn.category: category_arr[cond_2_return].view(),
                            cn.etype: entitytype_arr[cond_2_return].view(),
                            cn.description: description_arr[cond_2_return].view(),
                            cn.year: year_arr[cond_2_return].view(),
                            cn.FG_IDs: foreground_ids_arr_of_string[cond_2_return].view(),
                            cn.FG_count: funcEnum_count_foreground[cond_2_return].view(),
                            cn.BG_count: funcEnum_count_background[cond_2_return].view(),
                            cn.effect_size: effectSizes[cond_2_return].view(),
                            cn.over_under: over_under_arr_of_string[cond_2_return].view(),
                            cn.funcEnum: indices_arr[cond_2_return].view()})

    # cols_2_return_sort_order = cn.cols_2_return_run_enrichment_cy[:]
    cols_2_return_sort_order = list(cn.cols_2_return_run_enrichment_cy)
    if em in {"compare_samples"}:
        df_2_return[cn.BG_IDs] = background_ids_arr_of_string[cond_2_return].view()
    else:
        cols_2_return_sort_order.remove(cn.BG_IDs)
    df_2_return["s_value"] = get_s_value(df_2_return)
    # df_2_return["s_value_abs"] = df_2_return["s_value"].apply(lambda x: abs(x))
    df_2_return["s_value_abs"] = np.abs(df_2_return["s_value"])
    df_2_return = df_2_return.sort_values([cn.etype, "s_value_abs", cn.hierarchical_level, cn.year], ascending=[False, False, False, False]).reset_index(drop=True)
    df_2_return[cn.rank] = df_2_return.groupby(cn.etype)["s_value_abs"].rank(ascending=False, method="first").fillna(value=df_2_return.shape[0]).astype(int)
    if debug:
            return protein_ans_bg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, background_ids_arr_of_string, df_2_return
    df_2_return = ui.translate_primary_back_to_secondary(df_2_return)
    df_2_return[cn.FG_n] = foreground_n
    df_2_return[cn.BG_n] = background_n

    ### calc ratio in foreground, count foreground / len(protein_ans)
    df_2_return[cn.ratio_in_FG] = df_2_return[cn.FG_count] / df_2_return[cn.FG_n]
    df_2_return[cn.ratio_in_BG] = df_2_return[cn.BG_count] / df_2_return[cn.BG_n]
    if args_dict["STRING_beta"]:
        return df_2_return.rename(columns=cn.colnames_2_rename_dict_STRING_beta)[list(cn.cols_sort_order_STRING_beta)]
    elif args_dict["STRING_API"]:
        df_2_return["ncbiTaxonId"] = taxid
        df_2_return["preferredNames"] = ""
        return df_2_return.rename(columns=cn.colnames_2_rename_dict_STRING_API)[list(cn.cols_sort_order_STRING_API_genome_or_compare_samples)]
    return df_2_return[cols_2_return_sort_order]

@boundscheck(False)
@wraparound(False)
cdef calc_pvalues(unsigned int[::1] funcEnum_count_foreground,
                  unsigned int[::1] funcEnum_count_background,
                  unsigned int foreground_n,
                  unsigned int background_n,
                  double[::1] p_values,
                  cond_multitest,
                  double[::1] effectSizes,
                  unsigned int[::1] over_under_int_arr,
                  unsigned int o_or_u_or_both_encoding):
    cdef:
        int index_, foreground_count, background_count, a, b, c, d
        int len_functions = funcEnum_count_foreground.shape[0]
        dict fisher_dict = {}
        double p_val_uncorrected
        double odds_ratio

    for index_ in range(len_functions):
        foreground_count = funcEnum_count_foreground[index_]
        if foreground_count > 0:
            cond_multitest[index_] = True
            over_under_int_arr[index_] = 3 # meaningless encoding in order not to filter out things later if p_value_cutoff == 1
            if foreground_count == 1: # leave p-value set to 1, BUT DO multiple testing
                continue
            background_count = funcEnum_count_background[index_]
            a = foreground_count # number of proteins associated with given GO-term
            b = foreground_n - foreground_count # number of proteins not associated with GO-term
            c = background_count
            d = background_n - background_count
            p_val_uncorrected = fisher_dict.get((a, b, c, d), -1)
            if p_val_uncorrected == -1:
                if o_or_u_or_both_encoding == 1: # overrepresented
                    p_val_uncorrected = pvalue(a, b, c, d).right_tail
                    over_under_int_arr[index_] = 1
                elif o_or_u_or_both_encoding == 0: # both
                    p_val_uncorrected = pvalue(a, b, c, d).two_tail
                    try:
                        is_greater = (a / (a + b)) > (c / (c + d))
                        if is_greater:
                            is_greater = 1
                        else:
                            is_greater = 2
                    except ZeroDivisionError:
                        is_greater = 0 # np.nan
                    over_under_int_arr[index_] = is_greater
                elif o_or_u_or_both_encoding == 2: # underrepresented
                    p_val_uncorrected = pvalue(a, b, c, d).left_tail
                    over_under_int_arr[index_] = 2
                else:
                    p_val_uncorrected = 1
                    over_under_int_arr[index_] = 3
                fisher_dict[(a, b, c, d)] = p_val_uncorrected
            else: # write over_under but don't calc pvalue
                if o_or_u_or_both_encoding == 1: # overrepresented
                    over_under_int_arr[index_] = 1
                elif o_or_u_or_both_encoding == 0: # both
                    try:
                        is_greater = (a / (a + b)) > (c / (c + d))
                    except ZeroDivisionError:
                        is_greater = np.nan # ??? shouldn't this be 0 instead of np.nan ???
                    over_under_int_arr[index_] = is_greater
                elif o_or_u_or_both_encoding == 2: # underrepresented
                    over_under_int_arr[index_] = 2
                else:
                    over_under_int_arr[index_] = 3 # which caser is this supposed to be?
            p_values[index_] = p_val_uncorrected
            try:
                # https://stats.stackexchange.com/questions/22508/effect-size-for-fishers-exact-test
                # odds_ratio = (a * d) / (b * c) # true odds ratio
                # odds_ratio = (d / (c + d)) - (a / (a + b)) # difference in proportions
                odds_ratio = (a / (a + b)) - (c / (c + d)) # difference in proportions DBL
                # odds_ratio = (a / (a + b)) / (c / (c + d)) # from old agotool, ratio of percent in fg to percent in bg
            except ZeroDivisionError:
                odds_ratio = np.nan
            effectSizes[index_] = odds_ratio
    return 0

@boundscheck(False)
@wraparound(False)
cdef int create_funcEnum_count_background_v3(unsigned int[::1] funcEnum_count_background,
                                         const unsigned int[::1] funcEnum_index_arr, # uint32
                                         const unsigned int[::1] count_arr): # uint32
    cdef:
        int i, N = funcEnum_index_arr.shape[0]
        unsigned int index_
        unsigned short count

    for i in range(N):
        index_ = funcEnum_index_arr[i]
        count = count_arr[i]
        funcEnum_count_background[index_] = count
    return 0

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
cdef int count_terms_cy_abundance_corrected(double correction_factor,
                                        unsigned int[::1] funcEnum_associations,
                                        double[::1] funcEnum_count_float):
    cdef int N, i, k
    N = funcEnum_associations.shape[0]
    for i in range(N):
        k = funcEnum_associations[i]
        funcEnum_count_float[k] += correction_factor
    return 0

def count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans, funcEnum_count):
    for ENSP in (ENSP for ENSP in protein_ans if ENSP in ENSP_2_functionEnumArray_dict):
        funcEnumAssociations = ENSP_2_functionEnumArray_dict[ENSP]
        count_terms_cy(funcEnumAssociations, funcEnum_count)

@boundscheck(False)
@wraparound(False)
cdef int count_terms_cy(unsigned int[::1] funcEnum_associations,
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
    return 0

def collect_scores_per_term_characterize_foreground(protein_AN_list, ENSP_2_tuple_funcEnum_score_dict, funcEnums_2_include_set, score_cutoff=3):
    funcEnum_2_scores_dict = defaultdict(lambda: [])
    for protein_AN in protein_AN_list:
        funcEnum_already_counted = set()
        try:
            funcEnum_score = ENSP_2_tuple_funcEnum_score_dict[protein_AN]
        except KeyError:
            continue
        funcEnum_arr, score_arr = funcEnum_score
        len_funcEnum_arr = len(funcEnum_arr)
        for index_ in range(len_funcEnum_arr):
            funcEnum = funcEnum_arr[index_]
            if funcEnum in funcEnums_2_include_set:
                score = score_arr[index_]
                if score >= score_cutoff:
                    if funcEnum not in funcEnum_already_counted:
                        # in order to count a function only once per protein
                        funcEnum_2_scores_dict[funcEnum].append(score)
                        funcEnum_already_counted.update(set([funcEnum]))
    return funcEnum_2_scores_dict

def collect_scores_per_term(protein_AN_list, ENSP_2_tuple_funcEnum_score_dict, list_2_array=False):
    """
    ENSP_2_tuple_funcEnum_score_dict['3702.AT1G01010.1']
    (array([ 211,  252,  253], dtype=uint32),
     array([4200000, 4166357, 4195121], dtype=uint32))
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
        return {funcEnum: np.asarray(scores, dtype=np.dtype(variables.dtype_TM_score)) for funcEnum, scores in funcEnum_2_scores_dict.items()} # float64 --> uint32
    # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

def collect_scores_per_term_limit_2_inclusionTerms(protein_AN_list, ENSP_2_tuple_funcEnum_score_dict, funcEnums_2_include_set, list_2_array=False):
    """
    for a given protein: a functional term should only have a single score (not multiple as previously)
    ENSP_2_tuple_funcEnum_score_dict['3702.AT1G01010.1']
    (array([ 211,  252,  253], dtype=uint32),
     array([420000, 4166357, 4195121], dtype=uint32))
    funcEnum_2_scores_dict: key: functionEnumeration, val: list of Integer scores ( )
    """
    len_protein_AN_list = len(protein_AN_list)
    funcEnum_2_scores_dict = defaultdict(lambda: [0]*len_protein_AN_list)
    for index_protein, protein_AN in enumerate(protein_AN_list):
        try:
            funcEnum_score = ENSP_2_tuple_funcEnum_score_dict[protein_AN]
        except KeyError:
            continue
        funcEnum_arr, score_arr = funcEnum_score
        len_funcEnum_arr = len(funcEnum_arr)
        for index_ in range(len_funcEnum_arr):
            funcEnum = funcEnum_arr[index_]
            if funcEnum in funcEnums_2_include_set:
                score = score_arr[index_]
                funcEnum_2_scores_dict[funcEnum][index_protein] = score # funcEnum_2_scores_dict[funcEnum].append(score)
    if list_2_array:
        return {funcEnum: np.asarray(scores, dtype=np.dtype(variables.dtype_TM_score)) for funcEnum, scores in funcEnum_2_scores_dict.items()}
    # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

def collect_scores_per_term_abundance_corrected(ui, ENSP_2_tuple_funcEnum_score_dict, funcEnums_2_include_set, list_2_array=False):
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
                funcEnum = funcEnum_arr[index_]
                if funcEnum in funcEnums_2_include_set:
                    score = score_arr[index_]
                    funcEnum_2_scores_dict[funcEnum].append(score*correction_factor)
    if list_2_array:
        return {funcEnum: np.asarray(scores, dtype=np.dtype(variables.dtype_TM_score)) for funcEnum, scores in funcEnum_2_scores_dict.items()}
        # since concatenating np.arrays later on (for filling with zeros) produces 64 bit array anyway
    else:
        return funcEnum_2_scores_dict

@boundscheck(False)
@wraparound(False)
@cdivision(True)
cdef BenjaminiHochberg_cy(double[::1] p_values,
                         unsigned int num_total_tests,
                         double[::1] p_values_corrected,
                         unsigned int[::1] indices_2_BH):
    """
    #!!! cpdef instead of cdef for scores debugging/profiling
    ein index array mit absoluten positionen, pvals absolut und pvalscorr absolut
    p_values_2_BH, p_values_2_BH.shape[0], p_values_corrected_2_BH, indices_of_p_values_2_BH)
    :param p_values: unsorted array of float
    :param num_total_tests: Integer (number of all possible tests within etype/category, regardless of input)
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

def map_funcEnum_2_ENSPs(protein_ans_list, ENSP_2_functionEnumArray_dict, funcEnum_indices, foreground_ids_arr_of_string):
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
        foreground_ids_arr_of_string[funcEnum] = ";".join(sorted(set(ENSPs))) # needs to be sorted otherwise grouping incorrect later on
    return foreground_ids_arr_of_string

def get_preloaded_objects_for_single_analysis(blacklisted_terms_bool_arr, function_enumeration_len=6834675):
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
    over_under_int_arr = np.zeros(function_enumeration_len, dtype=np.dtype("uint32")) # encoding of 1: "overrepresented", 2: "underrepresented", 0: "NaN"
    over_under_arr_of_string = np.empty(function_enumeration_len, np.dtype("U1"))
    return foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes, over_under_int_arr, over_under_arr_of_string

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

def multiple_testing_per_entity_type(cond_etype, cond_multitest, p_values, p_values_corrected, indices_arr, num_total_tests):
    # select indices for given entity type and if multiple testing needs to be applied
    cond = cond_etype & cond_multitest
    # select p_values for BenjaminiHochberg
    p_values_2_BH = p_values[cond]
    # previously: num_total_tests = p_values_2_BH.shape[0]
    # select indices for BH
    indices_2_BH = indices_arr[cond]
    # sort p_values and remember indices sort order
    p_values_2_BH_sort_order = np.argsort(p_values_2_BH) # index positions of a reduced set
    indices_2_BH_of_superset = indices_2_BH[p_values_2_BH_sort_order]
    BenjaminiHochberg_cy(p_values, num_total_tests, p_values_corrected, indices_2_BH_of_superset)

def get_s_value(df, p_value_cutoff=0.05, KS_stat_cutoff=0.1, diff_proportions_cutoff=0.1):
    """
    calculate 's-value' type statistic in order to rank based on a combination of p-value and effect size
    for etypes -20, -25, and -26 (GOCC, BTO, and DOID) --> Common Language Effect Size
    for other etypes difference in ratios
    justification for cles_cutoff --> Kerby (https://doi.org/10.2466%2F11.IT.3.1) if the null is true the CLES is 50%
    justification for diff_proportions_cutoff --> unsure how to justify from lit. need be smaller than cles_cutoff
    --> changed from cles to KS_stat
    """
    min_pval = df[cn.p_value][df[cn.p_value] > 0].min()
    df["p_value_minlog"] = df[cn.p_value].apply(log_take_min_if_zero, args=(min_pval, ))
    df[cn.s_value] = 0.0
    # cond_scores = df[cn.etype].isin([-20, -25, -26])
    # p_value_cutoff = -1 * math.log10(p_value_cutoff) # test for values smaller than 0
    df[cn.s_value] = df["p_value_minlog"] * df[cn.effect_size]
    # df = df.drop(columns=["p_value_minlog"])
    return df[cn.s_value]

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
        return cond_limit_2_entity_type # return bool arr of locations that should NOT be tested
    else:
        return np.ones(function_enumeration_len, dtype=bool)

def limit_to_go_subset(etype_cond_dict, go_slim_subset, goslimtype_2_cond_dict, funcEnum_count_foreground):
    if go_slim_subset is None:
        return funcEnum_count_foreground
    cond_GO_etypes = etype_cond_dict["cond_21"] | etype_cond_dict["cond_22"] | etype_cond_dict["cond_23"]
    cond = cond_GO_etypes != goslimtype_2_cond_dict[go_slim_subset] # select all GO terms that are not slim
    # set these to count 0
    funcEnum_count_foreground[cond] = 0
    return funcEnum_count_foreground

def add_funcEnums_2_dict(protein_ans_fg, ENSP_2_functionEnumArray_dict, ENSP_2_tuple_funcEnum_score_dict):
    ### add Protein 2 functionEnum info for JensenLabScore data to get foregroundIDs in DF
    for protein in protein_ans_fg:
        try: # sort is probably not necessary # potential speedup removing the sorting
            ENSP_2_functionEnumArray_dict[protein] = np.sort(np.concatenate((ENSP_2_tuple_funcEnum_score_dict[protein][0], ENSP_2_functionEnumArray_dict[protein])))
        except KeyError:
            pass # print("protein {} not in ENSP_2_tuple_funcEnum_score_dict".format(protein)) # --> simply not annotated with anything from textmining

def add_funcEnums_2_dict_CSC(protein_AN_set, ENSP_2_functionEnumArray_dict, ENSP_2_rowIndex_dict, CSR_ENSPencoding_2_FuncEnum):
    """
    rowIndex = ENSP_2_rowIndex_dict["128UP_DROME"]
    CSR_ENSPencoding_2_FuncEnum[rowIndex].indices # --> FunEnums_array == ENSP_2_tuple_funcEnum_score_dict["128UP_DROME"][0]
    CSR_ENSPencoding_2_FuncEnum[rowIndex].data # --> Scores_array == ENSP_2_tuple_funcEnum_score_dict[ensp][1]
    """
    for protein in protein_AN_set:
        try:
            rowIndex = ENSP_2_rowIndex_dict[protein]
        except KeyError:
            continue
        funcEnum_array = CSR_ENSPencoding_2_FuncEnum[rowIndex].indices
        ENSP_2_functionEnumArray_dict[protein] = np.sort(np.concatenate((funcEnum_array, ENSP_2_functionEnumArray_dict[protein])))

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

def filter_stuff(args_dict, protein_ans_fg, p_values_corrected, foreground_ids_arr_of_string, funcEnum_count_foreground, year_arr, p_values, indices_arr, ENSP_2_functionEnumArray_dict, cond_filter, etype_cond_dict, cond_PMIDs, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, over_under_int_arr):
    FDR_cutoff, p_value_cutoff = args_dict["FDR_cutoff"], args_dict["p_value_cutoff"]
    cond_filter = (p_values_corrected <= FDR_cutoff) & (p_values <= p_value_cutoff)
    ### remove terms with only a single annotation
    if args_dict["filter_foreground_count_one"] is True:
        cond_filter &= funcEnum_count_foreground > 1
    else:  # remove terms without any annotation
        cond_filter &= funcEnum_count_foreground > 0

    ### overrepresented/underrepresented/both
    o_or_u_or_both_encoding = args_dict["o_or_u_or_both_encoding"]
    if o_or_u_or_both_encoding == 1: # overrepresented
        cond_o_or_u_or_both = over_under_int_arr == 1
    elif o_or_u_or_both_encoding == 2: # underrepresented
        cond_o_or_u_or_both = over_under_int_arr == 2
    elif o_or_u_or_both_encoding == 0: # both
        cond_o_or_u_or_both = over_under_int_arr > 0
    else:
        pass # should not happen
    cond_filter &= cond_o_or_u_or_both
    filter_PMID_top_n = args_dict["filter_PMID_top_n"]
    if filter_PMID_top_n is not None:
        cond_PMID_2_filter = cond_filter & etype_cond_dict["cond_56"]  # -56
        df_PMID = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_PMID_2_filter].view(), "year": year_arr[cond_PMID_2_filter].view(), "p_value": p_values[cond_PMID_2_filter].view(), "FDR": p_values_corrected[cond_PMID_2_filter].view(), "indices_arr": indices_arr[cond_PMID_2_filter].view()})
        indices_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])["indices_arr"].values[:filter_PMID_top_n]
        for index_ in indices_PMID:
            cond_PMIDs[index_] = True
    else:  # since no filtering use all PMIDs
        cond_PMIDs = cond_filter & etype_cond_dict["cond_56"]
    cond_etypes_with_ontology_filtered = cond_etypes_with_ontology & cond_filter  # {-21, -22, -23, -51, -57}
    # entity_types_with_ontology = {-20, -21, -22, -23, -25, -26, -51, -57} # Interpro has ontology, but omitted here to turn off filter_parents functionality
    cond_etypes_rem_foreground_ids_filtered = cond_etypes_rem_foreground_ids & cond_filter  # remaining etypes -52, -53, -54, -55
    cond_IDs_2_query = (cond_PMIDs | cond_etypes_with_ontology_filtered | cond_etypes_rem_foreground_ids_filtered)
    ### get foreground IDs of relevant subset --> array for entire data set
    ## exclude TextMining KS functionEnumerations since these are probably not very informative and we need performance --> don't exclude
#     if not KS_etypes_FG_IDs:
#         cond_IDs_2_query = cond_IDs_2_query & ~cond_KS_etypes # commented on purpose since STRING needs these
    funcEnum_indices_for_IDs = indices_arr[cond_IDs_2_query]
    foreground_ids_arr_of_string = map_funcEnum_2_ENSPs(protein_ans_fg, ENSP_2_functionEnumArray_dict, funcEnum_indices_for_IDs, foreground_ids_arr_of_string)
#     if not KS_etypes_FG_IDs:
#         foreground_ids_arr_of_string[cond_KS_etypes] = "" # commented out for STRING
    return foreground_ids_arr_of_string, funcEnum_indices_for_IDs, cond_etypes_with_ontology_filtered, cond_etypes_rem_foreground_ids_filtered, cond_filter

def run_characterize_foreground_cy(ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=False):
    if not low_memory:
        ENSP_2_functionEnumArray_dict, year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, etype_2_num_functions_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, goslimtype_2_cond_dict = static_preloaded_objects
    else:  # missing: ENSP_2_functionEnumArray_dict
        year_arr, hierlevel_arr, entitytype_arr, functionalterm_arr, indices_arr, description_arr, category_arr, etype_2_minmax_funcEnum, function_enumeration_len, etype_cond_dict, etype_2_num_functions_dict, taxid_2_proteome_count, taxid_2_tuple_funcEnum_index_2_associations_counts, lineage_dict_enum, blacklisted_terms_bool_arr, cond_etypes_with_ontology, cond_etypes_rem_foreground_ids, kegg_taxid_2_acronym_dict, goslimtype_2_cond_dict = static_preloaded_objects
    foreground_ids_arr_of_string, background_ids_arr_of_string, funcEnum_count_foreground, funcEnum_count_background, p_values, p_values_corrected, cond_multitest, blacklisted_terms_bool_arr_temp, cond_terms_reduced_with_ontology, cond_filter, cond_PMIDs, effectSizes, over_under_int_arr, over_under_arr_of_string = preloaded_objects_per_analysis
    em = ui.enrichment_method
    foreground_n = ui.get_foreground_n()
    args_dict = ui.args_dict
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]

    protein_ans_fg = ui.get_foreground_an_set()
    if low_memory:
        ENSP_2_functionEnumArray_dict = query.get_functionEnumArray_from_proteins(ui.get_all_individual_AN(), dict_2_array=True)
    ### add protein groups to ENSP_2_functionEnumArray_dict
    ENSP_2_functionEnumArray_dict = add_protein_groups_to_ENSP_2_functionEnumArray_dict(ENSP_2_functionEnumArray_dict, ui.get_all_unique_proteinGroups())

    ## count foreground
    count_all_terms(ENSP_2_functionEnumArray_dict, protein_ans_fg, funcEnum_count_foreground)

    ## limit to given entity types
    cond_limit_2_entity_type = limit_to_entity_types(args_dict["limit_2_entity_type"], function_enumeration_len, etype_cond_dict, funcEnum_count_foreground)
    limit_to_go_subset(etype_cond_dict, args_dict["go_slim_subset"], goslimtype_2_cond_dict, funcEnum_count_foreground)

    ### calc ratio in foreground, count foreground / len(protein_ans)
    ratio_in_foreground = funcEnum_count_foreground / foreground_n

    ### concatenate filtered results
    if filter_foreground_count_one:
        cond_2_return = funcEnum_count_foreground > 1
    else:
        cond_2_return = funcEnum_count_foreground >= 1

    ### limit PMID results
    filter_PMID_top_n = args_dict["filter_PMID_top_n"]
    if filter_PMID_top_n is not None:
        cond_PMID_2_filter = cond_2_return & etype_cond_dict["cond_56"]
        df_PMID = pd.DataFrame({"foreground_count": funcEnum_count_foreground[cond_PMID_2_filter].view(), "year": year_arr[cond_PMID_2_filter].view(), "indices_arr": indices_arr[cond_PMID_2_filter].view()})
        indices_PMID = df_PMID.sort_values(["foreground_count", "year"], ascending=[False, False])["indices_arr"].values[:filter_PMID_top_n]
        # set all PMIDs to False and then include only those that were selected
        cond_2_return[etype_cond_dict["cond_56"]] = False
        for index_ in indices_PMID:
            cond_2_return[index_] = True
    cond_2_return[blacklisted_terms_bool_arr > 0] = False

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
        df_2_return = pd.DataFrame({cn.term: functionalterm_arr[cond_2_return].view(),
                                    cn.hierarchical_level: hierlevel_arr[cond_2_return].view(),
                                    cn.category: category_arr[cond_2_return].view(),
                                    cn.etype: entitytype_arr[cond_2_return].view(),
                                    cn.description: description_arr[cond_2_return].view(),
                                    cn.year: year_arr[cond_2_return].view(),
                                    cn.ratio_in_FG: ratio_in_foreground[cond_2_return].view(),
                                    cn.FG_IDs: foreground_ids_arr_of_string[cond_2_return].view(),
                                    cn.FG_count: funcEnum_count_foreground[cond_2_return].view()})
    else:
        df_2_return = pd.DataFrame({cn.term: functionalterm_arr[cond_2_return].view(),
                                    cn.hierarchical_level: hierlevel_arr[cond_2_return].view(),
                                    cn.etype: entitytype_arr[cond_2_return].view(),
                                    cn.year: year_arr[cond_2_return].view(),
                                    cn.ratio_in_FG: ratio_in_foreground[cond_2_return].view(),
                                    cn.FG_IDs: foreground_ids_arr_of_string[cond_2_return].view(),
                                    cn.FG_count: funcEnum_count_foreground[cond_2_return].view(),
                                    cn.funcEnum: indices_arr[cond_2_return].view()})
        df_2_return[cn.category] = df_2_return[cn.etype].apply(lambda etype: variables.entityType_2_functionType_dict[etype])
        funcEnum_2_description_dict = query.get_function_description_from_funcEnum(indices_arr[cond_2_return].tolist())
        df_2_return[cn.description] = df_2_return[cn.funcEnum].apply(lambda funcEnum: funcEnum_2_description_dict[funcEnum])
    df_2_return = ui.translate_primary_back_to_secondary(df_2_return)
    df_2_return[cn.FG_n] = foreground_n
    ### rank everything correctly except PMIDs, "year"-column will only affect PMIDs
    df_2_return = df_2_return.sort_values([cn.etype, cn.year, cn.FG_count], ascending=[False, False, False]).reset_index(drop=True)
    # debug delete me --> df_2_return = df_2_return.sort_values([cn.etype, "s_value_abs", cn.hierarchical_level, cn.year], ascending=[False, False, False, False])

    if args_dict["STRING_beta"]:
        # return df_2_return[list(cn.cols_sort_order_characterize_foreground_STRING_beta)].rename(columns=cn.colnames_2_rename_dict_STRING_beta)
        return df_2_return.rename(columns=cn.colnames_2_rename_dict_STRING_beta)[list(cn.cols_sort_order_characterize_foreground_STRING_beta)]
    elif args_dict["STRING_API"]:
        df_2_return["ncbiTaxonId"] = args_dict["taxid"]
        df_2_return["preferredNames"] = ""
        return df_2_return.rename(columns=cn.colnames_2_rename_dict_STRING_API)[list(cn.cols_sort_order_STRING_API_functional_annotation)]
    cond_PMIDs = df_2_return[cn.etype] == -56
    df_2_return.loc[~cond_PMIDs, cn.rank] = df_2_return[~cond_PMIDs].groupby(cn.etype)[cn.FG_count].rank(ascending=False, method="first").fillna(value=df_2_return.shape[0])
    df_2_return.loc[cond_PMIDs, cn.rank] = df_2_return[cond_PMIDs].groupby(cn.etype)[cn.year].rank(ascending=False, method="first").fillna(value=df_2_return.shape[0])
    df_2_return[cn.rank] = df_2_return[cn.rank].astype(int)
    return df_2_return[list(cn.cols_2_return_run_characterize_foreground_cy)]