import os, sys, json
# import pickle
import numpy as np
from collections import defaultdict
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
sys.path.insert(0, os.path.abspath(os.path.realpath('python')))
import variables
import colnames as cn


### scatter plot
opacity_default = 0.7
opacity_highlight = 1
marker_line_width_default = 1 # invisible ring around points in scatter, white when points overlap
marker_line_color_default = "white"
marker_line_width_highlight = 3
marker_line_color_highlight = "#344957"
width_edges_line = 1.5
color_edge_line = "#d2d2d2"
scatter_plot_width = 700
scatter_plot_height = 400
legend_y = -0.3
text_font_size = 10
min_marker_size, max_marker_size = 4, 30

palette_dict = {1: ['#d95f02'], 2: ['#1b9e77', '#d95f02'], 3: ['#1b9e77', '#d95f02', '#7570b3'], 4: ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3'], 5: ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e'], 6: ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02'], 7: ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d'], 8: ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d', '#666666'], 9: ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999'], 10: ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a'], 11: ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99'], 12: ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928'], 13: ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'], 14: ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2']}

etype_2_categoryRenamed_dict = {-20: "GO cellular component TextMining",
                              -21: "GO biological process",
                              -22: "GO cellular component",
                              -23: "GO molecular function",
                              -25: "Brenda Tissue Ontology",
                              -26: "Disease Ontology",
                              -51: "UniProt keywords",
                              -52: "KEGG pathways",
                              -53: "SMART domains",
                              -54: "InterPro domains",
                              -55: "Pfam domains",
                              -56: "Publications",
                              -57: "Reactome",
                              -58: "WikiPathways"}

def ready_df_for_plot(df, lineage_dict, enrichment_method):
    sizeref = 2.0 * max(df[cn.FG_count]) / (max_marker_size ** 2)
    # ### rename categories
    # category_renamed_list = []
    # value_counts_series = df[cn.etype].value_counts(sort=False) # this depends on row sort order of run_cythonized df, if etype is sorted in ascending True instead of False --> wrong category assignments
    # for etype_, count in zip(value_counts_series.index, value_counts_series.values):
    #     try:
    #         categoryName = etype_2_categoryRenamed_dict[etype_]
    #     except KeyError:
    #         categoryName = ""
    #     category_renamed_list += [categoryName] * count
    # df[cn.category] = category_renamed_list
    df[cn.category] = df[cn.etype].apply(lambda x: etype_2_categoryRenamed_dict[x])

    ### prioritize category with strongest signal
    if enrichment_method in {"genome", "compare_samples", "abundance_correction"}:
        if sum(df[cn.over_under] == "o") > 0:
            category_rank_arr = df.groupby(cn.category)[cn.s_value].max().sort_values(ascending=False).index.values
        else:
            category_rank_arr = df.groupby(cn.category)[cn.s_value].min().sort_values(ascending=True).index.values
        df[cn.logFDR] = np.log10(df[cn.FDR]) * -1
    elif enrichment_method == "characterize_foreground":
        category_rank_arr = df.groupby(cn.category)[cn.ratio_in_FG].max().sort_values(ascending=False).index.values
    else:
        print("plot_and_table.py: enrichment_method '{}' not implemented".format(enrichment_method))
        category_rank_arr = []

    df[cn.category] = pd.Categorical(df[cn.category], category_rank_arr)
    df[cn.category_rank] = df[cn.category].cat.codes
    df = df.sort_values([cn.category, cn.rank]).reset_index(drop=True)

    color_discrete_map = {category_: color_hex_val for category_, color_hex_val in zip(df[cn.category].unique(), palette_dict[df.etype.unique().shape[0]])}
    df[cn.color] = df[cn.category].apply(lambda catname: color_discrete_map[catname])
    df[cn.text_label] = ""

    df[cn.marker_line_width] = marker_line_width_default
    df[cn.marker_line_color] = marker_line_color_default
    df[cn.opacity] = opacity_default

    term_2_edges_dict = get_term_2_edges_dict(df, lineage_dict, enrichment_method)
    term_2_edges_dict_json = json.dumps(term_2_edges_dict)
    return df, term_2_edges_dict_json, sizeref

def get_sorted_colNames_if_exist_in_DF(df, cols_sort_order):
    df_cols_set = set(df.columns)
    cols_set_temp = set(cols_sort_order).intersection(df_cols_set)
    return [colName for colName in cols_sort_order if colName in cols_set_temp]

