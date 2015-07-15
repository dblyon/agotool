import go_retriever
import go_enrichment
import userinput


def run(userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
        species2files_dict, go_dag, goslim_dag):

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

    if abcorr:
        ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an,
                                 col_background_an, col_background_int, decimal)
    else:
        ui = userinput.UserInput_noAbCorr(
            userinput_fn, num_bins, col_sample_an, col_background_an, decimal)
    # gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        uniprot_keywords_fn = species2files_dict[organism]["uniprot_keywords_fn"]
        assoc_dict = go_retriever.UniProtKeywordsParser(
            uniprot_keywords_fn).get_association_dict()
        gostudy = go_enrichment.GOEnrichmentStudy_UPK(
            ui, assoc_dict, alpha, randomSample, abcorr, o_or_u_or_both,
            multitest_method)
        header, results = gostudy.write_summary2file_web(
            fold_enrichment_study2pop, p_value_mulitpletesting,
            p_value_uncorrected)
    else:
        goa_ref_fn = species2files_dict[organism]["goa_ref_fn"]
        go_parent = gocat_upk
        assoc_dict = go_retriever.Parser_UniProt_goa_ref(
            goa_ref_fn = goa_ref_fn).get_association_dict(go_parent, go_dag)
        if go_slim_or_basic == 'slim':
            assoc_dict_slim = go_retriever.gobasic2slims(
                assoc_dict, go_dag, goslim_dag, backtracking)
            gostudy = go_enrichment.GOEnrichmentStudy(
                ui, assoc_dict_slim, goslim_dag, alpha, backtracking,
                randomSample, abcorr, o_or_u_or_both, multitest_method)
        else:
            gostudy = go_enrichment.GOEnrichmentStudy(
                ui, assoc_dict, go_dag, alpha, backtracking, randomSample,
                abcorr, o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(
            fold_enrichment_study2pop, p_value_mulitpletesting,
            p_value_uncorrected, indent)

    return header, results


