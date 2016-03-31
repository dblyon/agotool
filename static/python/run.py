from __future__ import print_function
import operator
import pandas as pd
import numpy as np

import go_retriever
import go_enrichment
import userinput
import obo_parser
import cluster_filter


def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)

def run(proteinGroup, compare_groups, userinput_fn, study_n, pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
        go_dag, goslim_dag, pgoa, upkp):

    col_sample_an = "sample_an"
    col_background_an = 'population_an'
    col_background_int = 'population_int'

    randomSample = False

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    if compare_groups:
        ui = userinput.UserInput_compare_groups(proteinGroup, userinput_fn, study_n, pop_n)
        ans_list = ui.get_all_unique_ans()
    elif abcorr:
        ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)
    else:
        ui = userinput.UserInput_noAbCorr(userinput_fn, num_bins, col_sample_an, col_background_an, decimal)

    ### gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        assoc_dict = upkp.get_association_dict_from_organims(organism)
        gostudy = go_enrichment.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, randomSample, abcorr, o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected)
    else:
        go_parent = gocat_upk
        # assoc_dict = pgoa.get_association_dict_for_organism(go_parent=go_parent, obo_dag=go_dag, organism=organism)
        assoc_dict = pgoa.get_association_dict(go_parent=go_parent, obo_dag=go_dag, ans_list=ans_list)
        if go_slim_or_basic == 'slim':
            assoc_dict = go_retriever.gobasic2slims(assoc_dict, go_dag, goslim_dag, backtracking)
            # gostudy = go_enrichment.GOEnrichmentStudy(ui, assoc_dict_slim, goslim_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method)
        # gostudy = go_enrichment.GOEnrichmentStudy(compare_groups, ui, assoc_dict_slim, goslim_dag, alpha, backtracking, randomSample, abcorr,
        #                                               o_or_u_or_both, multitest_method)

        if compare_groups == "characterize_study":
            gostudy = go_enrichment.GOEnrichmentStudy(proteinGroup, compare_groups, ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method)
            return gostudy.GOid2NumANs_dict_study, gostudy.go2ans_study_dict
        elif compare_groups == "compare_groups":
            gostudy = go_enrichment.GOEnrichmentStudy(proteinGroup, compare_groups, ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr,
                                                  o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
    return header, results


if __name__ == "__main__":
    # compare_groups = True
    # compare_groups = "compare_groups" # or "characterize_study"
    # proteinGroup = True # ANs are provided as proteinGroups not single ANs, use all GOterms associated with the group but count only as one protein for stats
    # decimal = '.'
    # organism = None
    # gocat_upk = 'all_GO'
    # go_slim_or_basic = 'basic'
    # indent = True
    # multitest_method = 'benjamini_hochberg'
    # alpha = 0.05
    # o_or_u_or_both = 'both'
    # abcorr = False
    # num_bins = 100
    # backtracking = True
    # fold_enrichment_study2pop = 0.0
    # p_value_uncorrected = 0.0
    # p_value_mulitpletesting = 0.0
    fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/go-basic.obo'
    go_dag = obo_parser.GODag(obo_file=fn_obo)
    fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/goslim_generic.obo'
    goslim_dag = obo_parser.GODag(obo_file=fn_obo)
    upkp = go_retriever.UniProtKeywordsParser()
    pgoa = go_retriever.Parser_GO_annotations()
    pgoa.fn_sqlite = r'/Users/dblyon/modules/cpr/agotool/static/python/AN2GO_UniProt_HOMD.sqlite'

    ### Daniel saliva
    # fn = r'/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_Jesper/GOenr/ANs_bac_unique.txt'
    # df = pd.read_csv(fn, sep='\t')
    # ans_list = df["AN"].tolist()
    # assoc_dict = pgoa.get_association_dict(go_parent="all_GO", obo_dag=go_dag, ans_list=ans_list)

    # fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'
    #
    # study_n = 10.0
    # pop_n = 10.0


    # header, results = run(proteinGroup, compare_groups, userinput_fn, study_n, pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
    #     multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
    #     fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
    #     go_dag, goslim_dag, pgoa, upkp)


    ################################################################################
    ################################################################################
    ######### TESTING START
    ####### TESTING compare_groups and characterize_study
    ### Characterize_study (with GOenrichment_characterize_study_test_DF_v2.txt)
    # ABC123 * 8 (out of 10 samples)
    # BCD123 * 3 (out of 10 samples)
    # ABC123 associated with GOID1 and GOID2
    # BCD123 associated with GOID1 and GOID3
    # GOID1: 8 + 3 = 11 associations, and 2 number of ANs
    # GOID2: 8 = 8 associations, and 1 number of ANs
    # GOID3: 3 = 3 associations, and 1 number of ANs
    ### Compare_groups (with GOenrichment_characterize_study_test_DF_v2.txt)
    # study_count = counts total redundant (NON-unique) number of associations
    # study_n = number of unique ANs * sample size
    # ABC123 * 8 (out of 10 samples in study), ABC123 * 5 (out of 10 in population)
    # BCD123 * 3 (out of 10 samples), BCD123 * 1 (out of 10 study)
    # ABC123 associated with GOID1 and GOID2
    # BCD123 associated with GOID1 and GOID3
    #        study_count   study_n   pop_count   pop_n
    # GOID1: 8+3           2*10      5+1         2*10
    # GOID2: 8             1*10      5           1*10
    # GOID3: 3             1*10      1           1*10
    ################################################################################
    ################################################################################
    # setting up objects
    decimal = '.'
    organism = None
    gocat_upk = 'all_GO'
    indent = False
    multitest_method = 'benjamini_hochberg'
    alpha = 0.05
    o_or_u_or_both = 'both'
    abcorr = False
    num_bins = 100
    backtracking = True
    fold_enrichment_study2pop = 0.0
    p_value_uncorrected = 0.0
    p_value_mulitpletesting = 0.0
    fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/go-basic.obo'
    go_dag = obo_parser.GODag(obo_file=fn_obo)
    fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/goslim_generic.obo'
    goslim_dag = obo_parser.GODag(obo_file=fn_obo)
    upkp = go_retriever.UniProtKeywordsParser()
    pgoa = go_retriever.Parser_GO_annotations()
    pgoa.fn_sqlite = r'/Users/dblyon/modules/cpr/agotool/static/python/AN2GO_UniProt_HOMD.sqlite'
    filter_ = cluster_filter.Filter(go_dag)
    ################################################################################
    ### Test 1
    # TESTING compare_groups = characterize_study
    study_n = 10
    pop_n = 10
    compare_groups = "characterize_study"  # "characterize_study" or "compare_groups"
    go_slim_or_basic = "slim"
    userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
    proteinGroup = False
    term_study, go2ans_study_dict = run(proteinGroup, compare_groups, userinput_fn,
                                            study_n, pop_n, decimal, organism,
                                            gocat_upk, go_slim_or_basic, indent,
                                            multitest_method, alpha,
                                            o_or_u_or_both, abcorr, num_bins,
                                            backtracking,
                                            fold_enrichment_study2pop,
                                            p_value_uncorrected,
                                            p_value_mulitpletesting,
                                            go_dag, goslim_dag, pgoa, upkp)
    sorted_term_study = sorted(term_study.items(), key=operator.itemgetter(1))[::-1]
    dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag, ))
    dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag, ))
    assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    ################################################################################
    # TESTING compare_groups = compare_groups
    study_n = 10
    pop_n = 10
    compare_groups = "compare_groups" # "characterize_study" or "compare_groups"
    go_slim_or_basic = "slim"
    userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
    proteinGroup = False
    header, results = run(proteinGroup, compare_groups, userinput_fn, study_n, pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
                multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
                fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
                go_dag, goslim_dag, pgoa, upkp)
    fn_out = userinput_fn.replace(".txt", "_compare_groups_{}.txt".format(go_slim_or_basic))
    fn_out_filtered = fn_out.replace('.txt', "_fltr.txt")
    tsv = (u'%s\n%s\n' % (header, u'\n'.join(results)))
    print(fn_out)
    write2file(fn_out, tsv)
    df = pd.read_csv(fn_out, sep='\t')
    df['level'] = df["id"].apply(go_retriever.get_level, args=(go_dag, ))
    df['ANs_count'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
    df.to_csv(fn_out, sep='\t', header=True, index=False)
    print(df.shape)
    assert sorted(df.study_n.unique()) == [10, 20]
    assert sorted(df.pop_n.unique()) == [10, 20]
    assert sorted(df.pop_count.unique()) == [1, 5, 6]
    assert sorted(df.study_count.unique()) == [3, 8, 11]
    df['ANs_count_study'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
    cond = df["study_n"] == df["ANs_count_study"] * study_n
    assert sum(cond) == len(cond) # all are True
    df['ANs_count_pop'] = df['ANs_pop'].apply(lambda x: len(x.split(",")))
    cond = df["pop_n"] == df["ANs_count"] * pop_n
    assert sum(cond) == len(cond)
    df_characterize_study = dfx.copy()
    df_compare_groups = df[["id", "study_count"]]
    df_compare_groups.columns = ["GOid", "study_count"]
    dfm = pd.merge(df_compare_groups, df_characterize_study, how='outer')
    cond = dfm['study_count'] == dfm['Num_associations']
    assert sum(cond) == len(cond)

    ### Test 3
    # TESTING compare_groups = characterize_study with proteinGroups
    study_n = 10
    pop_n = 10
    proteinGroup = True
    compare_groups = "characterize_study"  # "characterize_study" or "compare_groups"
    go_slim_or_basic = "slim"
    userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    GOid2NumANs_dict_study, go2ans_study_dict = run(proteinGroup, compare_groups,
                                        userinput_fn,
                                        study_n, pop_n, decimal, organism,
                                        gocat_upk, go_slim_or_basic, indent,
                                        multitest_method, alpha,
                                        o_or_u_or_both, abcorr, num_bins,
                                        backtracking,
                                        fold_enrichment_study2pop,
                                        p_value_uncorrected,
                                        p_value_mulitpletesting,
                                        go_dag, goslim_dag, pgoa, upkp)
    sorted_term_study = sorted(GOid2NumANs_dict_study.items(), key=operator.itemgetter(1))[::-1]
    dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag,))
    dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag,))
    assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    ### Test 4
    # TESTING compare_groups = characterize_study
    study_n = 10
    pop_n = 10
    compare_groups = "characterize_study"  # "characterize_study" or "compare_groups"
    go_slim_or_basic = "slim"
    userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    proteinGroup = True
    term_study, go2ans_study_dict = run(proteinGroup, compare_groups, userinput_fn,
                                            study_n, pop_n, decimal, organism,
                                            gocat_upk, go_slim_or_basic, indent,
                                            multitest_method, alpha,
                                            o_or_u_or_both, abcorr, num_bins,
                                            backtracking,
                                            fold_enrichment_study2pop,
                                            p_value_uncorrected,
                                            p_value_mulitpletesting,
                                            go_dag, goslim_dag, pgoa, upkp)
    sorted_term_study = sorted(term_study.items(), key=operator.itemgetter(1))[::-1]
    dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag, ))
    dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag, ))
    assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    ######### TESTING STOP
    ################################################################################
    ################################################################################


    # userinput_fn=r'/Users/dblyon/modules/cpr/goterm/agotool/static/data/exampledata/exampledata.txt'
    # decimal = ','
    # organism = '559292' #organism = '4932'
    # gocat_upk = 'all_GO'
    # go_slim_or_basic = 'basic'
    # indent = True
    # multitest_method = 'benjamini_hochberg'
    # alpha = 0.05
    # o_or_u_or_both = 'both'
    # abcorr = True
    # num_bins = 100
    # backtracking = True
    # fold_enrichment_study2pop = 0.0
    # p_value_uncorrected = 0.0
    # p_value_mulitpletesting = 0.0
    # species2files_dict = {'10116': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/10116.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/10116.tsv'}, '4932': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/4932.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/4932.tsv'}, '9031': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/9031.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/9031.tsv'}, '7227': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/7227.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/7227.tsv'}, '9606': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/9606.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/9606.tsv'}, '3702': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/3702.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/3702.tsv'}, '10090': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/10090.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/10090.tsv'}, '7955': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/7955.tab', 'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/7955.tsv'}}
    # obo2file_dict = {"slim": r'/Users/dblyon/modules/cpr/goterm/agotool/static/data/OBO/goslim_generic.obo',
    #                  "basic": r'/Users/dblyon/modules/cpr/goterm/agotool/static/data/OBO/go-basic.obo'}
    # go_dag = obo_parser.GODag(obo_file=obo2file_dict['basic'])
    # goslim_dag = obo_parser.GODag(obo_file=obo2file_dict['slim'])
    #
    # run(userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
    #     multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
    #     fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
    #     species2files_dict, go_dag, goslim_dag)