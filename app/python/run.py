from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, variables, cluster_filter, query
import pandas as pd
import numpy as np
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed
# import concurrent.futures
process_pool = ProcessPoolExecutor(2)
# thread_pool = ThreadPoolExecutor(4)
from fisher import pvalue
from io import StringIO
from multiple_testing import Bonferroni, Sidak, HolmBonferroni, BenjaminiHochberg
from collections import defaultdict


def run_STRING_enrichment(pqo, ui, args_dict):
    enrichment_method = args_dict["enrichment_method"]
    if enrichment_method not in {"characterize_foreground", "compare_samples", "compare_groups"}:
        args_dict["ERROR_enrichment_method"] = "ERROR: enrichment_method {} is not implemented. Please check the input parameters and examples.".format(enrichment_method)
        return False
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
    filter_parents = args_dict["filter_parents"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]

    if FDR_cutoff == 0:
        FDR_cutoff = None
    if fold_enrichment_for2background == 0:
        fold_enrichment_for2background = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None
    protein_ans_list = ui.get_all_unique_ANs()
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    df_list = []
    entity_types_2_use = {int(ele) for ele in limit_2_entity_type.split(";")}
    # remove KEGG infos, in order not to disseminate them without permission
    if args_dict["enrichment_method"] == "characterize_foreground" and args_dict["privileged"] == False:
        try:
            entity_types_2_use.remove(-51)
        except KeyError:
            pass
    for entity_type in entity_types_2_use:
        # dag = pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo)
        if entity_type not in variables.entity_types:
            args_dict["ERROR_entity_type"] = "ERROR: The entity type provided: '{}' is not recognized or can't be used for enrichment.".format(entity_type)
            return False
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict):
            enrichment_study = enrichment.EnrichmentStudy(pqo, args_dict, ui=ui, assoc_dict=assoc_dict, enrichment_method=enrichment_method, alpha=alpha,
                                                          o_or_u_or_both=o_or_u_or_both, multitest_method=multitest_method, entity_type=entity_type, indent=indent)
            result_df = enrichment_study.get_result(FDR_cutoff, fold_enrichment_for2background, p_value_uncorrected)
            if not result_df.empty:
                result_df["etype"] = entity_type
                result_df["category"] = variables.entityType_2_functionType_dict[entity_type]
                df_list.append(result_df)
    try:
        df = pd.concat(df_list)
    except ValueError: # empty list
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again. Alternatively you could try to use 'enrichment_method': 'characterize_foreground' in order to see all the functional annotations available in the DB (except KEGG)."
        return False

    df["hierarchical_level"] = df["term"].apply(lambda term: pqo.functerm_2_level_dict[term.replace(".", "")]) # since "indent" can prepend dots
    if filter_parents and (args_dict["enrichment_method"] != "characterize_foreground"):
        df = cluster_filter.filter_parents_if_same_foreground_v4(df, pqo.lineage_dict, variables.blacklisted_terms)
    if enrichment_method == "characterize_foreground":
        return format_results(df.sort_values(["etype"], ascending=[False]), output_format, args_dict)
    else:
        if filter_foreground_count_one:
            df = df[df["foreground_count"] > 1]
        # cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids']
        # cols_sort_order += sorted(set(df.columns.tolist()) - set(cols_sort_order))
        # return format_results(df[cols_sort_order].sort_values(["etype", "p_value"], ascending=[False, True]), output_format, args_dict)
        if args_dict["LOW_MEMORY"]: # variables.LOW_MEMORY:
            an_2_description_dict = query.get_description_from_an(df["term"].tolist())
            df["description"] = df["term"].apply(lambda an: an_2_description_dict[an])
        else:
            df["description"] = df["term"].apply(lambda an: pqo.function_an_2_description_dict[an])
        df = filter_and_sort_PMID(df)
        return format_results(df, output_format, args_dict)

