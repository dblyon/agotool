from __future__ import print_function
import operator, os, sys
import pandas as pd

# debug
from collections import defaultdict

# import numpy as np
sys.path.append("./../metaprot/sql/")

# import query
import go_retriever
import enrichment
import userinput
import obo_parser
import cluster_filter
import tools


def run(go_dag, goslim_dag, upk_dag, ui, connection, gocat_upk, go_slim_or_basic, indent, multitest_method, alpha,
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
    assoc_dict = tools.get_association_dict(connection, protein_ans_list, function_type, limit_2_parent=limit_2_parent, basic_or_slim=go_slim_or_basic, backtracking=backtracking)
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

def run_old(proteinGroup, compare_groups, userinput_fn, study_n, pop_n, decimal,
            organism, gocat_upk, go_slim_or_basic, indent,
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
        ui = userinput.Userinput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)
    else:
        ui = userinput.Userinput_noAbCorr(userinput_fn, num_bins, col_sample_an, col_background_an, decimal)

    ### gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        assoc_dict = upkp.get_association_dict_from_organims(organism)
        gostudy = enrichment.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, randomSample, abcorr, o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected)
        return header, results
    else:
        assoc_dict = pgoa.get_association_dict(go_parent=gocat_upk, obo_dag=go_dag, ans_list=ans_list)
        if not gocat_upk == "KEGG":
            if go_slim_or_basic == 'slim':
                assoc_dict = go_retriever.gobasic2slims(assoc_dict, go_dag, goslim_dag, backtracking)
        if compare_groups == "characterize_study":
            gostudy = enrichment.GOEnrichmentStudy(proteinGroup, compare_groups, ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method, gocat_upk)
            return gostudy.GOid2NumANs_dict_study, gostudy.go2ans_study_dict
        elif compare_groups == "method":
            gostudy = enrichment.GOEnrichmentStudy(proteinGroup, compare_groups, ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method, gocat_upk)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
        return header, results


class get_startup_objects(object):
    ### Jan is so smart and nice, we love callable Classes
    def __init__(self):
        self.args = self.__get_startup_objects()

    def __call__(self):
        if self.args is not False:
            return self.args
        else:
            self.args = self.__get_startup_objects()
            return self.args

    def __get_startup_objects(self):
        # setting up objects
        decimal = '.'
        organism = None
        gocat_upk = 'all_GO' # "all_GO", "BP", "MF", "CP", "UPK", "KEGG"
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
        pgoa.fn_sqlite_kegg = r"/Users/dblyon/modules/cpr/metaprot/HOMD_AN2KEGGname.sqlite"
        filter_ = cluster_filter.Filter(go_dag)
        return go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent, multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking, fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, filter_


