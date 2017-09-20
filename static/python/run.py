from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import enrichment, tools, query


def run(go_dag, goslim_dag, upk_dag, ui, gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
        o_or_u_or_both, backtracking, fold_enrichment_study2pop,
        p_value_uncorrected, p_value_mulitpletesting):

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    protein_ans_list = ui.get_all_unique_ANs()
    function_type, limit_2_parent = get_function_type__and__limit_2_parent(gocat_upk)
    # print(gocat_upk, function_type, limit_2_parent)
    assoc_dict = query.get_association_dict(protein_ans_list, function_type, limit_2_parent=limit_2_parent, basic_or_slim=go_slim_or_basic, backtracking=backtracking)
    # now convert assoc_dict into proteinGroups to consensus assoc_dict
    proteinGroups_list = ui.get_all_unique_proteinGroups()
    assoc_dict_pg = tools.convert_assoc_dict_2_proteinGroupsAssocDict(assoc_dict, proteinGroups_list)
    assoc_dict.update(assoc_dict_pg)
    dag = pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, go_dag, goslim_dag, upk_dag)
    enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag, alpha, backtracking, o_or_u_or_both, multitest_method, gocat_upk)
    header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
    return header, results

def pick_dag_from_function_type_and_basic_or_slim(function_type, go_slim_or_basic, go_dag, goslim_dag, upk_dag):
    """
    :param function_type:
    :param go_slim_or_basic:
    :param go_dag:
    :param goslim_dag:
    :param upk_dag:
    :return:
    """
    if function_type == "GO":
        if go_slim_or_basic == "slim":
            return goslim_dag
        else:
            return go_dag
    elif function_type == "UPK":
        return upk_dag
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
    if gocat_upk in {"BP", "CP", "MF"}:
        return "GO", gocat_upk
    elif gocat_upk == "all_GO":
        return "GO", None
    else:
        return gocat_upk, None

def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)
