import pandas as pd


### TESTING method = characterize_study
########################################################################
### create Test DataFrame for proteinGroups
# fn = r"/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_Jesper/GOenr/MaxPep/protGroup/Perio_vs_Healthy_Bacteriagenus.txt"
# dfx = pd.read_csv(fn, sep='\t')
# print dfx.shape
# print len(dfx["sample_an"].unique())
# dfx = dfx.head(11)
# dfx.head()
# ### create Test DataFrame for proteinGroups
# # equivalent to GOenrichment_characterize_study_test_DF_v2.txt but with proteinGroups --> the contingency table should give equivalent numbers (there might be more GOterms overall)
# fn = r"/Users/dblyon/CloudStation/CPR/Ancient_Proteins_Project/Daniel/txt_Jesper/GOenr/MaxPep/protGroup/Perio_vs_Healthy_Bacteriagenus.txt"
# dfx = pd.read_csv(fn, sep='\t')
# dfx = dfx.head(11)
# dfx.loc[0:7, "sample_an"] = "A3CP09;ssan_c_1_1478;EGQ25042.1;EGQ22065.1"
# dfx.loc[0:4, "population_an"] = "A3CP09;ssan_c_1_1478;EGQ25042.1;EGQ22065.1"
# dfx.loc[8:11, "sample_an"] = "vpardsm_c_1_987;vot158_c_15_2061;vaty_c_5_598"
# dfx.loc[5, "population_an"] = "vpardsm_c_1_987;vot158_c_15_2061;vaty_c_5_598"
# dfx.loc[6:, "population_an"] = np.nan
# fn_test = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_proteinGroups.txt'
# dfx.to_csv(fn_test, sep='\t', header=True, index=False)
########################################################################

# ### creating test dataframe nr. 1
# fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_Healthy_Bacspecies.txt'  # 14107
# dfx = pd.read_csv(fn, sep='\t')
# print dfx.shape
# print len(dfx["sample_an"].unique())
# dfx = dfx.head(11)
# fn_test = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF.txt'
# dfx.to_csv(fn_test, sep='\t', header=True, index=False)
# ### creating test dataframe nr. 2
# dfx.loc[0:7, "sample_an"] = "A4SUU7"
# dfx.loc[0:4, "population_an"] = "A4SUU7"
# dfx.loc[8:11, "sample_an"] = "A6W5V2"
# dfx.loc[5, "population_an"] = "A6W5V2"
# dfx.loc[6:, "population_an"] = np.nan
# fn_test = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
# dfx.to_csv(fn_test, sep='\t', header=True, index=False)


# # creating test dataframe
# fn = r'/Users/dblyon/modules/cpr/metaprot/Perio_vs_Healthy_Bacspecies.txt' # 14107
# cp /Users/dblyon/modules/cpr/metaprot/Perio_vs_Healthy_Bacspecies.txt /Users/dblyon/modules/cpr/agotool/static/data/exampledata
# dfx = pd.read_csv(fn, sep='\t')
# print dfx.shape
# print len(dfx["sample_an"].unique())
# dfx = dfx.head(11)
# # fn_test = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF.txt'
# # dfx.to_csv(fn_test, sep='\t', header=True, index=False)

# dfx.loc[0:7, "sample_an"] = "A4SUU7"
# dfx.loc[0:4, "population_an"] = "A4SUU7"
# dfx.loc[8:11, "sample_an"] = "A6W5V2"
# dfx.loc[5, "population_an"] = "A6W5V2"
# dfx.loc[6:, "population_an"] = np.nan
# fn_test = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'
# dfx.to_csv(fn_test, sep='\t', header=True, index=False)

# # TESTING method = characterize_study
# foreground_n = 10
# background_n = 10
# method = "characterize_study" # "characterize_study" or "method"
# go_slim_or_basic = "slim"
# userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'