def GO_compare_groups(userinput_fn, go_slim_or_basic, proteinGroup, *args):
    go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent, multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking, fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, filter_ = args
    study_n = 10
    pop_n = 10
    compare_groups = "method"  # "characterize_study" or "method"
    header, results = run(proteinGroup, compare_groups, userinput_fn, study_n,
        pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
        go_dag, goslim_dag, pgoa, upkp)
    if gocat_upk == "KEGG":
        fn_out = userinput_fn.replace(".txt", "_compare_{}.txt".format(gocat_upk))
    else:
        fn_out = userinput_fn.replace(".txt", "_compare_{}.txt".format(go_slim_or_basic))
    if proteinGroup:
        fn_out = fn_out.replace(".txt","_protGr.txt")
    tsv = (u'%s\n%s\n' % (header, u'\n'.join(results)))
    write2file(fn_out, tsv)
    df = pd.read_csv(fn_out, sep='\t')
    if not gocat_upk == "KEGG": # filter results
        df['level'] = df["id"].apply(go_retriever.get_level, args=(go_dag, ))
    df['ANs_count'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
    print(fn_out)
    df.to_csv(fn_out, sep='\t', header=True, index=False)
    if not gocat_upk == "KEGG": # filter results
        fn_out_filtered = fn_out.replace('.txt', "_fltr.txt")
        results_filtered = filter_.filter_term_lineage(header, results, indent, sort_on='p_uncorrected')
        tsv = (u'%s\n%s\n' % (header, u'\n'.join(results_filtered)))
        print(fn_out_filtered)
        write2file(fn_out_filtered, tsv)


def GO_characterize_study(userinput_fn, go_slim_or_basic, proteinGroup, *args):
    go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent, multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking, fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, filter_ = args
    backtracking = True
    if gocat_upk == "KEGG":
        backtracking = False
    study_n = 10
    pop_n = 10
    compare_groups = "characterize_study"
    term_study, go2ans_study_dict = run(proteinGroup, compare_groups, userinput_fn, study_n,
        pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
        go_dag, goslim_dag, pgoa, upkp)
    basename_split = os.path.basename(userinput_fn).split("_")
    basename = "_".join([basename_split[0], basename_split[3]])
    fn_out = os.path.join(os.path.dirname(userinput_fn), basename)
    if proteinGroup:
        fn_out = fn_out.replace(".txt","_protGr.txt")
    sorted_term_study = sorted(term_study.items(), key=operator.itemgetter(1))[::-1]
    if not gocat_upk == "KEGG":
        fn_out = fn_out.replace(".txt", "_characterize_{}.txt".format(go_slim_or_basic))
        dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
        dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag,))
        dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag,))
    else:
        fn_out = fn_out.replace(".txt", "_characterize_{}.txt".format(gocat_upk))
        dfx = pd.DataFrame(sorted_term_study, columns=["KEGG", "Num_associations"])
    print(fn_out)
    dfx.to_csv(fn_out, sep='\t', header=True, index=False)


