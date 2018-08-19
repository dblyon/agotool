import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.realpath(__file__))))

# import pytest
# from collections import defaultdict
# import requests

import variables, ratio, query, userinput, enrichment, run


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
        assert association_2_ANs_dict_v2 == association_2_ANs_dict_v3
        assert ans_counter_v2 <= ans_counter_v3

def test_EnrichmentStudy_genome(random_foreground_background, pqo_STRING):
    """
    checking for non empty results dictionary
    perc_association_foreground <= 100
    perc_asociation_background <= 100
    foreground_count <= foreground_n
    background_count <= background_n
    :return:
    """
    go_slim_or_basic = "basic"
    o_or_u_or_both = "overrepresented"
    multitest_method = "benjamini_hochberg"
    output_format = "json"
    foreground, background, taxid = random_foreground_background
    background_n = pqo_STRING.get_proteome_count_from_taxid(int(taxid))
    assert background_n == len(background)
    assert len(foreground) <= len(background)
    ui = userinput.REST_API_input(pqo_STRING,
        foreground_string=format_for_REST_API(foreground),
        background_string=format_for_REST_API(background),
        enrichment_method="genome") #, background_n=len(background))
    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, _ = query.get_association_2_count_ANs_background_split_by_entity(taxid)
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = run.pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo_STRING)
        assoc_dict = etype_2_association_dict_foreground[entity_type]
        if bool(assoc_dict): # not empty dictionary
            enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag,
                o_or_u_or_both=o_or_u_or_both,
                multitest_method=multitest_method,
                entity_type=entity_type,
                association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type],
                background_n=background_n)
            result = enrichment_study.get_result(output_format)
            assert result # not an empty dict

def test_run_STRING_enrichment(pqo_STRING, STRING_examples):
    """
    checking that
    :param pqo_STRING:
    :param STRING_examples:
    :return:
    """
    ### STRING example #1
    # foreground = ['511145.b1260', '511145.b1261', '511145.b1262', '511145.b1263', '511145.b1264', '511145.b1812', '511145.b2551', '511145.b3117', '511145.b3360', '511145.b3772', '511145.b4388']
    # taxid = 511145
    foreground, taxid = STRING_examples
    background_n = pqo_STRING.get_proteome_count_from_taxid(taxid)
    ui = userinput.REST_API_input(pqo_STRING, foreground_string=format_for_REST_API(foreground),enrichment_method="genome", background_n=background_n)
    results_all_function_types = run.run_STRING_enrichment(pqo=pqo_STRING, ui=ui, taxid=taxid, background_n=background_n, output_format="json", FDR_cutoff=None)
    assert results_all_function_types  != {'message': 'Internal Server Error'}
    etypes = variables.entity_types_with_data_in_functions_table
    assert len(set(results_all_function_types.keys()).intersection(etypes)) == len(etypes)
    for _, result in results_all_function_types.items():
        # assert result is not empty
        assert result

def test_run_STRING_enrichment_genome(pqo_STRING, STRING_examples):
    ### STRING example #1
    # foreground = ['511145.b1260', '511145.b1261', '511145.b1262', '511145.b1263', '511145.b1264', '511145.b1812', '511145.b2551', '511145.b3117', '511145.b3360', '511145.b3772', '511145.b4388']
    # taxid = 511145
    foreground, taxid = STRING_examples
    background_n = pqo_STRING.get_proteome_count_from_taxid(taxid)
    ui = userinput.REST_API_input(pqo_STRING, foreground_string=format_for_REST_API(foreground),enrichment_method="genome", background_n=background_n)
    results_all_function_types = run.run_STRING_enrichment_genome(pqo=pqo_STRING, ui=ui, taxid=taxid, background_n=background_n, output_format="json", FDR_cutoff=None)
    assert results_all_function_types  != {'message': 'Internal Server Error'}
    etypes = variables.entity_types_with_data_in_functions_table
    assert len(set(results_all_function_types.keys()).intersection(etypes)) == len(etypes)

def test_EnrichmentStudy_(random_foreground_background, pqo_STRING):
    """
    perc_association_foreground <= 100
    perc_asociation_background <= 100
    foreground_count <= foreground_n
    background_count <= background_n
    :return:
    """
    go_slim_or_basic = "basic"
    o_or_u_or_both = "overrepresented"
    multitest_method = "benjamini_hochberg"
    output_format = "json"
    foreground, background, taxid = random_foreground_background
    background_n = pqo_STRING.get_proteome_count_from_taxid(int(taxid))
    assert background_n == len(background)
    assert len(foreground) <= len(background)
    ui = userinput.REST_API_input(pqo_STRING,
        foreground_string=format_for_REST_API(foreground),
        background_string=format_for_REST_API(background),
        enrichment_method="genome", background_n=len(background))
    etype_2_association_dict_foreground = pqo_STRING.get_association_dict_split_by_category(foreground)
    etype_2_association_2_count_dict_background, etype_2_association_2_ANs_dict_background, _ = query.get_association_2_count_ANs_background_split_by_entity(taxid)
    for entity_type in variables.entity_types_with_data_in_functions_table:
        dag = run.pick_dag_from_entity_type_and_basic_or_slim(entity_type, go_slim_or_basic, pqo_STRING)
        assoc_dict = etype_2_association_dict_foreground[entity_type]
        if bool(assoc_dict): # not empty dictionary
            enrichment_study = enrichment.EnrichmentStudy(ui, assoc_dict, dag,
                o_or_u_or_both=o_or_u_or_both,
                multitest_method=multitest_method,
                entity_type=entity_type,
                association_2_count_dict_background=etype_2_association_2_count_dict_background[entity_type],
                background_n=background_n)
            result = enrichment_study.get_result(output_format)
            assert result # not an empty dict
