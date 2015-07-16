import goretriever, go_enrichment_, obo_parser, os, userinput_, uniprot_keywords, gotupk
# find_enrichment_dbl
# import pandas as pd
# import numpy as np

__author__ = 'dblyon'

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


if __name__ == '__main__':
    home = os.path.expanduser('~')
    decimal = ','
    gocat_upk = 'all_GO'
    go_slim_or_basic = 'basic'
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


    species = 'yeast'


    #####
    species = species.upper()
    if species == 'YEAST':
        goa_ref_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/yeast/gene_association.goa_ref_yeast'
        uniprot_keywords_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/keywords/UniProt_SaccharomycesCerevisiae_Keywords_20150611.tab'
        userinput_fn = home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_Yeast_v2.txt'
    elif species == 'HUMAN':
        goa_ref_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/human/gene_association.goa_ref_human'
        uniprot_keywords_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/UniProt_goa/keywords/UniProt_HomoSapiens_Keywords_20150611.tab'
        userinput_fn = home + r'/CloudStation/CPR/Brian_GO/alldata/Data_for_web_tool_HeLa_v2.txt'
#####
    if go_slim_or_basic == 'basic':
        obo_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/go-basic.obo'
    else:
        obo_fn = home + r'/CloudStation/CPR/Brian_GO/go_rescources/go_obo/goslim_generic.obo'
#####
    if go_terms_or_uniprot_keywords == 'go_terms':
        obo_dag = obo_parser.GODag(obo_file=obo_fn)
        assoc_dict = goretriever.Parser_UniProt_goa_ref(goa_ref_fn = goa_ref_fn).get_association_dict(go_parent, obo_dag)
    else:
        assoc_dict = uniprot_keywords.UniProt_keywords_parser(uniprot_keywords_fn).get_association_dict()

    for modification in ['Acetyl', 'Phos', 'Ubi', 'Succinyl']:
        for background in ['Observed', 'Genome', 'AbCorr']:
            if species == 'YEAST':
                if go_terms_or_uniprot_keywords == 'up_keywords':
                    fn_out = 'Yeast_modification_vs_background_UPK.txt'
                else:
                    fn_out = 'Yeast_modification_vs_background.txt'
            elif species == 'HUMAN':
                if go_terms_or_uniprot_keywords == 'up_keywords':
                    fn_out = 'HeLa_modification_vs_background_UPK.txt'
                else:
                    fn_out = 'HeLa_modification_vs_background.txt'
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
            ui = userinput_.UserInput(userinput_fn, num_bins, col_sample_an, col_background_an, col_background_int, decimal)

            if go_terms_or_uniprot_keywords == 'go_terms':
                gostudy = go_enrichment_.GOEnrichmentStudy(ui, assoc_dict, obo_dag, alpha, methods, backtracking, randomSample, abcorr, e_or_p_or_both)
                gostudy.write_summary2file(fn_out, min_ratio=min_ratio, indent=indent, pval=pval)
            else:
                gostudy = go_enrichment_.GOEnrichmentStudy_UPK(ui, assoc_dict, alpha, methods, randomSample, abcorr, e_or_p_or_both)
                gostudy.write_summary2file(fn_out, min_ratio=min_ratio, pval=pval)





    header, results = gotupk.run(userinput_fn, decimal, organism, gocat_upk, go_slim_or_basic, indent,
            multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
            fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting, species2files_dict, obo2file_dict)










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

















