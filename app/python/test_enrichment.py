import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

import pytest
from collections import defaultdict

import variables, ratio, query, userinput, enrichment, run



def test_count_vs_n_size():
    """
    foreground_count <= foreground_n
    background_count <= background_n
    :return:
    """
    pass

def format_for_REST_API(list_of_string):
    return "%0d".join(list_of_string)

def test_count_terms_v3(random_foreground_background, pqo_STRING):
    """
    this test IS for ratio.count_terms_v3,
    since it is testing for the presence of secondary IDs
    # goterm: 'GO:0007610' has secondary id 'GO:0044708'
    :param random_foreground_background:
    :param pqo_STRING:
    :return:
    """
    foreground, background, taxid = random_foreground_background
    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    go_slim_or_basic = "basic"
    for entity_type in variables.entity_types_with_data_in_functions_table:
        obo_dag = run.pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo_STRING)
        assoc_dict = etype_2_association_dict_foreground[entity_type]
        for an in (AN for AN in set(foreground) if AN in assoc_dict):
            for association in assoc_dict[an]:
                association_id = obo_dag[association].id
                assert association_id == association

        association_2_count_dict_v2, association_2_ANs_dict_v2, ans_counter_v2 = ratio.count_terms_v2(set(background), assoc_dict, obo_dag)
        association_2_count_dict_v3, association_2_ANs_dict_v3, ans_counter_v3 = ratio.count_terms_v3(set(background), assoc_dict)
        assert association_2_count_dict_v2 == association_2_count_dict_v3
        assert association_2_count_dict_v2 == association_2_count_dict_v3
        assert ans_counter_v2 == ans_counter_v3

def test_EnrichmentStudy(random_foreground_background, pqo_STRING):
    """
    perc_association_foreground <= 100
    perc_asociation_background <= 100
    :return:
    """
    go_slim_or_basic = "basic"
    o_or_u_or_both = "overrepresented"
    multitest_method = "benjamini_hochberg"
    enrichment_method = "genome"

    fold_enrichment_study2pop = None
    p_value_mulitpletesting = None
    p_value_uncorrected = None
    indent = True

    foreground, background, taxid = random_foreground_background
    background_n = pqo_STRING.get_proteome_count_from_taxid(int(taxid))
    assert background_n == len(background)
    assert len(foreground) <= len(background)
    ui = userinput.REST_API_input(pqo_STRING,
        foreground_string=format_for_REST_API(foreground),
        background_string=format_for_REST_API(background),
        enrichment_method="genome", background_n=len(background))

    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    if enrichment_method == "genome":
        etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, _ = query.get_association_2_counts_split_by_entity(taxid)
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = run.pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo_STRING)
        assoc_dict = etype_2_association_dict_foreground[entity_type]
        if bool(assoc_dict): # not empty dictionary
            ### assoc_dict: remove ANs with empty set as values --> don't think this is necessary since these rows should not exist in DB
            # assoc_dict = {key: val for key, val in assoc_dict.items() if len(val) >= 1},
            if enrichment_method == "genome":
                enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag,
                    o_or_u_or_both=o_or_u_or_both,
                    multitest_method=multitest_method,
                    entity_type=entity_type,
                    association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type],
                    association_2_ANs_dict_background=etype_2_association_2_ANs_dict_background[entity_type],
                    background_n=background_n)
            else:
                enrichment_study = enrichment.EnrichmentStudy(ui=ui,
                    assoc_dict=assoc_dict,
                    dag=dag,
                    enrichment_method=enrichment_method,
                    o_or_u_or_both=o_or_u_or_both,
                    multitest_method=multitest_method,
                    entity_type=entity_type)
            header, results = enrichment_study.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
            # results_all_function_types[entity_type] = (header, results)
            ### entity_type, header, results
            header_split = header.split("\t")
            index_perc_associated_foreground = header_split.index("perc_associated_foreground")
            index_perc_associated_background = header_split.index("perc_associated_background")
            index_foreground_count = header_split.index("foreground_count")
            index_foreground_n = header_split.index("foreground_n")
            index_background_count = header_split.index("background_count")
            index_background_n = header_split.index("background_n")
            for row in results:
                row_split = row.split("\t")
                assert float(row_split[index_perc_associated_foreground]) <= 100
                assert float(row_split[index_perc_associated_background]) <= 100
                assert int(row_split[index_foreground_count]) <= int(row_split[index_foreground_n])
                assert int(row_split[index_background_count]) <= int(row_split[index_background_n])
                assert int(row_split[index_foreground_n]) <= int(row_split[index_background_n])
                assert background_n == int(row_split[index_background_n])

