import goretriever, go_enrichment, obo_parser, userinput, uniprot_keywords, os

# webserver_data = home + r'/CloudStation/CPR/Brian_GO/webserver_data'

# key=TaxId, val=Dict {key=goa_ref_fn, uniprot_keywords_fn, val=rawString}


# (u'9606',  u'Homo sapiens'), # Human
# (u'4932',  u'Saccharomyces cerevisiae'), # Yeast
# (u'3702',  u'Arabidopsis thaliana'), # Arabidopsis
# (u'7955',  u'Danio rerio'), # Zebrafish
# (u'7227',  u'Drosophila melanogaster'), # Fly
# (u'9031',  u'Gallus gallus'), # Chicken
# (u'10090', u'Mus musculus'), # Mouse
# (u'10116', u'Rattus norvegicus'), # Rat
# (u'8364',  u'Xenopus (Silurana) tropicalis')] # Frog




def run(userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, species2files_dict, obo2file_dict):

    col_sample_an = "sample_an"
    col_background_an = 'population_an'
    col_background_int = 'population_int'

    o_or_u_or_both = o_or_u_or_both # e_or_p_or_both: is one of: 'enriched', 'purified', None
    decimal = decimal # is one of: "," or "."
    alpha = alpha

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

################################
#### constants

    randomSample = False
################################
    if abcorr:
        ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)
    else:
        ui = userinput.UserInput_noAbCorr(userinput_fn, num_bins, col_sample_an, col_background_an, decimal)
    # gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        uniprot_keywords_fn = species2files_dict[organism]["uniprot_keywords_fn"]
        assoc_dict = uniprot_keywords.UniProt_keywords_parser(uniprot_keywords_fn).get_association_dict()
        gostudy = go_enrichment.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, randomSample, abcorr, o_or_u_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected)
        return header, results
    else:
        goa_ref_fn = species2files_dict[organism]["goa_ref_fn"]
        go_parent = gocat_upk
        go_dag = obo_parser.GODag(obo_file=obo2file_dict['basic'])
        assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict(go_parent, go_dag)
        if go_slim_or_basic == 'slim':
            goslim_dag = obo_parser.GODag(obo_file=obo2file_dict['slim'])
            assoc_dict_slim = goretriever.gobasic2slims(assoc_dict, go_dag, goslim_dag, backtracking)
            gostudy = go_enrichment.GOEnrichmentStudy(ui, assoc_dict_slim, goslim_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method) #!!!
        else:
            gostudy = go_enrichment.GOEnrichmentStudy(ui, assoc_dict, go_dag, alpha, backtracking, randomSample, abcorr, o_or_u_or_both, multitest_method) #!!!
        header, results = gostudy.write_summary2file_web(fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
        return header, results


if __name__ == "__main__":
    organism = "4932"
    # userinput_file = species2files_dict[organism]["userinput_fn"]
    # userinput_fn = r'/Users/dblyon/Downloads/yeast_observed_acetyl_abundance.txt'
    # userinput_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/webserver_data/userdata/hela_observed_acetyl_abundance.txt'
    userinput_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/webserver_data/userdata/yeast_observed_acetyl_abundance.txt'
    decimal = ','
    gocat_upk = 'all_GO'

    go_slim_or_basic = 'slim'
    backtracking = True

    indent = True
    multitest_method = 'benjamini_hochberg'
    alpha = 0.05
    o_or_u_or_both = 'both'
    abcorr = True
    num_bins = 100
    fold_enrichment_study2pop = 0
    p_value_uncorrected = 0
    p_value_mulitpletesting = 0

    species2files_dict = {'10090': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_mouse',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Mouse_uniprot-proteome%3AUP000000589.tab'},
 '10116': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_rat',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Rat_uniprot-proteome%3AUP000002494.tab'},
 '3702': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_arabidopsis',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Arabidopsis_uniprot-proteome%3AUP000006548.tab'},
 '4932': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_yeast',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Yeast_uniprot-proteome%3AUP000002311.tab'},
 '7227': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_fly',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Fly_uniprot-proteome%3AUP000000803.tab'},
 '7955': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_zebrafish',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Zebrafish_uniprot-proteome%3AUP000000437.tab'},
 '8364': {'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Frog_uniprot-proteome%3AUP000008143.tab'},
 '9031': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_chicken',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Chicken_uniprot-proteome%3AUP000000539.tab'},
 '9606': {'goa_ref_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/GOA/gene_association.goa_human',
  'uniprot_keywords_fn': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/UniProt_Keywords/Human_uniprot-proteome%3AUP000005640.tab'}}

    obo2file_dict = {'basic': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/OBO/go-basic.obo',
        'slim': '/Users/dblyon/modules/cpr/goterm/agotool/static/data/OBO/goslim_generic.obo'}


    header, results = run(userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
            multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
            fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, species2files_dict, obo2file_dict)







