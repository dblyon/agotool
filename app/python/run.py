import os, sys
import pandas as pd
import numpy as np
from lxml import etree
import json

sys.path.insert(0, os.path.abspath(os.path.realpath(__file__)))
import run_cythonized
import tools, variables

#### plotly libs
import pickle
from collections import defaultdict
import plotly
import plotly.graph_objects as go



def run_UniProt_enrichment(pqo, ui, args_dict, api_call=False):
    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis()
    ncbi = pqo.ncbi
    if args_dict["o_or_u_or_both"] == "overrepresented":
        encoding = 1
    elif args_dict["o_or_u_or_both"] == "both":
        encoding = 0
    elif args_dict["o_or_u_or_both"] == "underrepresented":
        encoding = 2
    else:
        args_dict["ERROR o_or_u_or_both"] = "Unknown option for o_or_u_or_both, does not understand: '{}'".format(args_dict["o_or_u_or_both"])
        return False
    args_dict["o_or_u_or_both_encoding"] = encoding
    if args_dict["enrichment_method"] == "characterize_foreground":
        df_2_return = run_cythonized.run_characterize_foreground_cy(ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=variables.LOW_MEMORY)
    else:
        df_2_return = run_cythonized.run_enrichment_cy(ncbi, ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=variables.LOW_MEMORY)
        # ENSP_2_tuple_funcEnum_score_dict, ncbi, ui, preloaded_objects_per_analysis, static_preloaded_objects, low_memory=False, debug=False, KS_method="cy", KS_etypes_FG_IDs=True)
    if type(df_2_return) == dict: # args_dict returned since
        # e.g. enrichment_method "genome" using different taxon for foreground than background
        return False # display "info_check_input.html"
    elif type(df_2_return) == pd.core.frame.DataFrame:
        if df_2_return.shape[0] == 0:
            args_dict["ERROR empty results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
            if api_call:
                output_format = args_dict["output_format"]
                return format_results(df_2_return, output_format, args_dict)
            else:
                return False
        else:
            output_format = args_dict["output_format"]
            return format_results(df_2_return, output_format, args_dict)
    else:
        print("run.py " * 5)
        print("This shouldn't happen!!")
        print(type(df_2_return), df_2_return)
        print("run.py " * 5)
        return False

def run_STRING_enrichment(pqo, ui, args_dict):
    enrichment_method = args_dict["enrichment_method"]
    if enrichment_method not in {"characterize_foreground", "compare_samples"}: # , "compare_groups"
        args_dict["ERROR_enrichment_method"] = "ERROR: enrichment_method {} is not implemented. Please check the input parameters and examples.".format(enrichment_method)
        return False

    enrichment_method = args_dict["enrichment_method"]
    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    #with pqo.get_preloaded_objects_per_analysis_contextmanager(method=enrichment_method) as preloaded_objects_per_analysis:
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis(method=enrichment_method)
    if enrichment_method == "compare_samples":
        protein_ans_fg = ui.get_foreground_an_set() # is a set
        protein_ans_bg = ui.get_background_an_set() # is a set
        df_2_return = run_cythonized.run_compare_samples_cy(protein_ans_fg, protein_ans_bg, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)

    elif enrichment_method == "characterize_foreground":
        protein_ans = ui.get_an_redundant_foreground() # is a list
        df_2_return = run_cythonized.run_characterize_foreground_cy(protein_ans, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)

    ### for STRING internally disabled, otherwise this makes sense to use DONT DELETE
    if df_2_return.shape[0] == 0:
        args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
        return False

    output_format = args_dict["output_format"]
    return format_results(df_2_return, output_format, args_dict)

def run_STRING_enrichment_genome(pqo, ui, background_n, args_dict):
    taxid = check_taxids(args_dict)
    if not taxid:
        args_dict["ERROR_taxid"] = "Please provide a TaxID (a taxonomic identifier e.g. 9606 for Homo sapiens)"
        return False

    protein_ans = ui.get_all_individual_AN() # proteins_ans is a list
    if variables.VERSION_ != "STRING":
        if not check_all_ENSPs_of_given_taxid(protein_ans, taxid):
            taxid_string = str(taxid)
            ans_not_concur = [an for an in protein_ans if not an.startswith(taxid_string)]
            args_dict["ERROR_taxid_proteinAN"] = "ERROR_taxid_proteinAN: The TaxID '{}' provided and the taxid of the proteins provided (e.g. '{}') do not concur.".format(taxid, ans_not_concur[:3])
            return False

    static_preloaded_objects = pqo.get_static_preloaded_objects(variables.LOW_MEMORY)
    #with pqo.get_preloaded_objects_per_analysis_contextmanager(method="genome") as preloaded_objects_per_analysis:
    preloaded_objects_per_analysis = pqo.get_preloaded_objects_per_analysis(method="genome")
    # if variables.temp_dont_run_analysis:
    #     return format_results(pd.DataFrame(), args_dict["output_format"], args_dict)
    df_2_return = run_cythonized.run_genome_cy(taxid, protein_ans, background_n, preloaded_objects_per_analysis, static_preloaded_objects, args_dict, variables.LOW_MEMORY)
    if variables.VERSION_ != "STRING": # for STRING internally disabled, otherwise this makes sense to use DONT DELETE
        if df_2_return.shape[0] == 0:
            args_dict["ERROR_Empty_Results"] = "Unfortunately no results to display or download. This could be due to e.g. FDR_threshold being set too stringent, identifiers not being present in our system or not having any functional annotations, as well as others. Please check your input and try again."
            return False
    return format_results(df_2_return, args_dict["output_format"], args_dict)

def filter_and_sort_PMID(df, PMID_top_100=True):
    ### remove blacklisted terms --> duplicate to cluster_filter.filter_parents_if_same_foreground_v2
    # df = df[~df["term"].isin(variables.blacklisted_terms)]
    cond_PMID = df["etype"] == -56
    if sum(cond_PMID) > 0:
        df_PMID = df[cond_PMID]
        df_rest = df[~cond_PMID]
        df_PMID["year"] = df_PMID["description"].apply(PMID_description_to_year)
        df_PMID = df_PMID.sort_values(["FDR", "p_value", "year", "foreground_count"], ascending=[True, True, False, False])
        if PMID_top_100:
            df_PMID = df_PMID.head(100)
        df_rest = df_rest.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        df = pd.concat([df_rest, df_PMID], sort=False)
        cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids', 'year']
    else:
        df = df.sort_values(["etype", "FDR", "p_value", "foreground_count"], ascending=[False, True, True, False])
        cols_sort_order = ['term', 'hierarchical_level', 'p_value', 'FDR', 'category', 'etype', 'description', 'foreground_count', 'foreground_ids']
    cols_sort_order += sorted(set(df.columns.tolist()) - set(cols_sort_order))
    return df[cols_sort_order]

def PMID_description_to_year(string_):
    try:
        return int(string_[1:5])
    except ValueError or IndexError:
        return np.nan

def format_results(df, output_format, args_dict):
    if output_format == "dataframe":
        return df
    elif output_format == "tsv":
        return df.to_csv(sep="\t", header=True, index=False)
    elif output_format == "tsv-no-header" or output_format == "tsv_no_header":
        return df.to_csv(sep="\t", header=False, index=False)
    elif output_format == "json":
        # etype_2_resultsjson_dict = {}
        # for etype, group in df.groupby("etype"):
        #     etype_2_resultsjson_dict[etype] = group.to_json(orient='records')
        # return etype_2_resultsjson_dict
        # return df.to_json(orient="records")
        return json.dumps(df.to_dict(orient='records'))
    elif output_format == "xml": # xml gets formatted in runserver.py
        dict_2_return = {}
        for etype, df_group in df.groupby("etype"):
            results = df_group.to_csv(sep="\t", header=True, index=False)  # convert DatFrame to string
            header, rows = results.split("\n", 1)  # is df in tsv format
            xml_string = create_xml_tree(header, rows.split("\n"))
            dict_2_return[etype] = xml_string.decode()
        return dict_2_return
    else:
        args_dict["ERROR output format"] = "output_format {} is unknown, please chose one of [tsv, tsv-no-header, json, xml] and try again".format(output_format)
        return False

def create_xml_tree(header, rows):
    xml_tree = etree.Element("EnrichmentResult")
    header = header.split("\t")
    for row in rows:
        child = etree.SubElement(xml_tree, "record")
        for tag_content in zip(header, row.split("\t")):
            tag, content = tag_content
            etree.SubElement(child, tag).text = content
    return etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")

def check_all_ENSPs_of_given_taxid(protein_ans_list, taxid):
    taxid_string = str(taxid)
    for an in protein_ans_list:
        if not an.startswith(taxid_string):
            return False
    return True

def check_taxids(args_dict):
    taxid = args_dict["taxid"]
    if taxid is not None:
        return taxid
    taxid = args_dict["species"]
    if taxid is not None:
        args_dict["ERROR_species"] = "ERROR_species: argument 'species' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["species"])
        return False
    taxid = args_dict["organism"]
    if taxid is not None:
        args_dict["ERROR_organism"] = "ERROR_organism: argument 'organism' is deprecated, please use 'taxid' instead. You've provided is '{}'.".format(args_dict["organism"])
        return False

def get_function_type__and__limit_2_parent(gocat_upk):
    """
    # choices = (("all_GO", "all GO categories"),
    #            ("BP", "GO Biological Process"),
    #            ("CP", "GO Celluar Compartment"),
    #            ("MF", "GO Molecular Function"),
    #            ("UPK", "UniProt keywords"),
    #            ("KEGG", "KEGG pathways")),
    :param gocat_upk: String
    :return: Tuple(String, Bool)
    """
    if gocat_upk in {"BP", "CP", "MF", "all_GO"}:
        return "GO" #, gocat_upk
    else:
        return gocat_upk #, None

def write2file(fn, tsv):
    with open(fn, 'w') as f:
        f.write(tsv)

####################################################################################################
####################################################################################################
import os, sys, json, pickle
import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
# from plotly_tools import data_bars
from collections import defaultdict
import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
# import plotly.express as px
import plotly.graph_objects as go
sys.path.insert(0, os.path.abspath(os.path.realpath('python')))
import variables

### Colors
# DarkSlateGrey # UniProt color #71b8d3
table_background_color = "#f2f2f2" #ededed" #"#f1f1f1" ###  #f9f9f9 #F5F5F5 #a6b4cd #a8b5cf
table_highlight_color = "#b5d7eb" #"#abd5ed" # "gold abd5ed a7d0e8 # "#F6F8FA"
hover_label_color = "#43464B" # in agotool_plotly.css
plot_background_color = "#ffffff" #"rgb(255, 255, 255)" # white
plot_grid_color = "#efefef" # grey # efefef
plot_line_color = "#6C757D" #6d7787" #"#59667d" #"#4e5a6e" #"#7a7a7a" #"#2a3f5f" #"rgb(42, 63, 95)" # dark metal gray kind of blue
plot_ticklabel_color = plot_line_color
toggle_button_color = plot_line_color

### scatter plot
opacity_default = 0.7
opacity_highlight = 1
marker_line_width_default = 1 # invisible ring around points in scatter, white when points overlap
marker_line_color_default = "white"
marker_line_width_highlight = 3
marker_line_color_highlight = "#344957" #"black"
width_edges_line = 1.5
color_edge_line = "#d2d2d2" #'rgb(210,210,210)'
scatter_plot_width = 700
scatter_plot_height = 400
legend_y = -0.3

palette_dict = dict()
palette_dict[1] = ['#d95f02']
palette_dict[2] = ['#1b9e77','#d95f02']
palette_dict[3] = ['#1b9e77','#d95f02','#7570b3']
palette_dict[4] = ['#e41a1c','#377eb8','#4daf4a','#984ea3']
palette_dict[5] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e']
palette_dict[6] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']
palette_dict[7] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']
palette_dict[8] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']
palette_dict[9] = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999']
palette_dict[10] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
palette_dict[11] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99']
palette_dict[12] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
palette_dict[13] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2']
palette_dict[14] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2']
etype_2_categoryRenamed_dict = {-20: "GO cellular component TextMining",
                              -21: "GO biological process",
                              -22: "GO cellular component",
                              -23: "GO molecular function",
                              -25: "Brenda Tissue Ontology",
                              -26: "Disease Ontology",
                              -51: "UniProt keywords",
                              -52: "KEGG pathways",
                              -53: "SMART domains",
                              -54: "INTERPRO domains",
                              -55: "PFAM domains",
                              -56: "Publications (PubMed)",
                              -57: "Reactome",
                              -58: "WikiPathways"}

def table_type(df_column):
    if df_column.dtype in {np.dtype('float64'), np.dtype('float32')}:
        return "numeric"
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
            isinstance(df_column.dtype, pd.IntervalDtype) or
            isinstance(df_column.dtype, pd.Int8Dtype) or
            isinstance(df_column.dtype, pd.Int16Dtype) or
            isinstance(df_column.dtype, pd.Int32Dtype) or
            isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    elif (isinstance(df_column.dtype, pd.StringDtype) or
            isinstance(df_column.dtype, pd.BooleanDtype) or
            isinstance(df_column.dtype, pd.CategoricalDtype) or
            isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime'
    else:
        return 'any'
# rect.nsewdrag.drag

plotly_scatter_layout_template = dict(layout=go.Layout(
    {'dragmode': 'pan', 'clickmode': 'event+select',
     'legend': {'font_size': 13, 'title': {'font': {'size': 12}}, },
     'plot_bgcolor': plot_background_color,
     'margin': {'t': 30, "b": 0, "l": 0, "r": 0, },
     'xaxis': {'automargin': True, 'anchor': 'y', 'gridcolor': plot_grid_color, 'gridwidth': 1, 'linecolor': plot_line_color, 'linewidth': 2,
               'showgrid': True, 'showline': True, 'showticklabels': True, "ticks": "outside", "ticklen": 3, "tickfont_color": plot_ticklabel_color,
               "title_standoff": 8, "title_font_size": 12, "tickcolor": plot_ticklabel_color, "tickfont_size": 10,
               'zeroline': False, },
     'yaxis': {'automargin': True, 'anchor': 'x', 'gridcolor': plot_grid_color, 'gridwidth': 1, 'linecolor': plot_line_color, 'linewidth': 2,
               'showgrid': True, 'showline': True, "showticklabels": True, "ticks": "outside", "ticklen": 3, "tickfont_color": plot_ticklabel_color,
               "title_standoff": 12, "title_font_size": 12, "tickcolor": plot_ticklabel_color, "tickfont_size": 10,
               'zeroline': True, 'zerolinecolor': plot_grid_color, 'zerolinewidth': 3,}, }))

df = pd.read_csv(variables.fn_example, sep="\t")
### rename long category names
category_renamed_list = []
value_counts_series = df["etype"].value_counts(sort=False)
for etype, count in zip(value_counts_series.index, value_counts_series.values):
    try:
        categoryName = etype_2_categoryRenamed_dict[etype]
    except KeyError:
        categoryName = ""
    category_renamed_list += [categoryName] * count
df["category"] = category_renamed_list
### prioritize category with strongest signal
if sum(df["over_under"] == "o") > 0:
    category_rank_arr = df.groupby("category")["s_value"].max().sort_values(ascending=False).index.values
else:
    category_rank_arr = df.groupby("category")["s_value"].min().sort_values(ascending=True).index.values
df["category"] = pd.Categorical(df["category"], category_rank_arr)
df = df.sort_values(["category", "rank"]).reset_index(drop=True)
### debug
# df["category"] = df["category"].apply(lambda s: s[:4])
# df.sort_values(["rank"])
# df = df.groupby("etype").head(3)
# df["FG_IDs"] = ""
df["id"] = df["term"]
# print(df["term"].reset_index(drop=True))
df.set_index("id", inplace=True, drop=False)
# del df["id"]
# del df["FG_IDs"]
df = df.drop(columns=["rank_2_transparency", "FG_count_2_circle_size", "funcEnum"]) # "id",
p_value = "p value"
FDR = "false discovery rate"
effect_size = "effect size"
over_under = "over under"
hierarchical_level = "level"
s_value = "s value"
ratio_in_FG = "ratio in FG"
ratio_in_BG = "ratio in BG"
FG_IDs = "foreground identifiers"
BG_IDs = "background identifiers"
FG_count = "foreground count"
BG_count = "background count"
FG_n = "foreground n"
BG_n = "background n"
rank = "rank"
etype = "etype"
term = "term"
description = "description"
logFDR = "logFDR"
year = "year"
category = "category"
color = "color"
effectSize = "effect size"
marker_line_width = "marker_line_width"
marker_line_color = "marker_line_color"
id_ = "id"
opacity = "opacity"

all_terms_set = set(df[term].values)
color_discrete_map = {category_: color_hex_val for category_, color_hex_val in zip(df[category].unique(), palette_dict[df.etype.unique().shape[0]])}
df[color] = df[category].apply(lambda x: color_discrete_map[x])

df = df.rename(columns={"over_under": over_under, "hierarchical_level": hierarchical_level, "p_value": p_value, "FDR": FDR, "effectSize": effect_size, "s_value": s_value, "ratio_in_FG": ratio_in_FG, "ratio_in_BG": ratio_in_BG, "FG_IDs": FG_IDs, "BG_IDs": BG_IDs, "FG_count": FG_count, "BG_count": BG_count, "FG_n": FG_n, "BG_n": BG_n})

cols_compact = [rank, term, description, FDR, effect_size]
cols_sort_order_comprehensive = [s_value, term, description, p_value, FDR, logFDR, effect_size, category, over_under, hierarchical_level, year, FG_IDs, BG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, rank]
hidden_columns = [p_value, ratio_in_FG, ratio_in_BG, FG_count, BG_count, FG_n, BG_n, FG_IDs, etype, logFDR, year, color, rank, category, hierarchical_level, over_under, marker_line_width, marker_line_color, id_, opacity]
# hidden_columns = [marker_line_width, marker_line_color, id_]
df_cols_set = set(df.columns)
cols_set_temp = set(cols_sort_order_comprehensive).intersection(df_cols_set)
cols = [colName for colName in cols_sort_order_comprehensive if colName in cols_set_temp]
df = df[cols + list(df_cols_set - set(cols))]


df[marker_line_width] = marker_line_width_default
df[marker_line_color] = marker_line_color_default
df[opacity] = opacity_default
max_marker_size, min_marker_size = 30, 4
sizeref = 2.0 * max(df[FG_count]) / (max_marker_size ** 2)
# button_reset_plot_n_click = 0
### Network edges based on relationship within Ontology
term_2_edges_dict = defaultdict(lambda: {"X_points": [], "Y_points": [], "Weights": [], "Nodes": []})
term_2_edges_dict.update(pickle.load(open(os.path.join(variables.PYTHON_DIR, "term_2_edges_dict.p"), "rb")))

colName_attributes = []
for colName in df.columns:
    if colName in {"term"}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": False, "deletable": False, "type": table_type(df[colName])})
    elif colName in {p_value, FDR, logFDR}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".2e"}})
    elif colName in {effect_size, s_value, ratio_in_FG, ratio_in_BG}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".2f"}})
    elif colName in {FG_count, BG_count, FG_n, BG_n, etype}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".0f"}})
    else:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName])})