def df_2_dict_per_category_for_traces(df, enrichment_method):
    """
    sort rows per category so that large points are plotted first (in the background) and small points are in the foreground.
    maybe even opacity should be different (with some sort of gradient)
    """
    dict_per_category, term_2_positionInArr_dict = {}, {}
    term_2_category_dict = {term_: category_ for term_, category_ in zip(df[cn.term], df[cn.category])}
    if enrichment_method != "characterize_foreground":
        for category_name, group in df.groupby(cn.category):
            group = group.sort_values([cn.FG_count], ascending=False)
            term_2_positionInArr_dict.update({term_: pos for pos, term_ in enumerate(group[cn.term])})
            dict_per_category[category_name] = {cn.term: group[cn.term].tolist(),
                                                cn.description: group[cn.description].tolist(),
                                                cn.FG_count: group[cn.FG_count].tolist(),
                                                cn.logFDR: group[cn.logFDR].tolist(),
                                                cn.effect_size: group[cn.effect_size].tolist(),
                                                cn.color: group[cn.color].tolist(),
                                                cn.opacity: group[cn.opacity].tolist(),
                                                cn.marker_line_width: group[cn.marker_line_width].tolist(),
                                                cn.marker_line_color: group[cn.marker_line_color].tolist(),
                                                cn.text_label: group[cn.text_label].tolist(),
                                                }
    else:
        for category_name, group in df.groupby(cn.category):
            group = group.sort_values([cn.FG_count], ascending=False)
            term_2_positionInArr_dict.update({term_: pos for pos, term_ in enumerate(group[cn.term])})
            dict_per_category[category_name] = {cn.term: group[cn.term].tolist(),
                                                cn.description: group[cn.description].tolist(),
                                                cn.ratio_in_FG: group[cn.ratio_in_FG].tolist(),
                                                cn.FG_count: group[cn.FG_count].tolist(),
                                                cn.color: group[cn.color].tolist(),
                                                cn.opacity: group[cn.opacity].tolist(),
                                                cn.marker_line_width: group[cn.marker_line_width].tolist(),
                                                cn.marker_line_color: group[cn.marker_line_color].tolist(),
                                                cn.text_label: group[cn.text_label].tolist(),
                                                }
    return dict_per_category, term_2_positionInArr_dict, term_2_category_dict

def get_data_bars_dict(df, colName):
    """
    css style s_value column with horizontal bars,
     the length of the bar depends on s_value,
     the direction of the sign (positive or negative value),
     the color corresponds to the category and should be identical to the plot
    magnitude calculated for the whole dataset
    """
    term_2_style_dict = {}
    starting_point_right_side = 100 - 50 + 0.5/2 # left_and_right_side_delimiter_width = 0.5
    min_, max_ = df[colName].min(), df[colName].max()
    total = abs(max_) + abs(min_)
    for category_, group in df.groupby(cn.category):
        color_ = group[cn.color].iloc[0]
        for term, value in zip(group[cn.term], group[colName]):
            percentage = 50 * abs(value) / total
            if value > 0: # to the right.
                width = percentage + starting_point_right_side
                color_bar = "transparent 0%, transparent 49.75%, #6C757D 49.75%, #6C757D 50.25%, {} 50.25%, {} {}%, transparent {}%, transparent 100.0%".format(color_, color_, width, width)
            elif value < 0: # to the left
                empty_space_left = 50 - percentage
                width = empty_space_left + percentage
                color_bar = "transparent 0%, transparent {}%, {} {}%, {} {}%, #6C757D 49.75%, #6C757D 50.25%, transparent 50.25%, transparent 100.0%".format(empty_space_left,color_, empty_space_left, color_, width)
            else: # value is 0 or NaN or ? actually shouldn't happen at all
                color_bar = ""
            term_2_style_dict[term] = "{background: linear-gradient(90deg, " + color_bar + "); text-align: center;}"
    return term_2_style_dict

