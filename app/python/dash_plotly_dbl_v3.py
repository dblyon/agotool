import os, sys, json
import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
# from plotly_tools import data_bars
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
sys.path.insert(0, os.path.abspath(os.path.realpath('python')))
import variables


table_background_color = "#f2f2f2" #ededed" #"#f1f1f1" ###  #f9f9f9 #F5F5F5 #a6b4cd #a8b5cf
highlight_color = "#abd5ed" # "gold abd5ed a7d0e8
hover_label_color = "#43464B" # in agotool_plotly.css
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
# UniProt color #71b8d3

entityType_2_functionType_dict = {-20: "Gene Ontology cellular component TEXTMINING",
                              -21: "Gene Ontology biological process",
                              -22: "Gene Ontology cellular component",
                              -23: "Gene Ontology molecular function",
                              -25: "Brenda Tissue Ontology",
                              -26: "Disease Ontology",
                              -51: "UniProt keywords",
                              -52: "KEGG (Kyoto Encyclopedia of Genes and Genomes)",
                              -53: "SMART (Simple Modular Architecture Research Tool)",
                              -54: "INTERPRO",
                              -55: "PFAM (Protein FAMilies)",
                              -56: "PMID (PubMed IDentifier)",
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

layout_template_DBL_v2 = dict(layout=go.Layout({'dragmode': 'lasso', 'clickmode': 'event+select', # 'autosize': True
                                                'legend': {'itemsizing': 'constant', 'font_size': 14, 'title': {'font': {'size': 12}}, 'tracegroupgap': 6},
                                                'margin': {'t': 60}, 'plot_bgcolor': 'rgb(255, 255, 255)',
                                                'xaxis': {'anchor': 'y', 'gridcolor': 'rgb(239, 239, 239)', 'gridwidth': 1, 'linecolor': 'rgb(42, 63, 95)', 'linewidth': 2, 'showgrid': True, 'showline': True, 'showticklabels': True, 'zeroline': False, "ticks": "outside", },
                                                'yaxis': {'anchor': 'x', 'gridcolor': 'rgb(239, 239, 239)', 'gridwidth': 1, 'linecolor': 'rgb(42, 63, 95)', 'linewidth': 2, 'showgrid': True, 'showline': True, 'zeroline': True, 'zerolinecolor': 'rgb(239, 239, 239)', 'zerolinewidth': 3, "showticklabels": True, "ticks": "outside", }, }))
df = pd.read_csv(variables.fn_example, sep="\t")

### prioritize category with strongest signal
if sum(df["over_under"] == "o") > 0:
    category_rank_arr = df.groupby("category")["s_value"].max().sort_values(ascending=False).index.values
else:
    category_rank_arr = df.groupby("category")["s_value"].min().sort_values(ascending=True).index.values
df["category"] = pd.Categorical(df["category"], category_rank_arr)
df = df.sort_values(["category", "rank"]).reset_index(drop=True)

# df.sort_values(["rank"])
# df = df.groupby("etype").head(3)
df["id"] = df["term"]
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
FG_IDs = "FG IDs"
BG_IDs = "BG IDs"
FG_count = "FG count"
BG_count = "BG count"
FG_n = "FG n"
BG_n = "BG n"
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

color_discrete_map = {category_: color_hex_val for category_, color_hex_val in zip(df[category].unique(), palette_dict[df.etype.unique().shape[0]])}
df[color] = df[category].apply(lambda x: color_discrete_map[x])

df = df.rename(columns={"over_under": over_under, "hierarchical_level": hierarchical_level, "p_value": p_value, "FDR": FDR, "effectSize": effect_size, "s_value": s_value, "ratio_in_FG": ratio_in_FG, "ratio_in_BG": ratio_in_BG, "FG_IDs": FG_IDs, "BG_IDs": BG_IDs, "FG_count": FG_count, "BG_count": BG_count, "FG_n": FG_n, "BG_n": BG_n})

cols_compact = [rank, term, description, FDR, effect_size]
cols_sort_order_comprehensive = [s_value, term, description, FDR, effect_size, category, over_under, hierarchical_level, year, p_value, logFDR, FG_IDs, BG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, rank]
hidden_columns = [p_value, ratio_in_FG, ratio_in_BG, FG_count, BG_count, FG_n, BG_n, FG_IDs, etype, logFDR, year, color, rank, category, hierarchical_level, over_under, marker_line_width, marker_line_color, id_]
df_cols_set = set(df.columns)
cols_set_temp = set(cols_sort_order_comprehensive).intersection(df_cols_set)
cols = [colName for colName in cols_sort_order_comprehensive if colName in cols_set_temp]
df = df[cols + list(df_cols_set - set(cols))]

df[marker_line_width] = 1
df[marker_line_color] = "white"
max_marker_size = 40
min_marker_size = 4
sizeref = 2.0 * max(df[FG_count]) / (max_marker_size ** 2)


colName_attributes = []
for colName in df.columns:
    if colName in {"term"}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": False, "deletable": False, "type": table_type(df[colName])})
    elif colName in {p_value, FDR, logFDR}:
        # colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": "numeric", "format": {"specifier": ".2e"}})
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".2e"}})
    elif colName in {effect_size, s_value, ratio_in_FG, ratio_in_BG}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".2f"}})
    elif colName in {FG_count, BG_count, FG_n, BG_n, etype}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName]), "format": {"specifier": ".0f"}})
    else:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": table_type(df[colName])})