if __name__ == "__main__":
    ###  run GO enrichemnt and characterization
    list_of_tuple_combinations = [('Perio', 'Caries'), ('Perio', 'Healthy'), ('Caries', 'Healthy'), ('Healthy', 'Caries')]
    get_startup_objects = get_startup_objects()
    go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent, multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking, fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, filter_ = get_startup_objects()
    go_slim_or_basic = "slim"
    proteinGroup_list = [True] #, False] ##True]#, False]
    dir_ = r"/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_20160429_redFasta_FDR_matchBR/Intensity_Classic/"
    Homo_Bac_Other_list = ["Bacteria"]#, 'Homo']
    rank = 'genus'
    userinput_fn_list = []

    compare_groups = "characterize_study"
    study_n = 10
    pop_n = 10
    gocat_upk = "KEGG"
    backtracking = False


    for Homo_Bac_Other in Homo_Bac_Other_list:
        for combi in list_of_tuple_combinations:
            groupA, groupB = combi
            fn_out = "{}_vs_{}_{}{}.txt".format(groupA, groupB, Homo_Bac_Other, rank)
            fn_out = os.path.join(dir_, fn_out)
            userinput_fn_list.append(fn_out)
    for proteinGroup in proteinGroup_list:
        for userinput_fn in userinput_fn_list:
            GO_compare_groups(userinput_fn, go_slim_or_basic, proteinGroup,
                go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent,
                multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
                fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
                filter_)
            # print(userinput_fn)
            GO_characterize_study(userinput_fn, go_slim_or_basic, proteinGroup,
                go_dag, goslim_dag, upkp, pgoa, decimal, organism, gocat_upk, indent,
                multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
                fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
                filter_)







    # method = True
    # method = "method" # or "characterize_study"
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
    # fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/go-basic.obo'
    # go_dag = obo_parser.GODag(obo_file=fn_obo)
    # fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/goslim_generic.obo'
    # goslim_dag = obo_parser.GODag(obo_file=fn_obo)
    # upkp = go_retriever.UniProtKeywordsParser()
    # pgoa = go_retriever.Parser_GO_annotations()
    # pgoa.fn_sqlite = r'/Users/dblyon/modules/cpr/agotool/static/python/AN2GO_UniProt_HOMD.sqlite'

    ### Daniel saliva
    # fn = r'/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_Jesper/GOenr/ANs_bac_unique.txt'
    # df = pd.read_csv(fn, sep='\t')
    # ans_list = df["AN"].tolist()
    # assoc_dict = pgoa.get_association_dict(go_parent="all_GO", obo_dag=go_dag, ans_list=ans_list)

    # fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'
    #
    # foreground_n = 10.0
    # background_n = 10.0


    # header, results = run(proteinGroup, method, userinput_fn, foreground_n, background_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
    #     multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
    #     fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
    #     go_dag, goslim_dag, pgoa, upkp)


    ################################################################################
    ################################################################################
    ######### TESTING START
    ####### TESTING method and characterize_study
    ### Characterize_study (with GOenrichment_characterize_study_test_DF_v2.txt)
    # ABC123 * 8 (out of 10 samples)
    # BCD123 * 3 (out of 10 samples)
    # ABC123 associated with GOID1 and GOID2
    # BCD123 associated with GOID1 and GOID3
    # GOID1: 8 + 3 = 11 associations, and 2 number of ANs
    # GOID2: 8 = 8 associations, and 1 number of ANs
    # GOID3: 3 = 3 associations, and 1 number of ANs
    ### Compare_groups (with GOenrichment_characterize_study_test_DF_v2.txt)
    # foreground_count = counts total redundant (NON-unique) number of associations
    # foreground_n = number of unique ANs * sample size
    # ABC123 * 8 (out of 10 samples in study), ABC123 * 5 (out of 10 in population)
    # BCD123 * 3 (out of 10 samples), BCD123 * 1 (out of 10 study)
    # ABC123 associated with GOID1 and GOID2
    # BCD123 associated with GOID1 and GOID3
    #        foreground_count   foreground_n   background_count   background_n
    # GOID1: 8+3           2*10      5+1         2*10
    # GOID2: 8             1*10      5           1*10
    # GOID3: 3             1*10      1           1*10
    ################################################################################
    ################################################################################
    # # setting up objects
    # decimal = '.'
    # organism = None
    # gocat_upk = 'all_GO'
    # indent = False
    # multitest_method = 'benjamini_hochberg'
    # alpha = 0.05
    # o_or_u_or_both = 'both'
    # abcorr = False
    # num_bins = 100
    # backtracking = True
    # fold_enrichment_study2pop = 0.0
    # p_value_uncorrected = 0.0
    # p_value_mulitpletesting = 0.0
    # fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/go-basic.obo'
    # go_dag = obo_parser.GODag(obo_file=fn_obo)
    # fn_obo = r'/Users/dblyon/modules/cpr/agotool/static/data/OBO/goslim_generic.obo'
    # goslim_dag = obo_parser.GODag(obo_file=fn_obo)
    # upkp = go_retriever.UniProtKeywordsParser()
    # pgoa = go_retriever.Parser_GO_annotations()
    # pgoa.fn_sqlite = r'/Users/dblyon/modules/cpr/agotool/static/python/AN2GO_UniProt_HOMD.sqlite'
    # filter_ = cluster_filter.Filter(go_dag)
    ################################################################################
    ### Test 1
    # # TESTING method = characterize_study
    # foreground_n = 10
    # background_n = 10
    # method = "characterize_study"  # "characterize_study" or "method"
    # go_slim_or_basic = "slim"
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
    # proteinGroup = False
    # term_study, go2ans_study_dict = run(proteinGroup, method, userinput_fn,
    #                                         foreground_n, background_n, decimal, organism,
    #                                         gocat_upk, go_slim_or_basic, indent,
    #                                         multitest_method, alpha,
    #                                         o_or_u_or_both, abcorr, num_bins,
    #                                         backtracking,
    #                                         fold_enrichment_study2pop,
    #                                         p_value_uncorrected,
    #                                         p_value_mulitpletesting,
    #                                         go_dag, goslim_dag, pgoa, upkp)
    # sorted_term_study = sorted(term_study.items(), key=operator.itemgetter(1))[::-1]
    # dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    # dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag, ))
    # dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag, ))
    # assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    # print("test1 ")
    ################################################################################
    # # TESTING method = method
    # foreground_n = 10
    # background_n = 10
    # method = "method" # "characterize_study" or "method"
    # go_slim_or_basic = "slim"
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
    # proteinGroup = False
    # header, results = run(proteinGroup, method, userinput_fn, foreground_n, background_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
    #             multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
    #             fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
    #             go_dag, goslim_dag, pgoa, upkp)
    # fn_out = userinput_fn.replace(".txt", "_compare_groups_{}.txt".format(go_slim_or_basic))
    # fn_out_filtered = fn_out.replace('.txt', "_fltr.txt")
    # tsv = (u'%s\n%s\n' % (header, u'\n'.join(results)))
    # print(fn_out)
    # write2file(fn_out, tsv)
    # df = pd.read_csv(fn_out, sep='\t')
    # df['level'] = df["id"].apply(go_retriever.get_level, args=(go_dag, ))
    # df['ANs_count'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
    # df.to_csv(fn_out, sep='\t', header=True, index=False)
    # print(df.shape)
    # assert sorted(df.foreground_n.unique()) == [10, 20]
    # assert sorted(df.background_n.unique()) == [10, 20]
    # assert sorted(df.background_count.unique()) == [1, 5, 6]
    # assert sorted(df.foreground_count.unique()) == [3, 8, 11]
    # df['ANs_count_study'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
    # cond = df["foreground_n"] == df["ANs_count_study"] * foreground_n
    # assert sum(cond) == len(cond) # all are True
    # df['ANs_count_pop'] = df['ANs_pop'].apply(lambda x: len(x.split(",")))
    # cond = df["background_n"] == df["ANs_count"] * background_n
    # assert sum(cond) == len(cond)
    # df_characterize_study = dfx.copy()
    # df_compare_groups = df[["id", "foreground_count"]]
    # df_compare_groups.columns = ["GOid", "foreground_count"]
    # dfm = pd.merge(df_compare_groups, df_characterize_study, how='outer')
    # cond = dfm['foreground_count'] == dfm['Num_associations']
    # assert sum(cond) == len(cond)
    # print("test2 ")
    # ### Test 3
    # # TESTING method = characterize_study with proteinGroups
    # foreground_n = 10
    # background_n = 10
    # proteinGroup = True
    # method = "characterize_study"  # "characterize_study" or "method"
    # go_slim_or_basic = "slim"
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    # GOid2NumANs_dict_study, go2ans_study_dict = run(proteinGroup, method,
    #                                     userinput_fn,
    #                                     foreground_n, background_n, decimal, organism,
    #                                     gocat_upk, go_slim_or_basic, indent,
    #                                     multitest_method, alpha,
    #                                     o_or_u_or_both, abcorr, num_bins,
    #                                     backtracking,
    #                                     fold_enrichment_study2pop,
    #                                     p_value_uncorrected,
    #                                     p_value_mulitpletesting,
    #                                     go_dag, goslim_dag, pgoa, upkp)
    # sorted_term_study = sorted(GOid2NumANs_dict_study.items(), key=operator.itemgetter(1))[::-1]
    # dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    # dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag,))
    # dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag,))
    # assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    # print("test3 ")
    ### Test 4
    # # TESTING method = characterize_study
    # foreground_n = 10
    # background_n = 10
    # method = "characterize_study"  # "characterize_study" or "method"
    # go_slim_or_basic = "slim"
    # userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
    # proteinGroup = True
    # term_study, go2ans_study_dict = run(proteinGroup, method, userinput_fn,
    #                                         foreground_n, background_n, decimal, organism,
    #                                         gocat_upk, go_slim_or_basic, indent,
    #                                         multitest_method, alpha,
    #                                         o_or_u_or_both, abcorr, num_bins,
    #                                         backtracking,
    #                                         fold_enrichment_study2pop,
    #                                         p_value_uncorrected,
    #                                         p_value_mulitpletesting,
    #                                         go_dag, goslim_dag, pgoa, upkp)
    # sorted_term_study = sorted(term_study.items(), key=operator.itemgetter(1))[::-1]
    # dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
    # dfx['description'] = dfx["GOid"].apply(go_retriever.get_description, args=(go_dag, ))
    # dfx['level'] = dfx["GOid"].apply(go_retriever.get_level, args=(go_dag, ))
    # assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]
    # print("test4 ")
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