def get_data_bars_dict_characterizeFG(df, colName):
    term_2_style_dict = {}
    min_, max_ = df[colName].min(), df[colName].max()
    total = abs(max_) + abs(min_)
    for category_, group in df.groupby(cn.category):
        color_ = group[cn.color].iloc[0]
        for term, value in zip(group[cn.term], group[colName]):
            percentage = 100 * abs(value) / total
            if value > 0: # to the right.
                width = percentage
                color_bar = "#6C757D 0%, #6C757D 0.5%, {} 0.5%, {} {}%, transparent {}%, transparent 100.0%".format(color_, color_, width, width)
            else: # value is 0 or NaN or ? actually shouldn't happen at all
                color_bar = ""
            term_2_style_dict[term] = "{background: linear-gradient(90deg, " + color_bar + "); text-align: center;}"
    return term_2_style_dict

def get_linkout_template(category_name):
    # if category_name in {"GO cellular component TextMining", "GO cellular component", "GO biological process", "GO molecular function"}:
    if category_name in {"GO cellular component", "GO biological process", "GO molecular function"}:
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.ebi.ac.uk/QuickGO/term/{}">{}</a></td>'''
    elif category_name == "GO cellular component TextMining": # https://compartments.jensenlab.org/Entity?order=textmining,knowledge,predictions&knowledge=10&textmining=10&predictions=10&type1=-22&type2=10090&id1=GO:0070516
        linkout_template = r'''<td id="linkout_dbl"><a href="https://compartments.jensenlab.org/Entity?order=textmining,knowledge,predictions&knowledge=10&textmining=10&predictions=10&type1=-22&type2={}&id1={}">{}</a></td>'''
    elif category_name == "UniProt keywords":
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.uniprot.org/keywords/{}">{}</a></td>'''
    # alternative: https://www.ebi.ac.uk/ols/ontologies/doid/terms?DOID_863
    elif category_name == "Brenda Tissue Ontology": # https://tissues.jensenlab.org/Entity?order=textmining,knowledge,experiments&knowledge=10&experiments=10&textmining=10&type1=-25&type2=9606&id1=BTO:0004216
        # linkout_template = r'''<td id="linkout_dbl"><a href="https://www.ebi.ac.uk/ols/ontologies/bto/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F{}">{}</a></td>'''
        linkout_template = r'''<td id="linkout_dbl"><a href="https://tissues.jensenlab.org/Entity?order=textmining,knowledge,experiments&knowledge=10&experiments=10&textmining=10&type1=-25&type2={}&id1={}">{}</a></td>'''
    # elif category_name == "Disease Ontology": # https://www.ebi.ac.uk/ols/ontologies/doid/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FDOID_863
        # linkout_template = r'''<td id="linkout_dbl"><a href="https://www.ebi.ac.uk/ols/ontologies/doid/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F{}">{}</a></td>'''
    elif category_name == "Disease Ontology": # https://diseases.jensenlab.org/Entity?order=textmining,knowledge,experiments&textmining=10&knowledge=10&experiments=10&type1=-26&type2=9606&id1=DOID:1933
        linkout_template = r'''<td id="linkout_dbl"><a href="https://diseases.jensenlab.org/Entity?order=textmining,knowledge,experiments&textmining=10&knowledge=10&experiments=10&type1=-26&type2=9606&id1={}">{}</a></td>'''
    elif category_name == "KEGG pathways":  # https://www.genome.jp/dbget-bin/www_bget?pathway:map04914
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.genome.jp/dbget-bin/www_bget?pathway:{}">{}</a></td>'''
    elif category_name == "InterPro domains":  # https://www.ebi.ac.uk/interpro/entry/InterPro/IPR002471/
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.ebi.ac.uk/interpro/entry/InterPro/{}">{}</a></td>'''
    elif category_name == "Pfam domains":  # http://pfam.xfam.org/family/PF00017
        linkout_template = r'''<td id="linkout_dbl"><a href="http://pfam.xfam.org/family/{}">{}</a></td>'''
    elif category_name == "Publications":  # https://pubmed.ncbi.nlm.nih.gov/21072307/
        linkout_template = r'''<td id="linkout_dbl"><a href="https://pubmed.ncbi.nlm.nih.gov/{}">{}</a></td>'''
    elif category_name == "Reactome":  # https://reactome.org/content/detail/R-BTA-9034793
        linkout_template = r'''<td id="linkout_dbl"><a href="https://reactome.org/content/detail/{}">{}</a></td>'''
    elif category_name == "WikiPathways":  # https://www.wikipathways.org/index.php/Pathway:WP78
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.wikipathways.org/index.php/Pathway:{}">{}</a></td>'''
    else:
        linkout_template = r'''<td id="linkout_dbl"><a href="https://www.ebi.ac.uk/QuickGO/term/{}">{}</a></td>'''
    return linkout_template