def data_bars_dbl(df, column):
    """
    css style s_value column with horizontal bars,
     the length of the bar depends on s_value,
     the direction of the sign (positive or negative value),
     the color corresponds to the category and should be identical to the plot
    magnitude calculated for the whole dataset
    depends on 'row_id' to exist in dash_table --> generated via 'id' column in pd.DataFrame
    {'if': {'filter_query': '{s value} >= -0.4632684138910674 && {s value} < -0.4509838870118037', 'column_id': 's value'}, 'background': 'linear-gradient(90deg, #0074D9 0%, #0074D9 1.0%, white 1.0%, white 100%)', 'paddingBottom': 2, 'paddingTop': 2}
    {'if': {'filter_query': 'row_id' == 'KW-0539' && 'column_id' == 's value', 'background': 'linear-gradient(90deg, #0074D9 0%, #0074D9 1.0%, white 1.0%, white 100%)', 'paddingBottom': 2, 'paddingTop': 2}
    if column_id == 's value' && row_id == 'KW-0539' -->
    'row_id' is not a valid attribute for whatever reason
    """
    styles = []
    starting_point_right_side = 100 - 50 + 0.5/2 # left_and_right_side_delimiter_width = 0.5
    min_, max_ = df[column].min(), df[column].max()
    total = abs(max_) + abs(min_)
    for category_, group in df.groupby(category):
        for term, value in group[column].iteritems():
            color_ = group[color].iloc[0]
            percentage = 50 * abs(value) / total
            if value > 0: # to the right.
                width = percentage + starting_point_right_side
                color_bar = "transparent 0%, transparent 49.75%, #000000 49.75%, #000000 50.25%, {} 50.25%, {} {}%, transparent {}%, transparent 100.0%".format(color_, color_, width, width)
            elif value < 0: # to the left
                empty_space_left = 50 - percentage
                width = empty_space_left + percentage
                color_bar = "transparent 0%, transparent {}%, {} {}%, {} {}%, #000000 49.75%, #000000 50.25%, transparent 50.25%, transparent 100.0%".format(empty_space_left,color_, empty_space_left, color_, width)
            else: # value is 0 or NaN or ? actually shouldn't happen at all
                color_bar = ""
            styles.append({"if": {"column_id": "s value", "filter_query": "{id} = " + term, 'row_index': 'even'}, "background": "linear-gradient(90deg, {} )".format(color_bar), "paddingBottom": 1, "paddingTop": 1})
            styles.append({'if': {"column_id": "s value", "filter_query": "{id} = " + term, 'row_index': 'odd'}, "background": "linear-gradient(90deg, {} ) rgb(242, 242, 242) ".format(color_bar), "paddingBottom": 1, "paddingTop": 1})
    return styles

# style_data_conditional_basic = [
#                                 {"if": {"state": "selected"}, "backgroundColor": highlight_color, "border": "inherit !important", "text_align": "inherit !important",},
#                                 {"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important",},
#                                 ] + data_bars_dbl(df, s_value)
style_data_conditional_basic = data_bars_dbl(df, s_value)

# print(">"*50)
print("<<< restarting {} >>>".format(datetime.datetime.now()))
bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/materia/bootstrap.min.css" # bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/litera/bootstrap.min.css"
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[bs]) # dbc.themes.BOOTSTRAP


data_table_dbl = dash_table.DataTable(
            id='main_datatable',
            columns=colName_attributes,
            hidden_columns=hidden_columns,
            data=df.to_dict('records'),  # the contents of the table # drop(columns=[color, marker_line_color, marker_line_width])
            editable=False,              # allow editing of data inside all cells
            filter_action="native",      # allow filtering of data by user ('native') or not ('none')
            sort_action="native",        # enables data to be sorted per-column by user or not ('none')
            column_selectable="multi",   # allow users to select 'multi' or 'single' columns
            row_selectable="multi",      # allow users to select 'multi' or 'single' rows
            selected_columns=[],         # ids of columns that user selects
            selected_rows=[],            # indices of rows that user selects
            page_action= "none", #"native",        # all data is passed to the table up-front or not ('none')
            style_table={'height': '400px',
                         'overflowX': 'auto',
                         'overflowY': 'auto',
                         },
            style_data_conditional=[], # overwritten by JS callback
            style_data={ # overflow cells' content into multiple lines
                'whiteSpace': 'normal',
                "height": "14px",
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
                'if': {'row_index': 'odd'}, 'backgroundColor': table_background_color,
            },
            style_filter_conditional=[],
            style_filter={},
            style_header_conditional=[],
            style_header={'backgroundColor': 'white', 'borderBottom': '1px solid black', "fontSize": "13px", 'fontWeight': 'bold', 'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left', "text-indent": "0.25em", },
            style_cell_conditional=[{"if": {"column_id": s_value}, "width": "80px", }]  # 100
                                   + [{"if": {"column_id": term}, "textAlign": "left", "width": "100px", }]  # 120
                                   + [{"if": {"column_id": description}, "textAlign": "left", "width": "250px", }]  # 4000
                                   + [{'if': {'column_id': category}, 'textAlign': 'left', "width": "80px"}] + [{"if": {"column_id": FG_IDs}, "width": "220px"}]  # 120
                                   + [{"if": {"column_id": colName}, "width": "100px"} for colName in [FDR, effectSize]],  # 110
            style_cell={                 # ensure adequate header width when text is shorter than cell's text
                'minWidth': "10px", "width": "50px", "maxWidth": "400px", #'width': 60,
                "fontSize": "12px",
                "font-family": "sans-serif,roboto,Helvetica Neue,Arial,Noto Sans",
                "text_align": "center",
                "border": "0px",
            },
            tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()} for row in df.to_dict('rows')
                ],
            tooltip_duration=None,
            style_as_list_view=True,
            fixed_rows={'headers': True},
            )


