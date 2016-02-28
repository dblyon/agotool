import go_retriever
import go_enrichment
import userinput
import pandas as pd
import obo_parser


def run(compare_groups, userinput_fn, study_n, pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
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
        ui = userinput.UserInput_compare_groups(userinput_fn, study_n, pop_n)
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
            assoc_dict_slim = go_retriever.gobasic2slims(assoc_dict, go_dag, goslim_dag, backtracking)
            gostudy = go_enrichment.GOEnrichmentStudy(ui, assoc_dict_slim, goslim_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method)
        else: # compare_groups
            gostudy = go_enrichment.GOEnrichmentStudy(compare_groups, ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr,
                                                      o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)

    return header, results
    # return gostudy


if __name__ == "__main__":
    compare_groups = True
    decimal = '.'
    organism = None
    gocat_upk = 'all_GO'
    go_slim_or_basic = 'basic'
    indent = True
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

    ### Daniel saliva
    # fn = r'/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_Jesper/GOenr/ANs_bac_unique.txt'
    # df = pd.read_csv(fn, sep='\t')
    # ans_list = df["AN"].tolist()
    # assoc_dict = pgoa.get_association_dict(go_parent="all_GO", obo_dag=go_dag, ans_list=ans_list)

    fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_CH_Bacteria.txt'
    userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/CompareGroups_test.txt'

    study_n = 10.0
    pop_n = 20.0


    header, results = run(compare_groups, userinput_fn, study_n, pop_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
        go_dag, goslim_dag, pgoa, upkp)


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