def format_term_for_linkout(category_name, linkout_template, term_name, taxid="9606"):
    if category_name == "GO cellular component TextMining":
        # table_as_text = linkout_template.format(term_name.replace("GOCC:", "GO:"), term_name)
        table_as_text = linkout_template.format(taxid, term_name.replace("GOCC:", "GO:"), term_name)
    elif category_name == "Brenda Tissue Ontology":
        # table_as_text = linkout_template.format(term_name.replace("BTO:", "BTO_"), term_name)
        table_as_text = linkout_template.format(taxid, term_name, term_name)
    elif category_name == "Disease Ontology":
    #     table_as_text = linkout_template.format(term_name.replace("DOID:", "DOID_"), term_name)
        table_as_text = linkout_template.format(term_name, term_name)
    elif category_name == "Publications":
        table_as_text = linkout_template.format(term_name.replace("PMID:", ""), term_name)
    elif category_name == "Reactome":
        table_as_text = linkout_template.format("R-" + term_name, term_name)
    else:
        table_as_text = linkout_template.format(term_name, term_name)
    return table_as_text

def df_2_html_table_with_data_bars(df, cols_sort_order_csv, enrichment_method, taxid="9606"): #, session_id, session_folder_absolute):
    # linkout_style = """#linkout_dbl a:link { color:#000000; TEXT-DECORATION: none; font-weight: normal} #linkout_dbl a:visited { color:#000000; TEXT-DECORATION: none; font-weight: normal} #linkout_dbl a:active { color:#0000EE; } #linkout_dbl a:hover { color:#0000EE; font-weight: normal; text-decoration: underline; } """
    # file_name = "results_orig" + session_id + ".tsv"
    # fn_results_orig_absolute = os.path.join(session_folder_absolute, file_name)
    # remaining columns are omitted for csv file, but needed for plot
    # df_2_file = df[cols_sort_order_csv].rename(columns=cn.colnames_2_rename_dict_aGOtool_file)
    # df_2_file.to_csv(fn_results_orig_absolute, sep="\t", header=True, index=False)
    if enrichment_method != "characterize_foreground":
        term_2_style_dict = get_data_bars_dict(df, cn.s_value)
    else:
        term_2_style_dict = get_data_bars_dict_characterizeFG(df, cn.ratio_in_FG)
    df = df[cols_sort_order_csv].rename(columns=cn.colnames_2_rename_dict_aGOtool_web)
    table_as_text = '''<table border="0" class="dataframe display table dataTable_DBL dataTable table-striped" id="dataTable_DBL_id"> <thead> <tr style="text-align: left;">'''
    if enrichment_method in {"genome", "abundance_correction"}:
        for colname in df.columns.tolist():
            table_as_text += " <th>{}</th> ".format(colname)
        table_as_text += '''</tr> </thead> <tbody> '''
        for category_name, group in df.groupby(cn.category):
            linkout_template = get_linkout_template(category_name)
            for row in group.itertuples(index=False):
                s_value_ = row[0]
                term_name = row[1]
                description = row[2]
                fdr = row[3]
                effectsize = row[4]
                category = row[5]
                overunder = row[6]
                hierarchicallevel = row[7]
                year = row[8]
                fgids = row[9]
                fgcount = row[10]
                fgn = row[11]
                bgcount = row[12]
                bgn = row[13]
                ratioinfg = row[14]
                ratioinbg = row[15]
                pvalue = row[16]
                logfdr = row[17]
                rank = row[18]
                category_rank = row[19]
                term_id = term_name.replace(":", "").replace("-", "")
                try:
                    style = term_2_style_dict[term_name]
                except KeyError:
                    style = "{}"
                table_as_text += '''<tr> <style type="text/css"> #{}{} </style>'''.format(term_id, style)
                table_as_text += '''<td class="legible_text_shadow" id="{}">{:.2f}</td>'''.format(term_id, s_value_)
                table_as_text += format_term_for_linkout(category_name, linkout_template, term_name, taxid)
                table_as_text += '''<td>{}</td>'''.format(description)
                table_as_text += '''<td>{:.2E}</td>'''.format(fdr)
                table_as_text += '''<td>{:.2f}</td>'''.format(effectsize)
                table_as_text += '''<td>{}</td>'''.format(category)
                table_as_text += '''<td>{}</td>'''.format(overunder)
                table_as_text += '''<td>{}</td>'''.format(hierarchicallevel)
                table_as_text += '''<td>{}</td>'''.format(year)
                table_as_text += '''<td>{}</td>'''.format(fgids)
                table_as_text += '''<td>{}</td>'''.format(fgcount)
                table_as_text += '''<td>{}</td>'''.format(fgn)
                table_as_text += '''<td>{}</td>'''.format(bgcount)
                table_as_text += '''<td>{}</td>'''.format(bgn)
                table_as_text += '''<td>{:.3f}</td>'''.format(ratioinfg)
                table_as_text += '''<td>{:.3f}</td>'''.format(ratioinbg)
                table_as_text += '''<td>{:.2E}</td>'''.format(pvalue)
                table_as_text += '''<td>{:.2E}</td>'''.format(logfdr)
                table_as_text += '''<td>{}</td>'''.format(rank)
                table_as_text += '''<td>{}</td>'''.format(category_rank)
                table_as_text += ''' </tr> '''
        table_as_text += ''' </tbody> </table> '''

    elif enrichment_method == "characterize_foreground":
        for colname in df.columns.tolist():
            table_as_text += " <th>{}</th> ".format(colname)
        table_as_text += '''</tr> </thead> <tbody> '''

        for category_name, group in df.groupby(cn.category):
            linkout_template = get_linkout_template(category_name)
            for row in group.itertuples(index=False):
                ratioinfg = row[0]
                term_name = row[1]
                description = row[2]
                category = row[3]
                hierarchicallevel = row[4]
                year = row[5]
                fgids = row[6]
                fgcount = row[7]
                fgn = row[8]
                rank = row[9]
                category_rank = row[10]
                term_id = term_name.replace(":", "").replace("-", "")
                try:
                    style = term_2_style_dict[term_name]
                except KeyError:
                    style = "{}"
                table_as_text += '''<tr> <style type="text/css"> #{}{} </style>'''.format(term_id, style)
                table_as_text += '''<td class="legible_text_shadow" id="{}">{:.3f}</td>'''.format(term_id, ratioinfg)
                table_as_text += format_term_for_linkout(category_name, linkout_template, term_name, taxid)
                table_as_text += '''<td>{}</td>'''.format(description)
                table_as_text += '''<td>{}</td>'''.format(category)
                table_as_text += '''<td>{}</td>'''.format(hierarchicallevel)
                table_as_text += '''<td>{}</td>'''.format(year)
                table_as_text += '''<td>{}</td>'''.format(fgids)
                table_as_text += '''<td>{}</td>'''.format(fgcount)
                table_as_text += '''<td>{}</td>'''.format(fgn)
                table_as_text += '''<td>{}</td>'''.format(rank)
                table_as_text += '''<td>{}</td>'''.format(category_rank)
                table_as_text += ''' </tr> '''
        table_as_text += ''' </tbody> </table> '''

    elif enrichment_method == "compare_samples":
        for colname in df.columns.tolist():
            table_as_text += " <th>{}</th> ".format(colname)
        table_as_text += '''</tr> </thead> <tbody> '''

        for category_name, group in df.groupby(cn.category):
            linkout_template = get_linkout_template(category_name)
            for row in group.itertuples(index=False):
                s_value_ = row[0]
                term_name = row[1]
                description = row[2]
                fdr = row[3]
                effectsize = row[4]
                category = row[5]
                overunder = row[6]
                hierarchicallevel = row[7]
                year = row[8]
                fgids = row[9]
                bgids = row[10]
                fgcount = row[11]
                fgn = row[12]
                bgcount = row[13]
                bgn = row[14]
                ratioinfg = row[15]
                ratioinbg = row[16]
                pvalue = row[17]
                logfdr = row[18]
                rank = row[19]
                category_rank = row[20]
                term_id = term_name.replace(":", "").replace("-", "")
                try:
                    style = term_2_style_dict[term_name]
                except KeyError:
                    style = "{}"
                table_as_text += '''<tr> <style type="text/css"> #{}{} </style>'''.format(term_id, style)
                table_as_text += '''<td class="legible_text_shadow" id="{}">{:.2f}</td>'''.format(term_id, s_value_)
                table_as_text += format_term_for_linkout(category_name, linkout_template, term_name, taxid)
                table_as_text += '''<td>{}</td>'''.format(description)
                table_as_text += '''<td>{:.2E}</td>'''.format(fdr)
                table_as_text += '''<td>{:.2f}</td>'''.format(effectsize)
                table_as_text += '''<td>{}</td>'''.format(category)
                table_as_text += '''<td>{}</td>'''.format(overunder)
                table_as_text += '''<td>{}</td>'''.format(hierarchicallevel)
                table_as_text += '''<td>{}</td>'''.format(year)
                table_as_text += '''<td>{}</td>'''.format(fgids)
                table_as_text += '''<td>{}</td>'''.format(bgids)
                table_as_text += '''<td>{}</td>'''.format(fgcount)
                table_as_text += '''<td>{}</td>'''.format(fgn)
                table_as_text += '''<td>{}</td>'''.format(bgcount)
                table_as_text += '''<td>{}</td>'''.format(bgn)
                table_as_text += '''<td>{:.3f}</td>'''.format(ratioinfg)
                table_as_text += '''<td>{:.3f}</td>'''.format(ratioinbg)
                table_as_text += '''<td>{:.2E}</td>'''.format(pvalue)
                table_as_text += '''<td>{:.2E}</td>'''.format(logfdr)
                table_as_text += '''<td>{}</td>'''.format(rank)
                table_as_text += '''<td>{}</td>'''.format(category_rank)
        table_as_text += ''' </tbody> </table> '''
    else:
        print("enrichment_method: '{}' not defined".format(enrichment_method))

    return table_as_text