def run_STRING_enrichment_genome(pqo, ui, background_n, args_dict):
    taxid = check_taxids(args_dict)
    if not taxid:
        return False
    output_format=args_dict["output_format"]
    FDR_cutoff=args_dict["FDR_cutoff"]
    filter_parents = args_dict["filter_parents"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    enrichment_method = args_dict["enrichment_method"]
    protein_ans_list = ui.get_all_unique_ANs()

    if not check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
        taxid_string = str(taxid)
        ans_not_concur = [an for an in protein_ans_list if not an.startswith(taxid_string)]
        args_dict["ERROR_taxid_proteinAN"] = "ERROR_taxid_proteinAN: The TaxID '{}' provided and the taxid of the proteins provided (e.g. '{}') do not concur.".format(taxid, ans_not_concur[:3])
        return False
    df_list = []
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    if args_dict["LOW_MEMORY"]: #variables.LOW_MEMORY:
        etype_2_association_2_count_dict_background = query.from_taxid_get_association_2_count_split_by_entity(taxid)
    else:
        etype_2_association_2_count_dict_background = pqo.taxid_2_etype_2_association_2_count_dict_background[taxid]
    for entity_type in variables.entity_types_with_data_in_functions_table:
        #print(entity_type)
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            #print(assoc_dict["9606.ENSP00000266970"])
           # print(assoc_dict["9606.ENSP00000361021"])
            enrichment_study = enrichment.EnrichmentStudy(pqo, args_dict, ui=ui, assoc_dict=assoc_dict, enrichment_method=enrichment_method,
                o_or_u_or_both="overrepresented", multitest_method="benjamini_hochberg", entity_type=entity_type,
                association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type], background_n=background_n)
            #try:
            #    print(enrichment_study.df.shape)
            #except:
            #    print(type(enrichment_study.df))
            result_df = enrichment_study.get_result(FDR_cutoff=FDR_cutoff, fold_enrichment_for2background=None, p_value_uncorrected=None)
            #print(result_df.shape)
            if result_df is None:
                return False
            if not result_df.empty:
                result_df["etype"] = entity_type
                result_df["category"] = variables.entityType_2_functionType_dict[entity_type]
                df_list.append(result_df)
    try:
        df = pd.concat(df_list)
    except ValueError: # empty list
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
        return False

    df["hierarchical_level"] = df["term"].apply(lambda term: pqo.functerm_2_level_dict[term])
    #df.to_csv("temp_df_filter_parents.txt", sep="\t", header=True, index=False)
    if filter_parents: 
        df = cluster_filter.filter_parents_if_same_foreground_v4(df, pqo.lineage_dict, variables.blacklisted_terms, variables.entity_types_with_ontology)
    if filter_foreground_count_one:
        df = df[df["foreground_count"] > 1]
    # could be done async while p-values are being calculated
    if args_dict["LOW_MEMORY"]: #variables.LOW_MEMORY:
        an_2_description_dict = query.get_description_from_an(df["term"].tolist())
        df["description"] = df["term"].apply(lambda an: an_2_description_dict[an])
    else:
        df["description"] = df["term"].apply(lambda an: pqo.function_an_2_description_dict[an])
    df = filter_and_sort_PMID(df)
    #an = "HSA-3700989"
    #print("pqo", an, pqo.functerm_2_level_dict[an])
    #print("pqo", an, pqo.function_an_2_description_dict[an])
    return format_results(df, output_format, args_dict)

def count_terms_v3(ans_set, assoc_dict):
    association_2_ANs_dict = {}
    association_2_count_dict = defaultdict(int)
    for an in (AN for AN in ans_set if AN in assoc_dict):
        for association in assoc_dict[an]:
            association_2_count_dict[association] += 1
            if not association in association_2_ANs_dict:
                association_2_ANs_dict[association] = {an}
            else:
                association_2_ANs_dict[association] |= {an} # update dict
    return association_2_count_dict, association_2_ANs_dict, len(ans_set)

def run_rank_enrichment(pqo, ui, args_dict):
    taxid = check_taxids(args_dict)
    if not taxid:
        return False
    output_format=args_dict["output_format"]
    FDR_cutoff=args_dict["FDR_cutoff"]
    filter_parents = args_dict["filter_parents"]
    filter_foreground_count_one = args_dict["filter_foreground_count_one"]
    enrichment_method = args_dict["enrichment_method"]
    protein_ans_list = ui.get_all_unique_ANs()

    if not check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
        taxid_string = str(taxid)
        ans_not_concur = [an for an in protein_ans_list if not an.startswith(taxid_string)]
        args_dict["ERROR_taxid_proteinAN"] = "ERROR_taxid_proteinAN: The TaxID '{}' provided and the taxid of the proteins provided (e.g. '{}') do not concur.".format(taxid, ans_not_concur[:3])
        return False
    etype_2_association_dict = pqo.get_association_dict_split_by_category(protein_ans_list)
    df_list = []
    # etype_2_association_2_count_dict_background = pqo.taxid_2_etype_2_association_2_count_dict_background[taxid]
    for entity_type in variables.entity_types_with_data_in_functions_table:
        assoc_dict = etype_2_association_dict[entity_type]
        if bool(assoc_dict): # not empty dictionary
            enrichment_study = enrichment.EnrichmentStudy(pqo, args_dict, ui=ui, assoc_dict=assoc_dict, enrichment_method=enrichment_method, o_or_u_or_both="overrepresented", multitest_method="benjamini_hochberg", entity_type=entity_type)
            result_df = enrichment_study.get_result(FDR_cutoff=FDR_cutoff, fold_enrichment_for2background=None, p_value_uncorrected=None)
            if result_df is None:
                return False
            if not result_df.empty:
                result_df["etype"] = entity_type
                result_df["category"] = variables.entityType_2_functionType_dict[entity_type]
                df_list.append(result_df)
    try:
        df = pd.concat(df_list)
    except ValueError: # empty list
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
        return False
    df["hierarchical_level"] = df["term"].apply(lambda term: pqo.functerm_2_level_dict[term])
    if filter_parents:
        df = cluster_filter.filter_parents_if_same_foreground_v4(df, pqo.lineage_dict, variables.blacklisted_terms, variables.entity_types_with_ontology)
    if filter_foreground_count_one:
        df = df[df["foreground_count"] > 1]
    if args_dict["LOW_MEMORY"]: #variables.LOW_MEMORY:
        an_2_description_dict = query.get_description_from_an(df["term"].tolist())
        df["description"] = df["term"].apply(lambda an: an_2_description_dict[an])
    else:
        df["description"] = df["term"].apply(lambda an: pqo.function_an_2_description_dict[an])

    df = filter_and_sort_PMID(df)
    return format_results(df, output_format, args_dict)

