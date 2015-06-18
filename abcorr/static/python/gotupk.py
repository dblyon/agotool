import goretriever, go_enrichment_dbl, obo_parser, os, userinput, uniprot_keywords

home = os.path.expanduser('~')
webserver_data = home + r'/CloudStation/CPR/Brian_GO/webserver_data'

# key=TaxId, val=Dict {key=goa_ref_fn, uniprot_keywords_fn, val=rawString}
species2files_dict = {"9606":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_human',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Human_uniprot-proteome%3AUP000005640.tab'},
                      "4932":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_yeast',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Yeast_uniprot-proteome%3AUP000002311.tab'},
                      "3702":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_arabidopsis',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Arabidopsis_uniprot-proteome%3AUP000006548.tab'},
                      "7955":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_zebrafish',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Zebrafish_uniprot-proteome%3AUP000000437.tab'},
                      "7227":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_fly',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Fly_uniprot-proteome%3AUP000000803.tab'},
                      "9031":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_chicken',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Chicken_uniprot-proteome%3AUP000000539.tab'},
                      "10090":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_mouse',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Mouse_uniprot-proteome%3AUP000000589.tab'},
                      "10116":
                          {'goa_ref_fn': webserver_data + r'/GOA/gene_association.goa_rat',
                           'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Rat_uniprot-proteome%3AUP000002494.tab'},
                      "8364":
                          {'uniprot_keywords_fn': webserver_data + r'/UniProt_Keywords/Frog_uniprot-proteome%3AUP000008143.tab'}
                      }

obo2file_dict = {"slims": webserver_data + r'/OBO/goslim_generic.obo',
                 "basic": webserver_data + r'/OBO/go-basic.obo'}

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
        multitest_method, alpha, e_or_p_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting):

    # # fh = open(userinput_file, 'r')
    # print "####################################"
    # print type(userinput_file)
    # print userinput_file
    # print str(userinput_file)
    # print userinput_file.__dict__
    print "####################################"
    varnames = ['userinput_fn','decimal','organism','gocat_upk',
                'go_slim_or_basic','indent','multitest_method','alpha',
                'e_or_p_or_both','abcorr','num_bins','backtracking',
                'fold_enrichment_study2pop','p_value_uncorrected','p_value_mulitpletesting']
    vars = [userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, e_or_p_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting]
    for varname, var in zip(varnames, vars) :
            print varname, ": ", str(var), type(var)
    print "####################################"

    fn_out = home + r'/CloudStation/CPR/Brian_GO/webserver_data/userdata/results.txt'


    # col_background_an = 'Observed Proteome'
    # col_sample_an = "Acetyl"
    # col_background_int = 'iBAQ observed (log10)'

    col_sample_an = "sample_an"
    col_background_an = 'background_an'
    col_background_int = 'background_int'
    # background_int	background_an	sample_an

    e_or_p_or_both = e_or_p_or_both # e_or_p_or_both: is one of: 'enriched', 'purified', None
    decimal = decimal # is one of: "," or "."
    alpha = alpha
    # pval = p_value
    # if pval == 0:
    #     pval = None

    if fold_enrichment_study2pop == 0:
        fold_enrichment_study2pop = None
    if p_value_mulitpletesting == 0:
        p_value_mulitpletesting = None
    if p_value_uncorrected == 0:
        p_value_uncorrected = None

    min_ratio = None
    # min_ratio = minimum_ratio
    # check parameters
    # if min_ratio == 0:
    #     min_ratio = None
    # if min_ratio is not None:
    #     assert 1 <= min_ratio <= 2
    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    # multitest_method is one of "bonferroni", "sidak", "holm" # "benjamini_hochberg", "fdr"
    # backtracking = backtracking
    # num_bins = num_bins
    # indent = indent
    # abcorr = abcorr

################################
#### constants

    randomSample = False
################################
    print(userinput_fn)
    try:
        if os.path.isfile(userinput_fn):
            userinput_fn = userinput_fn
    except:
        userinput_fn = species2files_dict[organism]["userinput_fn"]

    print(userinput_fn)
    if abcorr:
        ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)
    else:
        ui = userinput.UserInput_noAbCorr(userinput_fn, num_bins, col_sample_an, col_background_an, decimal)

    # gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        uniprot_keywords_fn = species2files_dict[organism]["uniprot_keywords_fn"]
        assoc_dict = uniprot_keywords.UniProt_keywords_parser(uniprot_keywords_fn).get_association_dict()
        gostudy = go_enrichment_dbl.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, randomSample, abcorr, e_or_p_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fn_out, fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected)
        return header, results
    else:
        goa_ref_fn = species2files_dict[organism]["goa_ref_fn"]
        obo_fn = obo2file_dict[go_slim_or_basic]
        obo_dag = obo_parser.GODag(obo_file=obo_fn)
        go_parent = gocat_upk
        assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict(go_parent, obo_dag)
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, backtracking, randomSample, abcorr, e_or_p_or_both, multitest_method)
        header, results = gostudy.write_summary2file_web(fn_out, fold_enrichment_study2pop, p_value_mulitpletesting, p_value_uncorrected, indent)
        return header, results


if __name__ == "__main__":
    organism = "4932"
    # userinput_file = species2files_dict[organism]["userinput_fn"]
    userinput_file = r'/Users/dblyon/Downloads/yeast_observed_acetyl_abundance.txt'
    decimal = ','
    gocat_upk = 'UPK'
    go_slim_or_basic = 'basic'
    indent = True
    multitest_method = 'benjamini_hochberg'
    alpha = 0.05
    e_or_p_or_both = 'both'
    abcorr = True
    num_bins = 100
    backtracking = True
    fold_enrichment_study2pop = 0
    p_value_uncorrected = 0
    p_value_mulitpletesting = 0

    run(userinput_file, decimal, organism, gocat_upk, go_slim_or_basic, indent,
        multitest_method, alpha, e_or_p_or_both, abcorr, num_bins, backtracking,
        fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting)