def get_term_2_edges_dict(df, lineage_dict_direct, enrichment_method):
    """
    iterate over direct parents and stop once at least one is found
    Dict: key=term val=[X_vals_list, Y_vals_list, Weights_list]
    # for every term:
    #   for every edge:
    #     e.g. between point A (Ax, Ay) and B (Bx, By) as well as A (Ax, Ay) and C (Cx, Cy)
    #     X_point_list += [Ax, Bx, None]
    #     Y_point_list += [Ay, By, None]
    #     Weights_list += [A_2_B]
    #     X_point_list += [Ax, Cx, None]
    #     Y_point_list += [Ay, Cy, None]
    """
    term_2_edges_dict = defaultdict(lambda: {"X_points": [], "Y_points": [], "Weights": [], "Nodes": []})
    for etype_, group in df.groupby(cn.etype):
        if etype_ not in variables.entity_types_with_ontology:
            continue
        funcNameFamilySet_list_merged, funcNameFamilySet_list_temp, edgesXYCoords_list, funcNamePair_set = [], [], [], set()
        funcs_2_travers_set = group[cn.term]
        for term_ in funcs_2_travers_set:
            funcNamePair_set |= find_pairs_2_link(term_, lineage_dict_direct, funcs_2_travers_set)

        ## extract x and y coordinates and a weight depending on the overlapp of FG_IDs (Jaccard index)
        for funcNamePair in funcNamePair_set:
            if enrichment_method != "characterize_foreground":
                X_points_list, Y_points_list, Weight_temp = get_edge_positions_and_weight_as_list(group[group[cn.term].isin(funcNamePair)])
            else:
                X_points_list, Y_points_list, Weight_temp = get_edge_positions_and_weight_as_list_characterizeFG(group[group[cn.term].isin(funcNamePair)])

            funcName_a, funcName_b = funcNamePair
            term_2_edges_dict[funcName_a]["X_points"] += X_points_list
            term_2_edges_dict[funcName_a]["Y_points"] += Y_points_list
            term_2_edges_dict[funcName_a]["Weights"].append(Weight_temp)
            term_2_edges_dict[funcName_a]["Nodes"].append(funcName_b)

            term_2_edges_dict[funcName_b]["X_points"] += X_points_list
            term_2_edges_dict[funcName_b]["Y_points"] += Y_points_list
            term_2_edges_dict[funcName_b]["Weights"].append(Weight_temp)
            term_2_edges_dict[funcName_b]["Nodes"].append(funcName_a)
    return term_2_edges_dict

