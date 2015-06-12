import goretriever, go_enrichment_dbl, obo_parser, os, userinput
# find_enrichment_dbl
# import pandas as pd
# import numpy as np

__author__ = 'dblyon'




if __name__ == '__main__':
    home = os.path.expanduser('~')


    #!!! don't run this for every analysis. check organism here!!!
    # required, and regularly updated

    goa_ref_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
    # goa_ref_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/human/gene_association.goa_ref_human'

    obo_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo'
    # obo_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/goslim_generic.obo'

    obo_dag = obo_parser.GODag(obo_file=obo_fn)
    assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict()



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

# YEAST
# ['Genome',
#  'iBAQ observed (log10)',
#  'Observed Proteome',
#  'Phos',
#  'Ubi',
#  'Acetyl',
#  'Succinyl']

# 1- modified v genome
# 2- modified v observed
# 3- modified v Abundance-corrected

    decimal = ','
    randomSample = False
    userinput_fn = home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_Yeast_v2.txt'
    # userinput_fn = home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_HeLa.txt'

    for modification in ['Acetyl']: #['Phos', 'Ubi', 'Acetyl', 'Succinyl']:
        for background in ['Observed', 'Genome', 'AbCorr']:
            fn_out = 'Yeast_modification_vs_background.txt'
            # fn_out = 'HeLa_modification_vs_background.txt'
            fn_out = fn_out.replace('modification', modification)
            fn_out = fn_out.replace('background', background)
            if background == 'AbCorr':
                abcorr = True
            else:
                abcorr = False
            if background == 'Genome':
                col_background_an = 'Genome'
            else:
                col_background_an = 'Observed Proteome'
            col_sample_an = modification
            col_background_int = 'iBAQ observed (log10)'

            print(fn_out, modification, background)
            ui = userinput.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)

            gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr)
            gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)



##### old UserInput txt file
    # abcorr = True
    # userinput_fn = r'/Users/dblyon/CloudStation/CPR/Brian_GO/UserInput.txt'
    # fn_out = 'Yeast_Acetyl_vs_AbCorr_oldUserInput.txt'
    # ui = goretriever.UserInput(userinput_fn, num_bins)
    # gostudy = go_enrichment_dbl.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr)
    # gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)








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

















