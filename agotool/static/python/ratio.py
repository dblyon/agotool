from collections import defaultdict


def count_terms_v2(ans_set, assoc_dict, obo_dag):
    """
    count the number of terms in the study group
    produces
    term_cnt: key=GOid, val=Num of occurrences
    go2ans_dict: key=GOid, val=ListOfANs
    count_n: Integer(Number of ANs with a GO-term in assoc_dict and obo_dag
    """
    ans2count = set()
    go2ans_dict = {}
    term_cnt = defaultdict(int)
    for an in (acnum for acnum in ans_set if acnum in assoc_dict):
        for goterm in assoc_dict[an]:
            if goterm in obo_dag:
                ans2count.update([an])
                term_cnt[obo_dag[goterm].id] += 1
                if not go2ans_dict.has_key(goterm):
                    go2ans_dict[goterm] = set([an])
                else:
                    go2ans_dict[goterm].update([an])
    return(term_cnt, go2ans_dict, len(ans2count))


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
                    if not go2ans_dict.has_key(goterm):
                        go2ans_dict[goterm] = set([an])
                    else:
                        go2ans_dict[goterm].update([an])
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