def find_pairs_2_link(term, lineage_dict_direct, funcs_2_travers_set):
    funcNamePair_set = set()
    for parents in yield_direct_parents([term], lineage_dict_direct):
        if not parents:
            continue
        else:
            lineage_2_add = set(parents)
            lineage_2_add.add(term)
            funcNameFamilySet = lineage_2_add.intersection(funcs_2_travers_set)
        len_funcNameFamilySet = len(funcNameFamilySet)
        if len_funcNameFamilySet < 2:
            continue
        elif len_funcNameFamilySet == 2:
            funcNamePair_set.add(tuple(sorted(funcNameFamilySet)))
            return funcNamePair_set
        elif len_funcNameFamilySet > 2:
            for func in funcNameFamilySet - set([term]):
                funcNamePair_set.add(tuple(sorted([term, func])))
            return funcNamePair_set
        else:
            raise StopIteration
    return funcNamePair_set

def get_edge_positions_and_weight_as_list(df):
    """
    # for every term:
    #   for every edge:
    #     e.g. between point A (Ax, Ay) and B (Bx, By) as well as A (Ax, Ay) and C (Cx, Cy)
    #     X_point_list += [Ax, Bx, None]
    #     Y_point_list += [Ay, By, None]
    #     Weights_list += [A_2_B]
    #     X_point_list += [Ax, Cx, None]
    #     Y_point_list += [Ay, Cy, None]
    """
    # assert df.shape[0] == 2
    try:
        first_FG_IDs, second_FG_IDs = df[cn.FG_IDs].values
        first_FG_IDs = set(first_FG_IDs.split(";"))
        second_FG_IDs = set(second_FG_IDs.split(";"))
        ## compute weight of edge
        jaccard_index = len(first_FG_IDs.intersection(second_FG_IDs)) / len(first_FG_IDs.union(second_FG_IDs))
    except:  # AttributeError if NaN or ZeroDivisionError if ...
        jaccard_index = 1
    return df[cn.logFDR].tolist() + [None], df[cn.effect_size].tolist() + [None], jaccard_index

