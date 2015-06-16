import goretriever, go_enrichment_dbl, obo_parser, os, userinput, uniprot_keywords

home = os.path.expanduser('~')

# key=TaxId, val=Dict {key=goa_ref_fn, uniprot_keywords_fn, val=rawString}
species2files_dict = {"9606":
                          {'goa_ref_fn': home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/human/gene_association.goa_ref_human',
                           'uniprot_keywords_fn': home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/keywords/UniProt_HomoSapiens_Keywords_20150611.tab',
                           'userinput_fn': home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_HeLa_v2.txt'},
                      "4932":
                      {'goa_ref_fn': home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast',
                           'uniprot_keywords_fn': home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/keywords/UniProt_SaccharomycesCerevisiae_Keywords_20150611.tab',
                           'userinput_fn': home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_Yeast_v2.txt'}
                      }

obo2file_dict = {"slims": home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/goslim_generic.obo',
                 "basic": home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo'}

# (u'9606',  u'Homo sapiens'),
# (u'10090', u'Mus musculus'),
# (u'10116', u'Rattus norvegicus'),
# (u'4932',  u'Saccharomyces cerevisiae'),
# (u'7227',  u'Drosophila melanogaster'),
# (u'7955',  u'Danio rerio'),
# (u'9031',  u'Gallus gallus'),
# (u'8364',  u'Xenopus (Silurana) tropicalis')

def run(userinput_file, decimal, organism,
        gocat_upk, go_slims_or_basic, indent,
        correction_method, alpha, e_or_p_or_both, p_value, minimum_ratio, abcorr):

    # # fh = open(userinput_file, 'r')
    # print "####################################"
    # print type(userinput_file)
    # print userinput_file
    # print str(userinput_file)
    # print "####################################"
    # with open("ABC_parameters.txt", 'w') as fh:
    #     for par in [decimal, userinput_file, organism,
    #                 categories, go_slims_or_basic, indent,
    #                 correction_method, alpha, e_or_p_or_both, p_value, minimum_ratio]:
    #         fh.write(str(par) + '\n')
    #         print str(par)



    fn_out = "AAA111_webserver_output_test.txt"
    abcorr = abcorr
    e_or_p_or_both = e_or_p_or_both # e_or_p_or_both: is one of: 'enriched', 'purified', None
    decimal = decimal # is one of: "," or "."
    alpha = alpha
    pval = p_value
    if pval == 0:
        pval = None
    min_ratio = minimum_ratio
    # check parameters
    if min_ratio == 0:
        min_ratio = None
    if min_ratio is not None:
        assert 1 <= min_ratio <= 2
    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    indent = indent
    methods = [correction_method] #
    # methods = ["bonferroni", "sidak", "holm", "benjamini_hochberg"]
################################
#### constants
    backtracking = True
    num_bins = 100
    randomSample = False
################################

    userinput_fn = species2files_dict[organism]["userinput_fn"]
    col_background_an = 'Observed Proteome'
    col_sample_an = "Acetyl"
    col_background_int = 'iBAQ observed (log10)'
    ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)

    # gocat_upk is one of: 'MF', 'BP', 'CP', "all_GO", "UPK"
    if gocat_upk == "UPK":
        uniprot_keywords_fn = species2files_dict[organism]["uniprot_keywords_fn"]
        assoc_dict = uniprot_keywords.UniProt_keywords_parser(uniprot_keywords_fn).get_association_dict()
        gostudy = go_enrichment_dbl.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, methods, randomSample, abcorr, e_or_p_or_both)
        gostudy.write_summary2file(fn_out, min_ratio=min_ratio, pval=pval)
    else:
        goa_ref_fn = species2files_dict[organism]["goa_ref_fn"]
        obo_fn = obo2file_dict[go_slims_or_basic]
        obo_dag = obo_parser.GODag(obo_file=obo_fn)
        go_parent = gocat_upk
        assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict(go_parent, obo_dag)
        gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr, e_or_p_or_both)
        gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)



