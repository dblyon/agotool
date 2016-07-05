from collections import defaultdict


def get_goids_from_proteinGroup(proteinGroup, assoc_dict):
    """
    e.g. proteinGroup 'A3CP09;ssan_c_1_1478;EGQ25042.1;EGQ22065.1'
    assoc_dict {'P28482': {u'GO:0000165',u'GO:0000166',u'GO:0000186',u'GO:0000187',u'GO:0000189'}}
    :param proteinGroup: String(SemicolonSepAN)
    :param assoc_dict: Dict(key: AN, val: SetOfGOid)
    :return: SetOfGOid
    """
    goid_set = set()
    ans_list = proteinGroup.split(";")
    for an in ans_list:
        try:
            goid_set_temp = assoc_dict[an]
        except KeyError:
            continue
        goid_set.update(goid_set_temp)
    return goid_set, ans_list

def count_terms_proteinGroup(ui, assoc_dict, obo_dag, sample_or_background):
    """
    GOid2ANs_dict: key: GOid, val: ListOfAN
    GO2NumProtGroups_dict: key: GOid, val: Int(number of proteinGroups associated with GOterm)
    redundant count e.g. 8 out of 10 samples --> study_count = 8
    study_n = 10 (1 unique proteinGroup * 10 for study_n)
    """
    # counts proteinGroup only once (as one AN) but uses all GOterms associated with it
    GOid2RedundantNumProtGroups_dict = defaultdict(int) # key: String(GOid), val: Int(redundant Number of proteinGroups,
    # e.g. if 8 out of 10 samples have proteinGroup --> 8)
    GOid2ANs_dict = {} # key: GOid, val: ListOfANs (all ANs associated with GOterm)
    GOid2UniqueNumProtGroups_dict = {} # key: String(GOid), val: Int(NON-redundant Number of proteinGroups,
    # e.g. if 8 out of 10 samples have proteinGroup --> 1)
    if sample_or_background == "sample":
        proteinGroup_list = ui.get_sample_an().dropna().tolist()
        # redundant list
    else:
        proteinGroup_list = ui.get_background_an().dropna().tolist()
    for protGroup in proteinGroup_list:
        goid_set, ans_list = get_goids_from_proteinGroup(protGroup, assoc_dict)
        for goid in goid_set:
            if goid in obo_dag:
                if goid not in GOid2RedundantNumProtGroups_dict:
                    GOid2RedundantNumProtGroups_dict[goid] = 1
                    GOid2ANs_dict[goid] = set(ans_list)
                    GOid2UniqueNumProtGroups_dict[goid] = [protGroup]
                else:
                    GOid2RedundantNumProtGroups_dict[goid] += 1
                    GOid2ANs_dict[goid].update(ans_list)
                    GOid2UniqueNumProtGroups_dict[goid].append(protGroup)
    for key in GOid2UniqueNumProtGroups_dict:
        GOid2UniqueNumProtGroups_dict[key] = len(set(GOid2UniqueNumProtGroups_dict[key]))
    return GOid2RedundantNumProtGroups_dict, GOid2ANs_dict, GOid2UniqueNumProtGroups_dict

