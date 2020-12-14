import os, sys
import pandas as pd
import numpy as np
from lxml import etree
import json

sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import variables, colnames
import run_cythonized

etype = colnames.etype
term = colnames.term
funcEnum = colnames.funcEnum
description = colnames.description
p_value = colnames.p_value
FDR = colnames.FDR
effect_size = colnames.effect_size
over_under = colnames.over_under
hierarchical_level = colnames.hierarchical_level
s_value = colnames.s_value
ratio_in_FG = colnames.ratio_in_FG
ratio_in_BG = colnames.ratio_in_BG
FG_IDs = colnames.FG_IDs
BG_IDs = colnames.BG_IDs
FG_count = colnames.FG_count
BG_count = colnames.BG_count
FG_n = colnames.FG_n
BG_n = colnames.BG_n
rank = colnames.rank
year = colnames.year
category = colnames.category


def run_UniProt_enrichment(pqo, ui, args_dict, api_call=False):
    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis()
    ncbi = pqo.ncbi
    if args_dict["o_or_u_or_both"] == "both":
        encoding = 0
    elif args_dict["o_or_u_or_both"] == "overrepresented":
        encoding = 1
    elif args_dict["o_or_u_or_both"] == "underrepresented":
        encoding = 2
    else:
        args_dict["ERROR o_or_u_or_both"] = "Unknown option for o_or_u_or_both, does not understand: '{}'".format(args_dict["o_or_u_or_both"])
        return False
    args_dict["o_or_u_or_both_encoding"] = encoding
    if args_dict["enrichment_method"] == "characterize_foreground":
        df_2_return = run_cythonized.run_characterize_foreground_cy(ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=variables.LOW_MEMORY)
    else:
        df_2_return = run_cythonized.run_enrichment_cy(ncbi, ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=variables.LOW_MEMORY)
        # ENSP_2_tuple_funcEnum_score_dict, ncbi, ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=False, debug=False, KS_method="cy", KS_etypes_FG_IDs=True)
    if type(df_2_return) == dict: # args_dict returned since
        # e.g. enrichment_method "genome" using different taxon for foreground than background
        return False # display "info_check_input.html"
    elif type(df_2_return) == pd.core.frame.DataFrame:
        if df_2_return.shape[0] == 0:
            args_dict["ERROR empty results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
            if api_call:
                output_format = args_dict["output_format"]
                return format_results(df_2_return, output_format, args_dict)
            else:
                return False
        else:
            output_format = args_dict["output_format"]
            return format_results(df_2_return, output_format, args_dict)
    else:
        print("run.py " * 5)
        print(type(df_2_return), df_2_return)
        print("run.py " * 5)
        return False

def run_STRING_enrichment(pqo, ui, args_dict):
    enrichment_method = args_dict["enrichment_method"]
    if enrichment_method not in {"characterize_foreground", "compare_samples"}: # , "compare_groups"
        args_dict["ERROR_enrichment_method"] = "ERROR: enrichment_method {} is not implemented. Please check the input parameters and examples.".format(enrichment_method)
        return False

    enrichment_method = args_dict["enrichment_method"]
    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    #with pqo.get_preloaded_objects_per_analysis_contextmanager(method=enrichment_method) as preloaded_objects_per_analysis:
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis(method=enrichment_method)
    if enrichment_method == "compare_samples":
        protein_ans_fg = ui.get_foreground_an_set() # is a set
        protein_ans_bg = ui.get_background_an_set() # is a set
        df_2_return = run_cythonized.run_compare_samples_cy(protein_ans_fg, protein_ans_bg, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)

    elif enrichment_method == "characterize_foreground":
        protein_ans = ui.get_an_redundant_foreground() # is a list
        df_2_return = run_cythonized.run_characterize_foreground_cy(protein_ans, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)

    ### for STRING internally disabled, otherwise this makes sense to use DONT DELETE
    if df_2_return.shape[0] == 0:
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
        return False

    output_format = args_dict["output_format"]
    return format_results(df_2_return, output_format, args_dict)

def run_STRING_enrichment_genome(pqo, ui, background_n, args_dict):
    taxid = check_taxids(args_dict)
    if not taxid:
        args_dict["ERROR_taxid"] = "Please provide a TaxID (a taxonomic identifier e.g. 9606 for Homo sapiens)"
        return False

    protein_ans = ui.get_all_individual_AN() # proteins_ans is a list
    if variables.VERSION_ != "STRING":
        if not check_all_ENSPs_of_given_taxid(protein_ans, taxid):
            taxid_string = str(taxid)
            ans_not_concur = [an for an in protein_ans if not an.startswith(taxid_string)]
            args_dict["ERROR_taxid_proteinAN"] = "ERROR_taxid_proteinAN: The TaxID '{}' provided and the taxid of the proteins provided (e.g. '{}') do not concur.".format(taxid, ans_not_concur[:3])
            return False

    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    #with pqo.get_preloaded_objects_per_analysis_contextmanager(method="genome") as preloaded_objects_per_analysis:
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis(method="genome")
    # if variables.temp_dont_run_analysis:
    #     return format_results(pd.DataFrame(), args_dict["output_format"], args_dict)
    df_2_return = run_cythonized.run_genome_cy(taxid, protein_ans, background_n, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)
    if variables.VERSION_ != "STRING": # for STRING internally disabled, otherwise this makes sense to use DONT DELETE
        if df_2_return.shape[0] == 0:
            args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
            return False
    return format_results(df_2_return, args_dict["output_format"], args_dict)

def filter_and_sort_PMID(df, PMID_top_100=True): # deprecated ?
    ### remove blacklisted terms --> duplicate to cluster_filter.filter_parents_if_same_foreground_v2
    # df = df[~df["term"].isin(variables.blacklisted_terms)]
    cond_PMID = df["etype"] == -56
    if sum(cond_PMID) > 0:
        df_PMID = df[cond_PMID]
        df_rest = df[~cond_PMID]
        df_PMID["year"] = df_PMID["description"].apply(PMID_description_to_year)
        # df_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])
        df_PMID = df_PMID.sort_values([FDR, p_value, year, FG_count], ascending=[True, True, False, False])
        if PMID_top_100:
            df_PMID = df_PMID.head(100)
        # df_rest = df_rest.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        df_rest = df_rest.sort_values([etype, FDR, p_value, FG_count], ascending=[False, True, True, False])
        df = pd.concat([df_rest, df_PMID], sort=False)
        # cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids', 'year']
        cols_sort_order = [term, hierarchical_level, p_value, FDR, category, etype, description, FG_count, FG_IDs, year]
    else:
        # df = df.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        df = df.sort_values([etype, FDR, p_value, FG_count], ascending=[False, True, True, False])
        # cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids']
        cols_sort_order = [term, hierarchical_level, p_value, FDR, category, etype, description, FG_count, FG_IDs]
    cols_sort_order += sorted(set(df.columns.tolist()) - set(cols_sort_order))
    return df[cols_sort_order]

def PMID_description_to_year(string_):
    try:
        return int(string_[1:5])
    except ValueError or IndexError:
        return np.nan

def format_results(df, output_format, args_dict):
    if output_format == "dataframe":
        return df
    elif output_format == "tsv":
        return df.to_csv(sep="\t", header=True, index=False)
    elif output_format == "tsv-no-header" or output_format == "tsv_no_header":
        return df.to_csv(sep="\t", header=False, index=False)
    elif output_format == "json":
        return json.dumps(df.to_dict(orient='records'))
    elif output_format == "xml": # xml gets formatted in runserver.py
        dict_2_return = {}
        for etype_, df_group in df.groupby(etype):
            results = df_group.to_csv(sep="\t", header=True, index=False)  # convert DatFrame to string
            header, rows = results.split("\n", 1)  # is df in tsv format
            xml_string = create_xml_tree(header, rows.split("\n"))
            dict_2_return[etype_] = xml_string.decode()
        return dict_2_return
    else:
        args_dict["ERROR output format"] = "output_format {} is unknown, please chose one of [tsv, tsv-no-header, json, xml] and try again".format(output_format)
        return False

def create_xml_tree(header, rows):
    xml_tree = etree.Element("EnrichmentResult")
    header = header.split("\t")
    for row in rows:
        child = etree.SubElement(xml_tree, "record")
        for tag_content in zip(header, row.split("\t")):
            tag, content = tag_content
            etree.SubElement(child, tag).text = content
    return etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")

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