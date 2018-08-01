from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, variables, query


def run(pqo, ui,
        gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting):
    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None
    protein_ans_list = ui.get_all_unique_ANs()
    function_type = get_function_type__and__limit_2_parent(gocat_upk)
    assoc_dict = pqo.get_association_dict(protein_ans_list, gocat_upk, basic_or_slim=go_slim_or_basic)
    ### now convert assoc_dict into proteinGroups to consensus assoc_dict
    proteinGroups_list = ui.get_all_unique_proteinGroups()
    assoc_dict_pg = tools.convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list)
    assoc_dict.update(assoc_dict_pg)
    # assoc_dict: remove ANs with empty set as values
    assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1}
    dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo)
    enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, o_or_u_or_both, multitest_method, gocat_upk, function_type)
    header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
    return header, results

def run_STRING_enrichment(pqo, ui,
        gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting):
    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None
    protein_ans_list = ui.get_all_unique_ANs()
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    for entity_type in etype_2_association_dict.keys(): #variables.entity_types:
        # ToDo not implemented yet
        if entity_type not in variables.entity_types_with_data_in_functions_table:
            continue
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            ### assoc_dict: remove ANs with empty set as values --> don't think this is necessary since these rows should not exist in DB
            # assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1}
            enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, o_or_u_or_both, multitest_method, gocat_upk, entity_type)
            header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
            results_all_function_types[entity_type] = (header, results)
    return results_all_function_types

def run_STRING_enrichment_speed(pqo, ui,
        go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting, taxid, background_n=None):

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None
    enrichment_method = ui.enrichment_method
    # print("-"*20)
    # print("enrichment_method: ", enrichment_method)
    # print("-"*20)
    protein_ans_list = ui.get_all_unique_ANs()
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    if enrichment_method == "genome":
        # ensps_taxid = query.get_proteins_of_taxid(taxid)
        etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, _ = query.get_association_2_counts_split_by_entity(taxid)
        # don't use etype_2_background_n but background_n above instead

    ### ToDo
    # create "method" "genome" (for background)
    # no background has to be provided, but TaxID is being used
    #   - for association dict ? --> only for selected species this could be stored in memory?
    #   - precomputed counts for each TaxID in DB
    # for api string calls don't do cleanup?

    # ToDo not implemented yet for all asoiciations
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            ### assoc_dict: remove ANs with empty set as values --> don't think this is necessary since these rows should not exist in DB
            # assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1},
            if enrichment_method == "genome":
                enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method,
                    alpha=alpha, o_or_u_or_both=o_or_u_or_both, multitest_method=multitest_method, entity_type=entity_type,
                    association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type],
                    association_2_ANs_dict_background=etype_2_association_2_ANs_dict_background[entity_type],
                    background_n=background_n)
            else:
                enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method,
                    alpha=alpha, o_or_u_or_both=o_or_u_or_both, multitest_method=multitest_method, entity_type=entity_type)
            header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
            results_all_function_types[entity_type] = (header, results)
    return results_all_function_types


def pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo):
    if entity_type in {'-21', '-22', '-23'}:
        if go_slim_or_basic == "slim":
            return pqo.goslim_dag
        else:
            return pqo.go_dag
    elif entity_type == "-51":
        return pqo.upk_dag
    elif entity_type == "-52":
        return pqo.kegg_pseudo_dag
    elif entity_type in {"-53", "-54", "-55", "-56"}:
        return pqo.DOM_pseudo_dag
    else:
        raise StopIteration

def pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo):
    # if entity_type == "GO":
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