def count_terms_proteinGroup_KEGG(ui, assoc_dict, sample_or_background):
    """
    GOid2ANs_dict: key: GOid, val: ListOfAN
    GO2NumProtGroups_dict: key: GOid, val: Int(number of proteinGroups associated with GOterm)
    redundant count e.g. 8 out of 10 samples --> study_count = 8
    study_n = 10 (1 unique proteinGroup * 10 for study_n)

    :param ui: UserInputInstance
    :param assoc_dict: Dict(key: AN, val: ListOfString)
    :param sample_or_background: String
    :return: Tuple(Dict, Dict, Dict)
    """
    # counts proteinGroup only once (as one AN) but uses all GOterms associated with it
    GOid2RedundantNumProtGroups_dict = defaultdict(int) # key: String(GOid), val: Int(redundant Number of proteinGroups,
    # e.g. if 8 out of 10 samples have proteinGroup --> 8)
    GOid2ANs_dict = {} # key: GOid, val: ListOfANs (all ANs associated with GOterm)
    GOid2UniqueNumProtGroups_dict = {} # key: String(GOid), val: Int(NON-redundant Number of proteinGroups,
    # e.g. if 8 out of 10 samples have proteinGroup --> 1)
    if sample_or_background == "sample":
        proteinGroup_list = ui.get_sample_an().dropna().tolist()
        # redundant list
    else:
        proteinGroup_list = ui.get_background_an().dropna().tolist()
    for protGroup in proteinGroup_list:
        KEGG_set, ans_list = get_goids_from_proteinGroup(protGroup, assoc_dict)
        for goid in KEGG_set:
            if goid not in GOid2RedundantNumProtGroups_dict:
                GOid2RedundantNumProtGroups_dict[goid] = 1
                GOid2ANs_dict[goid] = set(ans_list)
                GOid2UniqueNumProtGroups_dict[goid] = [protGroup]
            else:
                GOid2RedundantNumProtGroups_dict[goid] += 1
                GOid2ANs_dict[goid].update(ans_list)
                GOid2UniqueNumProtGroups_dict[goid].append(protGroup)
    for key in GOid2UniqueNumProtGroups_dict:
        GOid2UniqueNumProtGroups_dict[key] = len(set(GOid2UniqueNumProtGroups_dict[key]))
    return GOid2RedundantNumProtGroups_dict, GOid2ANs_dict, GOid2UniqueNumProtGroups_dict

def count_terms_v2(ans_set, assoc_dict, obo_dag):
    """
    count the number of terms in the study group
    GOid2NumANs_dict: key=GOid, val=Num of occurrences
    GOid2ANs_dict: key=GOid, val=ListOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag
    :return: Tuple(dict, dict, int)
    """
    ans2count = set()
    GOid2ANs_dict = {}
    GOid2NumANs_dict = defaultdict(int)
    for an in (acnum for acnum in ans_set if acnum in assoc_dict):
        for goterm in assoc_dict[an]:
            if goterm in obo_dag:
                ans2count.update([an])
                goid = obo_dag[goterm].id
                GOid2NumANs_dict[goid] += 1
                if not goid in GOid2ANs_dict:
                    GOid2ANs_dict[goid] = set([an])
                else:
                    GOid2ANs_dict[goid].update([an])
    return GOid2NumANs_dict, GOid2ANs_dict, len(ans2count)

def count_terms_v2_KEGG(ans_set, assoc_dict):
    """
    count the number of terms in the study group
    GOid2NumANs_dict: key=GOid, val=Num of occurrences
    GOid2ANs_dict: key=GOid, val=ListOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag
    :return: Tuple(dict, dict, int)
    """
    ans2count = set()
    GOid2ANs_dict = {}
    GOid2NumANs_dict = defaultdict(int)
    for an in (acnum for acnum in ans_set if acnum in assoc_dict):
        for keggterm in assoc_dict[an]:
            ans2count.update([an])
            GOid2NumANs_dict[keggterm] += 1
            if not keggterm in GOid2ANs_dict:
                GOid2ANs_dict[keggterm] = set([an])
            else:
                GOid2ANs_dict[keggterm].update([an])
    return GOid2NumANs_dict, GOid2ANs_dict, len(ans2count)


def count_terms(ans_set, assoc_dict, obo_dag):
    """
    count the number of terms in the study group
    produces defaultsdict: key=GOid, val=Num of occurrences
    go2ans_dict: key=GOid, val=ListOfANs
    """
    go2ans_dict = {}
    term_cnt = defaultdict(int)
    for an in (acnum for acnum in ans_set if acnum in assoc_dict):
        for goterm in assoc_dict[an]:
            if goterm in obo_dag:
                term_cnt[obo_dag[goterm].id] += 1
                if not go2ans_dict.has_key(goterm):
                    go2ans_dict[goterm] = set([an])
                else:
                    go2ans_dict[goterm].update([an])
    return(term_cnt, go2ans_dict)

