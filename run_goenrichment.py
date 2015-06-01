import goretriever, find_enrichment_dbl, go_enrichment_dbl, obo_parser
# import pandas as pd
# import numpy as np

__author__ = 'dblyon'




if __name__ == '__main__':
    ui = goretriever.UserInput()

    ##### Parameters from User
    # Sample frequency IDs: List of AccessionNumbers
    # Background frequency IDs: List of AccessionNumbers
    # Background frequency abundance: corresponding List of Intensities
    # organism = 'yeast' # Saccharomyces cerevisiae, HeLa, etc.
    # --> generate study_fn, population_fn

    userinput_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/UserInput.txt'
    fn_out = 'SummaryTest_yeast_acetyl_AbCorr_noBacktracking.txt'

    # study_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/study_test4.txt'
    study_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/study_yeast_acetyl.txt'
    # population_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast_test4.txt'
    population_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/population_yeast_obsProteome.txt'
    association_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/input_goatools/association_goa_yeast'

    # required, and regularly updated
    goa_ref_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
    obo_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo'
#     obo_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/go_rescources/go_obo/goslim_generic.obo'

    num_bins = 100
    alpha = 0.05 # "Test-wise alpha for multiple testing"
    pval = None # "Family-wise alpha (whole experiment), only print out "
                # "Bonferroni p-value is less than this value. "
    compare = False # "the population file as a comparison group. if this "
                    # "flag is specified, the population is used as the study "
                    # "plus the `population/comparison`"
    min_ratio = None # "only show values where the difference between study "
                 # "and population ratios is greater than this. useful for "
                 # "excluding GO categories with small differences, but "
                 # "containing large numbers of genes. should be a value "
                 # "between 1 and 2. "
    fdr = False # "Calculate the false discovery rate (alt. to the "
                # "Bonferroni but slower)"
    indent = False # "indent GO terms"
    methods = ["bonferroni", "sidak", "holm", "benjamini_hochberg"]
    backtracking = False

    # check parameters
    if min_ratio is not None:
        assert 1 <= min_ratio <= 2

    assert 0 < alpha < 1, "Test-wise alpha must fall between (0, 1)"

    # do stuff depending on settings
    if fdr:
        methods.append("fdr")

    #####
    # option A
    study_an_frset, pop_an_set = find_enrichment_dbl.read_geneset(study_fn, population_fn, compare=compare) # study and pop are set and frozenset of AccessionNumbers from user input
    assoc_dict = find_enrichment_dbl.read_associations(association_fn)  # assoc is a dict: key=AN, val=set of go-terms

    # option B # ToDo #!!!
    # without producing additional files: study_fn, population_fn, association_fn
    # goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn)
    # assoc_dict = goretriever.get_association_dict()
    ui = goretriever.UserInput(userinput_fn, num_bins) # adapt UserInput to process web input etc.
    # study_an_frset = ui.get_study_an_frset()
    # pop_an_set = ui.get_pop_an_set()
    #####

    obo_dag = obo_parser.GODag(obo_file=obo_fn)  #!!! don't run this for every analysis

    gostudy = go_enrichment_dbl.GOEnrichmentStudy(study_an_frset, pop_an_set, assoc_dict, obo_dag, ui, alpha, methods, backtracking)
        # pop_an_set, assoc_dict, obo_dag, ui, alpha=alpha, study_an_frset=study_an_frset, methods=methods)

    gostudy.run_study()
    gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)