def create_plotly_scatter(dff=df):
    fig = go.Figure()
    for category_name, group in dff.groupby(category):
        fig.add_trace(go.Scatter(name=category_name, x=group[logFDR].tolist(), y=group[effectSize].tolist(), ids=group[term].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_color=group[color].iloc[0], marker_size=group[FG_count], marker_opacity=group[opacity], marker_sizemin=min_marker_size, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color], customdata=[list(ele) for ele in zip(group[term], group[description], group[FG_count])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
    fig.update_layout(hoverlabel=dict(font_size=12), template=plotly_scatter_layout_template, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, font_size=12, orientation="h", yanchor="bottom", y=legend_y, xanchor="left", x=0, ), ) # , itemclick="toggleothers", itemdoubleclick="toggle"
    # fig.update_layout(autosize=False, width=scatter_plot_width, height=scatter_plot_height, )
    fig.update_layout(autosize=True)
    fig_data_as_json = json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)
    fig_layout_as_json = json.dumps(fig.layout, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_data_as_json, fig_layout_as_json

# def df_2_html_table(df, session_id, session_folder_absolute, form, errors=(), compact_or_comprehensive="compact"):
def df_2_html_table(session_id, session_folder_absolute, df=df):
    df_all_etypes = df
    args_dict = {}

    file_name = "results_orig" + session_id + ".tsv"
    fn_results_orig_absolute = os.path.join(session_folder_absolute, file_name)
    df_all_etypes.to_csv(fn_results_orig_absolute, sep="\t", header=True, index=False)
    # if args_dict["enrichment_method"] != "characterize_foreground":
    #     df_all_etypes = df_all_etypes.sort_values(["etype", "rank"])
    etype_2_rowsCount_dict, etype_2_df_as_html_dict = {}, {}
    df_as_html_dict = {}
    p_value = "p value"
    FDR = "p value corrected"
    effect_size = "effect size"
    over_under = "over under"
    hierarchical_level = "level"
    s_value = "s value"
    ratio_in_FG = "ratio in FG"
    ratio_in_BG = "ratio in BG"
    FG_IDs = "FG IDs"
    BG_IDs = "BG IDs"
    FG_count = "FG count"
    BG_count = "BG count"
    FG_n = "FG n"
    BG_n = "BG n"
    rank = "rank"
    df_all_etypes = df_all_etypes.rename(columns={"over_under": over_under, "hierarchical_level": hierarchical_level, "p_value": p_value, "FDR": FDR, "effectSize": effect_size, "s_value": s_value, "ratio_in_FG": ratio_in_FG, "ratio_in_BG": ratio_in_BG, "FG_IDs": FG_IDs, "BG_IDs": BG_IDs, "FG_count": FG_count, "BG_count": BG_count, "FG_n": FG_n, "BG_n": BG_n})
    pd.set_option('colheader_justify', 'center')

    # show year, not hierarchy
    cols_sort_order_PMID = ['rank', 'term', 'description', 'year', over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]
    # show hierarchy, not year
    cols_sort_order_hierarchy = ['rank', 'term', 'description', hierarchical_level, over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]
    # not hiearachy, not year
    cols_sort_order_rest = ['rank', 'term', 'description', over_under, p_value, FDR, effect_size, s_value, ratio_in_FG, ratio_in_BG, FG_count, FG_n, BG_count, BG_n, FG_IDs, BG_IDs]

    def helper_format_to_html(df):
        return df.to_html(index=False, border=0, classes=["display table dataTable_DBL dataTable table-striped"], table_id="dataTable_DBL_id", justify="left",
            formatters={"effect size": lambda x: "{:.2f}".format(x), FDR: lambda x: "{:.2E}".format(x), p_value: lambda x: "{:.2E}".format(x), s_value: lambda x: "{:.2f}".format(x),
                        ratio_in_FG: lambda x: "{:.2f}".format(x), ratio_in_BG: lambda x: "{:.2f}".format(x), FG_count: lambda x: "{:.0f}".format(x)})

    # if args_dict["o_or_u_or_both"] != "both": # don't hide "over under"
    #     cols_sort_order_PMID.remove(over_under)
    #     cols_sort_order_hierarchy.remove(over_under)
    #     cols_sort_order_rest.remove(over_under)
    #
    # if args_dict["enrichment_method"] not in {"compare_samples"}: # "compare_groups"
    #     cols_sort_order_PMID.remove(BG_IDs)
    #     cols_sort_order_hierarchy.remove(BG_IDs)
    #     cols_sort_order_rest.remove(BG_IDs)
    #
    # if args_dict["enrichment_method"] == "characterize_foreground":
    #     cols_2_remove = (BG_IDs, BG_n, BG_count, ratio_in_BG, over_under, p_value, FDR, effect_size, s_value, rank)
    #     cols_sort_order_PMID = [ele for ele in cols_sort_order_PMID if ele not in cols_2_remove]
    #     cols_sort_order_hierarchy = [ele for ele in cols_sort_order_hierarchy if ele not in cols_2_remove]
    #     cols_sort_order_rest = [ele for ele in cols_sort_order_rest if ele not in cols_2_remove]

    # for etype, group in df_all_etypes.groupby("etype"):
    #     num_rows = group.shape[0]
    #     if num_rows > 0:
    #         etype_2_rowsCount_dict[etype] = num_rows
    #         if etype in variables.PMID: # -56 is the only one with "year"
    #             etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_PMID])
    #         elif etype in variables.entity_types_with_ontology:
    #             etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_hierarchy])
    #         else:
    #             etype_2_df_as_html_dict[etype] = helper_format_to_html(group[cols_sort_order_rest])

    # return render_template('results_comprehensive.html', etype_2_rowsCount_dict=etype_2_rowsCount_dict, etype_2_df_as_html_dict=etype_2_df_as_html_dict, errors=errors, file_path=file_name, session_id=session_id, form=form, args_dict=args_dict)
    print(df.shape)
    df_as_html_dict = helper_format_to_html(df)
    return df_as_html_dict


if __name__ == "__main__":
    create_plotly_scatter()