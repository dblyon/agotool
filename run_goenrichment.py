import goretriever, go_enrichment_dbl, obo_parser, os
# find_enrichment_dbl
# import pandas as pd
# import numpy as np

__author__ = 'dblyon'




if __name__ == '__main__':
    #!!! don't run this for every analysis. check organism here!!!
    # required, and regularly updated
    goa_ref_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
    obo_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo'
    # obo_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/go_obo/goslim_generic.obo'
    obo_dag = obo_parser.GODag(obo_file=obo_fn)
    assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict()

    userinput_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/UserInput.txt'
    # userinput_fn = home + r'/modules/cpr/goterm/test/UserInput_test2.txt'

    ui = goretriever.UserInput()
    home = os.path.expanduser('~')

    randomSample = False
    backtracking = True
    num_bins = 100
    alpha = 0.05
    # "Test-wise alpha for multiple testing"
    pval = None
    # "Family-wise alpha (whole experiment), only print out "
    # "Bonferroni p-value is less than this value. "
    compare = False
    # "the population file as a comparison group. if this "
    # "flag is specified, the population is used as the study "
    # "plus the `population/comparison`"
    min_ratio = None
    # "only show values where the difference between study "
    # "and population ratios is greater than this. useful for "
    # "excluding GO categories with small differences, but "
    # "containing large numbers of genes. should be a value "
    # "between 1 and 2. "
    fdr = False
    # "Calculate the false discovery rate (alt. to the "
    # "Bonferroni but slower)"
    indent = True
    # "indent GO terms"
    methods = ["bonferroni", "sidak", "holm", "benjamini_hochberg"]
    # do stuff depending on settings
    if fdr:
        methods.append("fdr")
    # check parameters
    if min_ratio is not None:
        assert 1 <= min_ratio <= 2
    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    # for i in range(1,11):
    #     fn_out = 'SummaryTest_yeast_acetyl_randomSample_v' + str(i) + '.txt'

    fn_out = 'SummaryTest_yeast_acetyl_AbundanceCorrected.txt'
    ui = goretriever.UserInput(userinput_fn, num_bins) # adapt UserInput to process web input etc.
    gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample)
    results = gostudy.run_study()
    gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)





    ##### Parameters from User
    # Sample frequency IDs: List of AccessionNumbers
    # Background frequency IDs: List of AccessionNumbers
    # Background frequency abundance: corresponding List of Intensities
    # organism = 'yeast' # Saccharomyces cerevisiae, HeLa, etc.
    # --> generate study_fn, population_fn
    # study_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/study_test4.txt'
    # population_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast_test4.txt'
    # study_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/study_yeast_acetyl.txt'
    # population_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast_obsProteome.txt'
    # association_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/association_goa_yeast'