def get_go2ans_dict(assoc_dict):
    """
    produce dictionary with GO-ids as key and List of AccessionNumbers as value
    :param assoc_dict: Dict: key=AN, val=set of go-terms
    :return: Dict: key=GOid, val=ListOfANs
    """
    go2ans_dict = {}
    for an in assoc_dict:
        goid_list = assoc_dict[an]
        for goid in goid_list:
            if not go2ans_dict.has_key(goid):
                go2ans_dict[goid] = set([an])
            else:
                go2ans_dict[goid].update([an])
    return go2ans_dict

# def count_terms_abundance_corrected(ui, assoc_dict, obo_dag):
#     """
#     produce abundance corrected counts of GO-terms of background frequency
#     round floats to nearest integer
#     UserInput-object includes ANs of sample, and background as well as abundance data
#     produces:
#         term_cnt: key=GOid, val=Num of occurrences
#         go2ans_dict: key=GOid, val=ListOfANs
#     :param ui: UserInput-object
#     :param assoc_dict:  Dict with key=AN, val=set of GO-terms
#     :param obo_dag: Dict with additional methods
#     :return: DefaultDict(Float)
#     """
#     go2ans_dict = {}
#     term_cnt = defaultdict(float)
#     for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
#         for an in ans: # for every AccessionNumber
#             if assoc_dict.has_key(an):
#             # assoc_dict contains GO-terms and their parents (due to obo_dag.update_association)
#             # for all ANs of goa_ref UniProt
#             # if AN not in dict, no GO-term associated
#             # goterms = get_goterms_from_an(an, include_parents=True)
#                 goterms = assoc_dict[an]
#                 for goterm in goterms:
#                     if goterm in obo_dag:
#                         term_cnt[obo_dag[goterm].id] += weight_fac
#                     # else:
#                     #     pass
#                     if not go2ans_dict.has_key(goterm):
#                         go2ans_dict[goterm] = set([an]) # obo_dag[goterm].id
#                     else:
#                         go2ans_dict[goterm].update([an])
#     for goterm in term_cnt:
#         term_cnt[goterm] = int(round(term_cnt[goterm]))
#     go2ans2return = {}
#     for goterm in term_cnt:
#         count = term_cnt[goterm]
#         if count >=1:
#             go2ans2return[goterm] = go2ans_dict[goterm]
#     return(term_cnt, go2ans2return)

def count_terms_abundance_corrected(ui, assoc_dict, obo_dag):
    """
    produce abundance corrected counts of GO-terms of background frequency
    round floats to nearest integer
    UserInput-object includes ANs of sample, and background as well as abundance data
    produces:
        term_cnt: key=GOid, val=Num of occurrences
        go2ans_dict: key=GOid, val=ListOfANs
    :param ui: UserInput-object
    :param assoc_dict:  Dict with key=AN, val=set of GO-terms
    :param obo_dag: Dict with additional methods
    :return: DefaultDict(Float)
    """
    go2ans_dict = {}
    term_cnt = defaultdict(float)
    for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
        for an in ans:
            if assoc_dict.has_key(an):
            # assoc_dict contains GO-terms and their parents (due to obo_dag.update_association)
            # for all ANs of goa_ref UniProt
            # if AN not in dict, no GO-term associated
            # goterms = get_goterms_from_an(an, include_parents=True)
                goterms = assoc_dict[an]
                for goterm in goterms:
                    if goterm in obo_dag:
                        goterm_name = obo_dag[goterm].id
                        term_cnt[goterm_name] += weight_fac
                        if not go2ans_dict.has_key(goterm):
                            go2ans_dict[goterm_name] = set([an])
                        else:
                            go2ans_dict[goterm_name].update([an])
                    else:
                        pass
    for goterm in term_cnt:
        term_cnt[goterm] = int(round(term_cnt[goterm]))
    go2ans2return = {}
    for goterm in term_cnt:
        count = term_cnt[goterm]
        if count >=1:
            go2ans2return[goterm] = go2ans_dict[goterm]
    return(term_cnt, go2ans2return)


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