def get_edge_positions_and_weight_as_list_characterizeFG(df):
    try:
        first_FG_IDs, second_FG_IDs = df[cn.FG_IDs].values
        first_FG_IDs = set(first_FG_IDs.split(";"))
        second_FG_IDs = set(second_FG_IDs.split(";"))
        ## compute weight of edge
        jaccard_index = len(first_FG_IDs.intersection(second_FG_IDs)) / len(first_FG_IDs.union(second_FG_IDs))
    except:  # AttributeError if NaN or ZeroDivisionError if ...
        jaccard_index = 1
    return df[cn.ratio_in_FG].tolist() + [None], df[cn.FG_count].tolist() + [None], jaccard_index

def yield_direct_parents(terms, lineage_dict):
    """
    generator: to return all direct parents of given terms
    lineage_dict = cst.get_lineage_dict_for_all_entity_types_with_ontologies(direct_or_allParents="direct")
    terms = ["GO:0016572"]
    for parents in yield_direct_parents(terms, lineage_dict):
        print(parents)
    :param terms: list of string
    :param lineage_dict: child 2 direct parents dict
    :return: list of string
    """
    def get_direct_parents(terms, lineage_dict):
        parents = []
        for term in terms:
            try:
                parents += lineage_dict[term]
            except KeyError:
                pass
        parents = sorted(set(parents))
        return parents

    parents = get_direct_parents(terms, lineage_dict)
    while parents:
        yield parents
        parents = get_direct_parents(parents, lineage_dict)
    return None


if __name__ == "__main__":
    # pass
    # - Table cell height could be smaller/lower
    # - hide options in enrichment page --> cleaner look
    # - plot / results page toggle button to show tipps
    # df = pd.read_csv(variables.fn_example, sep="\t")
    # term_2_style_dict = get_data_bars_dict(df, cn.s_value)
    # term = "KW-0472"
    # print(term_2_style_dict[term])

    df = pd.read_csv(variables.fn_example, sep="\t")
    df = ready_df_for_plot(df, lineage_dict=None, enrichment_method="genome")
    # df = df.groupby(cn.etype).head(20)
    # import pickle
    # lineage_dict_direct = pickle.load(open(os.path.join(variables.PYTHON_DIR, "term_2_edges_dict.p"), "rb"))
    # print("lineage_dict", lineage_dict_direct["GOCC:0005634"])
    # term_2_edges_dict = get_term_2_edges_dict(df, lineage_dict_direct, "abundance_correction")
