from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, variables #, query


def run(pqo, ui,
        gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, backtracking, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting):

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    protein_ans_list = ui.get_all_unique_ANs()
    # function_type, limit_2_parent = get_function_type__and__limit_2_parent(gocat_upk)
    function_type = get_function_type__and__limit_2_parent(gocat_upk)

    assoc_dict = pqo.get_association_dict(protein_ans_list, gocat_upk, basic_or_slim=go_slim_or_basic)

    ### now convert assoc_dict into proteinGroups to consensus assoc_dict
    proteinGroups_list = ui.get_all_unique_proteinGroups()
    assoc_dict_pg = tools.convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list)
    assoc_dict.update(assoc_dict_pg)
    # assoc_dict: remove ANs with empty set as values
    assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1}
    # dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo.go_dag, pqo.goslim_dag, pqo.upk_dag, KEGG_pseudo_dag)
    dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo)
    enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, backtracking, o_or_u_or_both, multitest_method, gocat_upk, function_type)
    header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
    return header, results

def run_STRING_enrichment(pqo, ui,
        gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, backtracking, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting):

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    protein_ans_list = ui.get_all_unique_ANs()
    # function_type, limit_2_parent = get_function_type__and__limit_2_parent(gocat_upk)
    # function_type = get_function_type__and__limit_2_parent(gocat_upk)

    # only do query once for STRING style enrichment
    # get assocations for everything (query DB once) but split them up into categories
    # assoc_dict = pqo.get_association_dict(protein_ans_list, gocat_upk, basic_or_slim=go_slim_or_basic)
    assoc_dict_metadict = pqo.get_association_dict_split_by_category(protein_ans_list)

    #!!! strip protein-Group support for speed?
    ### now convert assoc_dict into proteinGroups to consensus assoc_dict
    # proteinGroups_list = ui.get_all_unique_proteinGroups()
    # assoc_dict_pg = tools.convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list)
    # assoc_dict.update(assoc_dict_pg)


    # now do enrichment for each category, collect results and return combined

    results_all_function_types = {}
    # function_types = ("GO", "KEGG", "UPK") # Interpro, etc.
    for function_type in variables.function_types:
        dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo)
        assoc_dict = assoc_dict_metadict[function_type]

        # assoc_dict: remove ANs with empty set as values
        assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1}
        enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, backtracking, o_or_u_or_both, multitest_method, gocat_upk, function_type)
        header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
        results_all_function_types[function_type] = (header, results)
    return results_all_function_types

def pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo):
    # if function_type == "GO":
    if function_type in {"GO", "BP", "CP", "MF"}:
        if go_slim_or_basic == "slim":
            return pqo.goslim_dag
        else:
            return pqo.go_dag
    elif function_type == "UPK":
        return pqo.upk_dag
    elif function_type == "KEGG":
        return pqo.KEGG_pseudo_dag
    elif function_type == "DOM":
        return pqo.DOM_pseudo_dag
    else:
        raise StopIteration

# def get_function_type__and__limit_2_parent(gocat_upk):
#     """
#     # choices = (("all_GO", "all GO categories"),
#     #            ("BP", "GO Biological Process"),
#     #            ("CP", "GO Celluar Compartment"),
#     #            ("MF", "GO Molecular Function"),
#     #            ("UPK", "UniProt keywords"),
#     #            ("KEGG", "KEGG pathways")),
#     :param gocat_upk: String
#     :return: Tuple(String, Bool)
#     """
#     if gocat_upk in {"BP", "CP", "MF"}:
#         return "GO", gocat_upk
#     elif gocat_upk == "all_GO":
#         return "GO", None
#     else:
#         return gocat_upk, None

def get_function_type__and__limit_2_parent(gocat_upk):
    """
    # choices = (("all_GO", "all GO categories"),
    #            ("BP", "GO Biological Process"),
    #            ("CP", "GO Celluar Compartment"),
    #            ("MF", "GO Molecular Function"),
    #            ("UPK", "UniProt keywords"),
    #            ("KEGG", "KEGG pathways")),
    :param gocat_upk: String
    :return: Tuple(String, Bool)
    """
    if gocat_upk in {"BP", "CP", "MF", "all_GO"}:
        return "GO" #, gocat_upk
    else:
        return gocat_upk #, None

def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)