# GOid2NumANs_dict_study, go2ans_study_dict = run.run(method, userinput_fn, foreground_n, background_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
#         multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
#         fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
#         go_dag, goslim_dag, pgoa, upkp)
# sorted_term_study = sorted(GOid2NumANs_dict_study.items(), key=operator.itemgetter(1))[::-1]
# dfx = pd.DataFrame(sorted_term_study, columns=["GOid", "Num_associations"])
# # dfx['description'] = dfx['GOid'].apply(get_description)
# # dfx['level'] = dfx['GOid'].apply(get_level)
# dfx['description'] = dfx["GOid"].apply(get_description, args=(go_dag, ))
# dfx['level'] = dfx["GOid"].apply(get_level, args=(go_dag, ))

# dfx.head()
# df_characterize_study = dfx.copy()

# assert sorted(dfx.Num_associations.unique()) == [3, 8, 11]

# # TESTING method = method
# foreground_n = 10
# background_n = 10
# method = "method" # "characterize_study" or "method"
# go_slim_or_basic = "slim"
# userinput_fn = r'/Users/dblyon/modules/cpr/metaprot/test/GOenrichment_characterize_study_test_DF_v2.txt'

# header, results = run.run(method, userinput_fn, foreground_n, background_n, decimal, organism, gocat_upk, go_slim_or_basic, indent,
#             multitest_method, alpha, o_or_u_or_both, abcorr, num_bins, backtracking,
#             fold_enrichment_study2pop, p_value_uncorrected, p_value_mulitpletesting,
#             go_dag, goslim_dag, pgoa, upkp)
# fn_out = userinput_fn.replace(".txt", "_compare_groups_{}.txt".format(go_slim_or_basic))
# fn_out_filtered = fn_out.replace('.txt', "_fltr.txt")

# tsv = (u'%s\n%s\n' % (header, u'\n'.join(results)))
# print fn_out
# write2file(fn_out, tsv)
# df = pd.read_csv(fn_out, sep='\t')
# df['level'] = df["id"].apply(get_level, args=(go_dag, ))

# df['ANs_count'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
# df = find_GOterms_for_perio_caries(df)
# df.to_csv(fn_out, sep='\t', header=True, index=False)
# print df.shape

# # results_filtered = filter_.filter_term_lineage(header, results, indent)
# # tsv = (u'%s\n%s\n' % (header, u'\n'.join(results_filtered)))
# # print fn_out_filtered
# # write2file(fn_out_filtered, tsv)
# # df = pd.read_csv(fn_out_filtered, sep='\t')
# # df['level'] = df["id"].apply(get_level, args=(go_dag, ))
# # df['ANs_count'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
# # df = find_GOterms_for_perio_caries(df)
# # df.to_csv(fn_out_filtered, sep='\t', header=True, index=False)
# # print df.shape

# df['ANs_count_study'] = df['ANs_study'].apply(lambda x: len(x.split(",")))
# cond = df["foreground_n"] == df["ANs_count_study"]*foreground_n
# assert sum(cond) == len(cond)
# df['ANs_count_pop'] = df['ANs_pop'].apply(lambda x: len(x.split(",")))
# cond = df["background_n"] == df["ANs_count"]*background_n
# assert sum(cond) == len(cond)

# df_characterize_study.head() # Num_associations == foreground_count

# df_compare_groups["foreground_count"] == df_characterize_study["Num_associations"]

# df_compare_groups = df[["id", "foreground_count"]]
# df_compare_groups.columns = ["GOid", "foreground_count"]
# df_compare_groups.head()

# df_characterize_study = dfx.copy()
# df_compare_groups = df[["id", "foreground_count"]]
# df_compare_groups.columns = ["GOid", "foreground_count"]
# dfm = pd.merge(df_compare_groups, df_characterize_study, how='outer')
# cond = dfm['foreground_count'] == dfm['Num_associations']
# assert sum(cond) == len(cond)

# df.sort_values("background_count", ascending=False).head()

# assert sorted(df.foreground_n.unique()) == [10, 20]
# assert sorted(df.background_n.unique()) == [10, 20]
# assert sorted(df.background_count.unique()) == [1, 5, 6]
# assert sorted(df.foreground_count.unique()) == [3, 8, 11]

# dfx.head()
# dfx.sort_values("Num_associations", ascending=True)
# dfx.describe()