def filter_and_sort_PMID(df, PMID_top_100=True):
    ### remove blacklisted terms --> duplicate to cluster_filter.filter_parents_if_same_foreground_v2
    # df = df[~df["term"].isin(variables.blacklisted_terms)]
    cond_PMID = df["etype"] == -56
    if sum(cond_PMID) > 0:
        df_PMID = df[cond_PMID]
        df_rest = df[~cond_PMID]
        df_PMID["year"] = df_PMID["description"].apply(PMID_description_to_year)
        df_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])
        if PMID_top_100:
            df_PMID = df_PMID.head(100)
        df_rest = df_rest.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        df = pd.concat([df_rest, df_PMID], sort=False)
        cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids', 'year']
    else:
        df = df.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids']
    cols_sort_order += sorted(set(df.columns.tolist()) - set(cols_sort_order))
    return df[cols_sort_order]

def PMID_description_to_year(string_):
    try:
        return int(string_[1:5])
    except ValueError or IndexError:
        return np.nan

def format_results(df, output_format, args_dict):
    if output_format == "tsv":
        return df.to_csv(sep="\t", header=True, index=False)
    if output_format == "tsv-no-header" or output_format == "tsv_no_header":
        return df.to_csv(sep="\t", header=False, index=False)
    elif output_format == "json":
        etype_2_resultsjson_dict = {}
        for etype, group in df.groupby("etype"):
            etype_2_resultsjson_dict[etype] = group.to_json(orient='records')
        return etype_2_resultsjson_dict
    elif output_format == "xml": # xml gets formatted in runserver.py
        dict_2_return = {}
        for etype, df_group in df.groupby("etype"):
            results = df_group.to_csv(sep="\t", header=True, index=False)  # convert DatFrame to string
            header, rows = results.split("\n", 1)  # is df in tsv format
            xml_string = create_xml_tree(header, rows.split("\n"))
            dict_2_return[etype] = xml_string.decode()
        return dict_2_return
    else:
        args_dict["ERROR_output_format"] = "output_format {} is unknown, please check your parameters".format(output_format)
        return False

def create_xml_tree(header, rows):
    xml_tree = etree.Element("EnrichmentResult")
    header = header.split("\t")
    for row in rows:
        child = etree.SubElement(xml_tree, "record")
        for tag_content in zip(header, row.split("\t")):
            tag, content = tag_content
            etree.SubElement(child, tag).text = content
    return etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")#.decode("UTF-8")

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

# def pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo):
#     if entity_type in {-21, -22, -23}:
#         if go_slim_or_basic == "basic":
#             return pqo.go_dag
#         else:
#             return pqo.goslim_dag
#     elif entity_type == -51:
#         return pqo.upk_dag
#     elif entity_type == -52:
#         return pqo.kegg_pseudo_dag
#     elif entity_type == -53:
#         return pqo.smart_pseudo_dag
#     elif entity_type == -54:
#         return pqo.interpro_pseudo_dag
#     elif entity_type == -55:
#         return pqo.pfam_pseudo_dag
#     elif entity_type == -56:
#         return pqo.pmid_pseudo_dag
#     else:
#         print("entity_type: {} {} unknown".format(entity_type, type(entity_type)))
#         # raise StopIteration
#         return False

# def pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, pqo):
#     # if entity_type == "GO":
#     if function_type in {"GO", "BP", "CP", "MF"}:
#         if go_slim_or_basic == "slim":
#             return pqo.goslim_dag
#         else:
#             return pqo.go_dag
#     elif function_type == "UPK":
#         return pqo.upk_dag
#     elif function_type == "KEGG":
#         return pqo.KEGG_pseudo_dag
#     elif function_type == "DOM":
#         return pqo.DOM_pseudo_dag
#     else:
#         raise StopIteration