@app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
               Output(component_id="scatter_container", component_property="children")],
              [Input(component_id="main_datatable", component_property="selected_rows"),
               Input(component_id="main_datatable", component_property="derived_virtual_data"),
               Input(component_id="main_datatable", component_property='derived_virtual_selected_rows'),
               Input(component_id="main_datatable", component_property='derived_virtual_selected_row_ids'),
               Input(component_id="main_datatable", component_property='derived_virtual_indices'),
               Input(component_id="main_datatable", component_property='derived_virtual_row_ids'),
               Input(component_id="main_datatable", component_property='active_cell'),
               Input(component_id="main_datatable", component_property='selected_cells')])
def highlight_dataTableRows_and_pointsInScatter_on_selectInDataTable(selected_rows, derived_virtual_data, derived_virtual_selected_rows, derived_virtual_selected_row_ids, derived_virtual_indices, derived_virtual_row_ids, active_cell, selected_cells):
    # print("calling highlight_dataTableRows_and_pointsInScatter_on_selectInDataTable")
    if derived_virtual_data is None or len(derived_virtual_data) == 0:
        dff = df
    else:
        dff = pd.DataFrame(derived_virtual_data)
    # dff = df if len(derived_virtual_data) == 0 else pd.DataFrame(derived_virtual_data)
    dff[marker_line_width] = 1
    dff[marker_line_color] = "white"
    dff.loc[derived_virtual_selected_rows, marker_line_width] = 3
    dff.loc[derived_virtual_selected_rows, marker_line_color] = hover_label_color

    fig = go.Figure()
    for category_name, group in dff.groupby(category):
        fig.add_trace(go.Scatter(name=category_name, x=group[logFDR].tolist(), y=group[effectSize].tolist(), ids=group[term].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_color=group[color].iloc[0], marker_size=group[FG_count], marker_sizemin=min_marker_size, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group[marker_line_width], marker_line_color=group[marker_line_color], customdata=[list(ele) for ele in zip(group[term], group[description], group[FG_count])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
    fig.update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, font_size=12, orientation="h", yanchor="bottom", y=-0.5, xanchor="left", x=0)) # legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.8, xanchor="left", x=0)
    scatter_plot_fig = dcc.Graph(id='scatter_plot', figure=fig)

    if selected_rows is not None:
        selected_term_list = dff.loc[selected_rows, term].tolist()
        style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': highlight_color} for term in selected_term_list]
        return style_data_conditional_extension + style_data_conditional_basic, scatter_plot_fig
    else:
        return style_data_conditional_basic, scatter_plot_fig


### app
app.layout = html.Div(id='general_div', className="container-fluid",
    children=[

        dbc.Row([
            dbc.Col(html.Div(id="scatter_container", children=[]), xs={"size": 12}, sm={"size": 12}, md={"size": 10}, lg={"size": 8},),
            ], justify="center",),

        html.Br(),

        dbc.Row([
            # dbc.Col(width=2),
            dbc.Col(html.Div(data_table_dbl), xs={"size": 12}, sm={"size": 12}, md={"size": 10}, lg={"size": 10},),
            # dbc.Col(width=2),
        ], justify="center",),


        html.Br(),

        ],)


if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)
# ToDo
# - click on points to toggle labels # https://plotly.com/python/click-events/
# - hover over point to show lines between points of hierarchical connection
# - highlight works on wrong columns when sorting
# - Toggle columns button style --> CSS button "info" or something
# - export as SVG
# click plot and highlight in table
# https://dash.plotly.com/datatable/interactivity
# ### https://stackoverflow.com/questions/62516573/update-dash-table-by-selecting-points-on-scatter-plot?answertab=active#tab-top

# https://codeburst.io/notes-from-the-latest-plotly-js-release-b035a5b43e21 and below
# https://github.com/plotly/dash-recipes/blob/46d8419b267020fdbd1644c31cbe2c3437b24c0b/dash-plotly-132-selected-attributes.py

### Bugs
# sort table and select row --> highlights wrong row