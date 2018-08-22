from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, variables


# def run_STRING_enrichment(pqo, ui, enrichment_method="compare_samples",
#         limit_2_entity_type="-51", go_slim_or_basic="basic", indent=True,
#         multitest_method="benjamini_hochberg", alpha=0.05, o_or_u_or_both="both",
#         fold_enrichment_for2background=None, p_value_uncorrected=None, FDR_cutoff=None, output_format="json"):
def run_STRING_enrichment(pqo, ui, args_dict):
    enrichment_method = args_dict["enrichment_method"]
    limit_2_entity_type = args_dict["limit_2_entity_type"]
    go_slim_or_basic = args_dict["go_slim_or_basic"]
    indent = args_dict["indent"]
    multitest_method = args_dict["multitest_method"]
    alpha = args_dict["alpha"]
    o_or_u_or_both = args_dict["o_or_u_or_both"]
    fold_enrichment_for2background = args_dict["fold_enrichment_for2background"]
    p_value_uncorrected = args_dict["p_value_uncorrected"]
    FDR_cutoff = args_dict["FDR_cutoff"]
    output_format = args_dict["output_format"]
    if FDR_cutoff == 0:
        FDR_cutoff = None
    if fold_enrichment_for2background == 0:
        fold_enrichment_for2background = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    protein_ans_list = ui.get_all_unique_ANs()
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    entity_types_2_use = {int(ele) for ele in limit_2_entity_type.split(";")}
    # remove KEGG infos, in order not to disseminate them without permission
    if args_dict["enrichment_method"] == "characterize_foreground" and args_dict["privileged"] == False:
        try:
            entity_types_2_use.remove(-51)
        except KeyError:
            pass
    for entity_type in entity_types_2_use:
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo)
        if not dag:
            args_dict["ERROR_entity_type"] = "ERROR: The entity type provided: '{}' is not recognized or can't be used for enrichment.".format(entity_type)
            return False
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict):
            enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method, alpha=alpha,
                                                          o_or_u_or_both=o_or_u_or_both, multitest_method=multitest_method, entity_type=entity_type, indent=indent)
            result = enrichment_study.get_result(output_format, FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
            if result: # don't add empty results
                results_all_function_types[entity_type] = result
    return results_all_function_types

# def run_STRING_enrichment_genome(pqo, ui, taxid, background_n=None, output_format="json", FDR_cutoff=None):
def run_STRING_enrichment_genome(pqo, ui, background_n, args_dict):
    # taxid=args_dict["taxid"]
    output_format=args_dict["output_format"]
    FDR_cutoff=args_dict["FDR_cutoff"]
    taxid = check_taxids(args_dict)
    if not taxid:
        return False

    enrichment_method = ui.enrichment_method
    protein_ans_list = ui.get_all_unique_ANs()

    if not check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
        taxid_string = str(taxid)
        ans_not_concur = [an for an in protein_ans_list if not an.startswith(taxid_string)]
        args_dict["ERROR_taxid_proteinAN"] = "ERROR_taxid_proteinAN: The TaxID '{}' provided and the taxid of the proteins provided (e.g. '{}') to not concur.".format(taxid, ans_not_concur[:3])
        # args_dict["1A WARNING/ERROR"] = "1A WARNING/ERROR: argument 'taxid' provided is '{}', it does not conform with the provided protein identifiers.".format(args_dict["taxid"])
        return False

    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    results_all_function_types = {}
    etype_2_association_2_count_dict_background = pqo.taxid_2_etype_2_association_2_count_dict_background[taxid]
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, "basic", pqo)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            enrichment_study = enrichment.EnrichmentStudy(ui=ui, assoc_dict=assoc_dict, obo_dag=dag, enrichment_method=enrichment_method,
                o_or_u_or_both="overrepresented", multitest_method="benjamini_hochberg", entity_type=entity_type,
                association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type], background_n=background_n)
            result = enrichment_study.get_result(output_format, FDR_cutoff=FDR_cutoff, fold_enrichment_for2background=None, p_value_uncorrected=None)
            if result: # don't add empty results
                results_all_function_types[entity_type] = result
    return results_all_function_types

def check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
    taxid_string = str(taxid)
    for an in protein_ans_list:
        if not an.startswith(taxid_string):
            return False
    return True

def check_taxids(args_dict):
    taxid = args_dict["taxid"]
    if taxid is not None:
        return taxid
    taxid = args_dict["species"]
    if taxid is not None:
        args_dict["ERROR_species"] = "ERROR_species: argument 'species' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["species"])
        return False
    taxid = args_dict["organism"]
    if taxid is not None:
        args_dict["ERROR_organism"] = "ERROR_organism: argument 'organism' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["organism"])
        return False

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
    else:
        print("entity_type: {} {} unknown".format(entity_type, type(entity_type)))
        # raise StopIteration
        return False

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
