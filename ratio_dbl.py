#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import defaultdict

# def count_terms(geneset, assoc, obo_dag):
#     """count the number of terms in the study group
#     """
#     term_cnt = defaultdict(int)
#     for gene in (g for g in geneset if g in assoc):
#         for x in assoc[gene]:
#             if x in obo_dag:
#                 term_cnt[obo_dag[x].id] += 1
#     return term_cnt

def count_terms(ans_set, assoc, obo_dag):
    """
    count the number of terms in the study group
    """
    term_cnt = defaultdict(int)
    for an in (acnum for acnum in ans_set if acnum in assoc):
        for goterm in assoc[an]:
            if goterm in obo_dag:
                term_cnt[obo_dag[goterm].id] += 1
    return term_cnt

def count_terms_abundance_corrected(ui, assoc_dict, obo_dag):
    """
    produce abundance corrected counts of GO-terms of background frequency
    round floats to nearest integer
    UserInput-object includes ANs of sample, and background as well as abundance data
    :param ui: UserInput-object
    :param assoc_dict:  Dict with key=AN, val=set of GO-terms
    :param obo_dag: Dict with additional methods
    :param binom: Boolean
    :return: DefaultDict(Float)
    """
    term_cnt = defaultdict(float)
    for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
        for an in ans: # for every AccessionNumber
            if assoc_dict.has_key(an):
            # assoc_dict contains GO-terms and their parents (due to obo_dag.update_association)
            # for all ANs of goa_ref UniProt
            # if AN not in dict, no GO-term associated
                # goterms = get_goterms_from_an(an, include_parents=True)
                goterms = assoc_dict[an]
                for goterm in goterms:
                    if goterm in obo_dag:
                        term_cnt[obo_dag[goterm].id] += weight_fac
    for goterm in term_cnt:
        term_cnt[goterm] = int(round(term_cnt[goterm]))
    return term_cnt




def is_ratio_different(min_ratio, study_go, study_n, pop_go, pop_n):
    """
    check if the ratio go/n is different between the study group and
    the population
    """
    if min_ratio is None:
        return True
    s = float(study_go) / study_n
    p = float(pop_go) / pop_n
    if s > p:
        return s / p > min_ratio
    return p / s > min_ratio
