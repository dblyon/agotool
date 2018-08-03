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
    redundant count e.g. 8 out of 10 samples --> foreground_count = 8
    foreground_n = 10 (1 unique proteinGroup * 10 for foreground_n)
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
            ### if goid in obo_dag:
                    # this assertion should not be neccessary since already check when creating tables for Postgres, hence only GO-term in
                    # the DB that are also in the current version of obo.
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
    redundant count e.g. 8 out of 10 samples --> foreground_count = 8
    foreground_n = 10 (1 unique proteinGroup * 10 for foreground_n)

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

def count_terms_manager(ans_set, assoc_dict, obo_dag=None, entity_type="-51"):
    if obo_dag is None:
        return count_terms_v3(ans_set, assoc_dict)
    if entity_type == "52": #method == "KEGG" (KEGG entity_type: "52")
        return count_terms_v2_KEGG(ans_set, assoc_dict)
    else:
        return count_terms_v2(ans_set, assoc_dict, obo_dag)

def count_terms_v2(ans_set, assoc_dict, obo_dag):
    """
    count the number of terms in the study group
    association_2_count_dict: key=GOid, val=Num of occurrences
    association_2_ANs_dict: key=GOid, val=SetOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag)
    :return: Tuple(dict, dict, int)
    """
    ans_2_count = set()
    association_2_ANs_dict = {}
    association_2_count_dict = defaultdict(int)
    for an in (AN for AN in ans_set if AN in assoc_dict):
        for association in assoc_dict[an]:
            ans_2_count.update([an])
            association_id = obo_dag[association].id
            association_2_count_dict[association_id] += 1
            if not association_id in association_2_ANs_dict:
                association_2_ANs_dict[association_id] = set([an])
            else:
                association_2_ANs_dict[association_id].update([an])
    return association_2_count_dict, association_2_ANs_dict, len(ans_2_count)

def count_terms_v3(ans_set, assoc_dict):
    """
    # ToDo write test for counter functions
    # goterm: 'GO:0007610' has secondary id 'GO:0044708' --> if resolved at table creation not a problem otherwise it is
    count the number of terms in the study group
    association_2_count_dict: key=GOid, val=Num of occurrences
    association_2_ANs_dict: key=GOid, val=SetOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag)
    :return: Tuple(dict, dict, int)
    """
    # ans_counter = 0
    association_2_ANs_dict = {}
    association_2_count_dict = defaultdict(int)
    for an in (AN for AN in ans_set if AN in assoc_dict):
        # ans_counter += 1
        for association in assoc_dict[an]:
            association_2_count_dict[association] += 1
            if not association in association_2_ANs_dict:
                association_2_ANs_dict[association] = {an}
            else:
                association_2_ANs_dict[association] |= {an} # update dict
    return association_2_count_dict, association_2_ANs_dict, len(ans_set) #ans_counter

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
            # if goterm in obo_dag:
            # this assertion should not be neccessary since already check when creating tables for Postgres, hence only GO-term in
            # the DB that are also in the current version of obo.
            term_cnt[obo_dag[goterm].id] += 1
            if goterm not in go2ans_dict:
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
            if goid not in go2ans_dict:
                go2ans_dict[goid] = set([an])
            else:
                go2ans_dict[goid].update([an])
    return go2ans_dict

def count_terms_abundance_corrected_manager(ui, assoc_dict, obo_dag, method):
    if method == "KEGG":
        return count_terms_abundance_corrected_KEGG(ui, assoc_dict)
    else:
        return count_terms_abundance_corrected(ui, assoc_dict, obo_dag)

def count_terms_abundance_corrected(ui, assoc_dict, obo_dag):
    """
    modify to use protein groups --> handled in Userinput.py
    produce abundance corrected counts of GO-terms of background frequency
    round floats to nearest integer
    Userinput-object includes ANs of sample, and background as well as abundance data
    produces:
        term_cnt: key=GOid, val=Num of occurrences
        go2ans_dict: key=GOid, val=ListOfANs
    :param ui: Userinput-object
    :param assoc_dict:  Dict with key=AN, val=set of GO-terms
    :param obo_dag: Dict with additional methods
    :return: DefaultDict(Float)
    """
    go2ans_dict = {}
    term_cnt = defaultdict(float)
    for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
        for an in ans:
            if an in assoc_dict:
            # assoc_dict contains GO-terms and their parents (due to obo_dag.update_association) #!!!
            # for all ANs of goa_ref UniProt
            # if AN not in dict, no GO-term associated
            # goterms = get_goterms_from_an(an, include_parents=True)
                goterms = assoc_dict[an]
                for goterm in goterms:
                    # if goterm in obo_dag:
                    # this assertion should not be neccessary since already check when creating tables for Postgres, hence only GO-term in
                    # the DB that are also in the current version of obo.
                    goterm_name = obo_dag[goterm].id
                    term_cnt[goterm_name] += weight_fac
                    # if not go2ans_dict.has_key(goterm):
                    if goterm not in go2ans_dict:
                        # go2ans_dict[goterm_name] = set([an])
                        go2ans_dict[goterm_name] = {an}
                    else:
                        # go2ans_dict[goterm_name].update([an])
                        go2ans_dict[goterm_name] |= {an}
    for goterm in term_cnt:
        term_cnt[goterm] = int(round(term_cnt[goterm]))
    go2ans2return = {}
    for goterm in term_cnt:
        count = term_cnt[goterm]
        if count >=1:
            go2ans2return[goterm] = go2ans_dict[goterm]
    return term_cnt, go2ans2return

def count_terms_abundance_corrected_KEGG(ui, assoc_dict):
    """
    #!!! modify to use protein groups --> handled in Userinput.py or not?
    produce abundance corrected counts of GO-terms of background frequency
    round floats to nearest integer
    Userinput-object includes ANs of sample, and background as well as abundance data
    produces:
        term_cnt: key=GOid, val=Num of occurrences
        go2ans_dict: key=GOid, val=ListOfANs
    :param ui: Userinput-object
    :param assoc_dict:  Dict with key=AN, val=set of GO-terms
    :return: DefaultDict(Float)
    """
    go2ans_dict = {}
    term_cnt = defaultdict(float)
    for ans, weight_fac in ui.iter_bins(): # for every bin, produce ans-background and weighting-factor
        for an in ans:
            if an in assoc_dict:
                goterms = assoc_dict[an]
                for goterm in goterms:
                    goterm_name = goterm
                    term_cnt[goterm_name] += weight_fac
                    if goterm not in go2ans_dict:
                        # go2ans_dict[goterm_name] = set([an])
                        go2ans_dict[goterm_name] = {an}
                    else:
                        # go2ans_dict[goterm_name].update([an])
                        go2ans_dict[goterm_name] |= {an}
                else:
                    pass
    for goterm in term_cnt:
        term_cnt[goterm] = int(round(term_cnt[goterm]))
    go2ans2return = {}
    for goterm in term_cnt:
        count = term_cnt[goterm]
        if count >=1:
            go2ans2return[goterm] = go2ans_dict[goterm]
    return term_cnt, go2ans2return

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

