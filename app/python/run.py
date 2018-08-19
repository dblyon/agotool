from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, variables, query


# def run(pqo, ui,
#         gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
#         o_or_u_or_both, fold_enrichment_for2background,
#         p_value_uncorrected, p_value_mulitpletesting):
#     if fold_enrichment_for2background == 0:
#         fold_enrichment_for2background = None
#     if p_value_mulitpletesting == 0:
#         p_value_mulitpletesting = None
#     if p_value_uncorrected == 0:
#         p_value_uncorrected = None
#     protein_ans_list = ui.get_all_unique_ANs()
#     function_type = get_function_type__and__limit_2_parent(gocat_upk)
#     assoc_dict = pqo.get_association_dict(protein_ans_list, gocat_upk, basic_or_slim=go_slim_or_basic)
#     ### now convert assoc_dict into proteinGroups to consensus assoc_dict
#     proteinGroups_list = ui.get_all_unique_proteinGroups()
#     assoc_dict_pg = tools.convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list)
#     assoc_dict.update(assoc_dict_pg)
#     # assoc_dict: remove ANs with empty set as values
#     assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1}
#     dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo)
#     enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, o_or_u_or_both, multitest_method, gocat_upk, function_type)
#     header, results = enrichment_study.write_summary2file_web(fold_enrichment_for2background, p_value_mulitpletesting, p_value_uncorrected, indent)
#     return header, results

def run_STRING_enrichment(pqo, ui, enrichment_method="compare_samples",
        limit_2_entity_type=None, go_slim_or_basic="basic", indent=True,
        multitest_method="Benjamini_Hochberg", alpha=0.05, o_or_u_or_both="both",
        fold_enrichment_for2background=None, p_value_uncorrected=None, FDR_cutoff=None, output_format="json"):
    if FDR_cutoff == 0:
        FDR_cutoff = None
    if fold_enrichment_for2background == 0:
        fold_enrichment_for2background = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None
    protein_ans_list = ui.get_all_unique_ANs()
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    if limit_2_entity_type is None:
        entity_types_2_use = variables.entity_types_with_data_in_functions_table
    else:
        entity_types_2_use = limit_2_entity_type
    for entity_type in entity_types_2_use:
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict):
            enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method, alpha=alpha,
                                                          o_or_u_or_both=o_or_u_or_both, multitest_method=multitest_method, entity_type=entity_type,
                                                          indent=indent)
            result = enrichment_study.get_result(output_format, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
            results_all_function_types[entity_type] = result
    return results_all_function_types

def run_STRING_enrichment_genome(pqo, ui, taxid, background_n=None, output_format="json", FDR_cutoff=None):
    enrichment_method = ui.enrichment_method
    protein_ans_list = ui.get_all_unique_ANs()
    # check that all ENSPs are of given taxid
    # ToDo
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    etype_2_association_2_count_dict_background = pqo.taxid_2_etype_2_association_2_count_dict_background[taxid]
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, "basic", pqo)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method,
                o_or_u_or_both="overrepresented", multitest_method="Benjamini_Hochberg", entity_type=entity_type,
                association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type],
                background_n=background_n)
            result = enrichment_study.get_result(output_format, FDR_cutoff=FDR_cutoff, fold_enrichment_for2background=None, p_value_uncorrected=None)
            results_all_function_types[entity_type] = result
    return results_all_function_types

def pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo):
    if entity_type in {-21, -22, -23}:
        if go_slim_or_basic == "basic":
            return pqo.go_dag
        else:
            return pqo.goslim_dag
    elif entity_type == -51:
        return pqo.upk_dag
    elif entity_type == -52:
        return pqo.kegg_pseudo_dag
    elif entity_type == -53:
        return pqo.smart_pseudo_dag
    elif entity_type == -54:
        return pqo.interpro_pseudo_dag
    elif entity_type == -55:
        return pqo.pfam_pseudo_dag
    # elif entity_type == -56:
    #     return pqo.DOM_pseudo_dag
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
