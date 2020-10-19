import os, sys, logging, time, argparse
import datetime
from collections import defaultdict
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
from lxml import etree
import flask
from flask import render_template, request, send_from_directory, jsonify
from flask_restful import reqparse, Api, Resource
from werkzeug.wrappers import Response
import wtforms
from wtforms import fields
import markdown
from flaskext.markdown import Markdown
from ast import literal_eval
from plotly_tools import data_bars
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
sys.path.insert(0, os.path.abspath(os.path.realpath('python')))
import variables

palette_dict = {}
palette_dict[1] = ['#d95f02']
palette_dict[2] = ['#1b9e77','#d95f02']
palette_dict[3] = ['#1b9e77','#d95f02','#7570b3']
palette_dict[4] = ['#e41a1c','#377eb8','#4daf4a','#984ea3'] # ['#1b9e77','#d95f02','#7570b3','#e7298a']
palette_dict[5] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e']
palette_dict[6] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']
palette_dict[7] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']
palette_dict[8] = ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']
palette_dict[9] = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999']
palette_dict[10] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
palette_dict[11] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99']
palette_dict[12] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
palette_dict[13] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'] # palettes.d3['Category20'][13]
palette_dict[14] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'] # palettes.d3['Category20'][14]

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

layout_template_DBL_v2 = dict(layout=go.Layout({'dragmode': 'lasso', 'autosize': True, 'clickmode': 'event+select',
                                                'legend': {'itemsizing': 'constant', 'font_size': 14, 'title': {'font': {'size': 12}}, 'tracegroupgap': 0},
                                                'margin': {'t': 60}, 'plot_bgcolor': 'rgb(255, 255, 255)',
                                                'xaxis': {'anchor': 'y', 'gridcolor': 'rgb(239, 239, 239)', 'gridwidth': 1, 'linecolor': 'rgb(42, 63, 95)', 'linewidth': 2, 'showgrid': True, 'showline': True, 'showticklabels': True, 'zeroline': False, "ticks": "outside", },
                                                'yaxis': {'anchor': 'x', 'gridcolor': 'rgb(239, 239, 239)', 'gridwidth': 1, 'linecolor': 'rgb(42, 63, 95)', 'linewidth': 2, 'showgrid': True, 'showline': True, 'zeroline': True, 'zerolinecolor': 'rgb(239, 239, 239)', 'zerolinewidth': 3, "showticklabels": True, "ticks": "outside", }, }))
max_marker_size = 40
df = pd.read_csv(variables.fn_example, sep="\t")
df = df.groupby("etype").tail(3)
df["id"] = df["term"]
df.set_index("id", inplace=True, drop=False)
df = df.drop(columns=["id", "rank_2_transparency", "FG_count_2_circle_size", "funcEnum"])
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

color_discrete_map = {category_: color_hex_val for category_, color_hex_val in zip(df[category].unique(), palette_dict[df.etype.unique().shape[0]])}
df[color] = df[category].apply(lambda x: color_discrete_map[x])

df = df.rename(columns={"over_under": over_under, "hierarchical_level": hierarchical_level, "p_value": p_value, "FDR": FDR, "effectSize": effect_size, "s_value": s_value, "ratio_in_FG": ratio_in_FG, "ratio_in_BG": ratio_in_BG, "FG_IDs": FG_IDs, "BG_IDs": BG_IDs, "FG_count": FG_count, "BG_count": BG_count, "FG_n": FG_n, "BG_n": BG_n})

cols_compact = [rank, term, description, FDR, effect_size]
cols_sort_order_comprehensive = [category, term, hierarchical_level, description, over_under, p_value, FDR, logFDR, effect_size, s_value, year, FG_IDs, BG_IDs, FG_count, FG_n, BG_count, BG_n, ratio_in_FG, ratio_in_BG, rank]
hidden_columns = [p_value, ratio_in_FG, ratio_in_BG, FG_count, BG_count, FG_n, BG_n, FG_IDs, etype, logFDR, year, color, rank, category, hierarchical_level, over_under, marker_line_width, marker_line_color]
df_cols_set = set(df.columns)
cols_set_temp = set(cols_sort_order_comprehensive).intersection(df_cols_set)
cols = [colName for colName in cols_sort_order_comprehensive if colName in cols_set_temp]
df = df[cols + list(df_cols_set - set(cols))]
df[marker_line_width] = 1
df[marker_line_color] = "white"

colName_attributes = []
for colName in df.columns:
    if colName in {"term"}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": False, "deletable": False, "type": "text"})
    elif colName in {p_value, FDR}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": "numeric", "format": {"specifier": ".2e"}})
    elif colName in {effect_size, s_value, ratio_in_FG, ratio_in_BG}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": "numeric", "format": {"specifier": ".2f"}})
    elif colName in {FG_count, BG_count, FG_n, BG_n, etype}:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": "numeric", "format": {"specifier": ".0f"}})
    else:
        colName_attributes.append({"name": colName, "id": colName, "hideable": True, "type": "text"})

print(">"*50)
print("---  restarting  {} ---".format(datetime.datetime.now()))
print("<"*50)

bs = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/materia/bootstrap.min.css"
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[bs]) # dbc.themes.BOOTSTRAP

data_table_dbl = dash_table.DataTable(
            id='main_datatable',
            columns=colName_attributes,
            hidden_columns=hidden_columns,
            data=df.to_dict('records'),  # the contents of the table
            editable=False,              # allow editing of data inside all cells
            # filter_action="native",      # allow filtering of data by user ('native') or not ('none')
            sort_action="native",        # enables data to be sorted per-column by user or not ('none')
            sort_mode="multi",           # sort across 'multi' or 'single' columns
            column_selectable="multi",   # allow users to select 'multi' or 'single' columns
            row_selectable="multi",      # allow users to select 'multi' or 'single' rows
            selected_columns=[],         # ids of columns that user selects
            selected_rows=[],            # indices of rows that user selects
            page_action= "native", #"native",        # all data is passed to the table up-front or not ('none')
            # page_current=0,              # page number that user is on
            # page_size=10,                # number of rows visible per page
            style_cell={                 # ensure adequate header width when text is shorter than cell's text
                'minWidth': "10px", "width": "50px", "maxWidth": "400px", #'width': 60,
                "fontSize": "12px", "font-family": "sans-serif", # roboto,
                "text_align": "center",
                "border": "0px",
            },
            style_cell_conditional=
                [{"if": {"column_id": term}, "textAlign": "left", "width": "120px",}]
                +
                [{"if": {"column_id": description}, "textAlign": "left", "width": "400px",}]
                +
                [{'if': {'column_id': category}, 'textAlign': 'left'}]
                +
                [{"if": {"column_id": FG_IDs}, "width": "120px"}]
                +
                [{"if": {"column_id": colName}, "width": "110px"} for colName in [FDR, effectSize, s_value]],
            style_data={
                'whiteSpace': 'normal',
                "height": "14px",
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
            },
            tooltip_data=[{
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
                } for row in df.to_dict('rows')
                ],
            tooltip_duration=None,
            # style_data_conditional=(
            #                         [{'if': {'row_index': 'odd'},
            #                           'backgroundColor': "#F5F5F5",}]
            #                         +
            #                         [{"if": {"state": "selected"},
            #                           "backgroundColor": "inherit !important",
            #                           "border": "inherit !important",
            #                           "text_align": "inherit !important",}]
            #                         +
            #                         [{"if": {"state": "active"},
            #                           "backgroundColor": "inherit !important",
            #                           "border": "inherit !important",
            #                           "text_align": "inherit !important",}]
            #                         +
            #                         data_bars(df, s_value) # Format active cells *********************************
            #                         ),
            style_header={
                'backgroundColor': 'white',
                'borderBottom': '1px solid black',
                "fontSize": "13px",
                'fontWeight': 'bold',
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                "text-indent": "0.25em",
                },
            style_as_list_view=True,
            )

# Div general_div
#   children
#     Div first_row
#       children
#         Graph main_graph
#     Div second_row
#       children
#         DataTable main_table

sizeref = 2.0 * max(df[FG_count]) / (max_marker_size ** 2)

app.layout = html.Div(id='general_div',
    children=[
        html.Div(id='first_row',
            children=[
                # dbc.Row(
                #     dbc.Col(
                #         html.Div(id='main_datatable'),
                    html.Div(dcc.Graph(id='scatter_plot',
                     figure=px.scatter(data_frame=df, x=logFDR, y=effectSize, color=category, size=FG_count, hover_data={term: True, description: True, FG_count: True, logFDR: False, effectSize: False, category: False, color: False, }, custom_data=[term, description, FG_count, color], color_discrete_map=color_discrete_map).update_traces(hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", mode='markers', marker={'sizemode': 'area', 'sizeref': sizeref, 'sizemin': 3, }).update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.5, xanchor="left", x=0)))),
                        # xs={"size": 12, "offset": 0},
                        # sm={"size": 12, "offset": 0},
                        # md={"size": 8, "offset": 2},
                        # lg={"size": 6, "offset": 3},
                    #     ),
                    # ),
                ]
            ),

        html.Br(),

        html.Div(id="second_row",
            children=[
                # dbc.Row(
                #     dbc.Col(
                        html.Div(data_table_dbl, className="d-flex justify-content-center"),
                #         html.Div(),
                    #     ),
                    # ),
                ]
            ),

        html.Br(),

        ]
)
#
# @app.callback(
#     Output(component_id='scatter-container', component_property='children'),
#     [Input(component_id='main_datatable', component_property="derived_virtual_data"),
#      Input(component_id='main_datatable', component_property='derived_virtual_selected_rows'),
#      Input(component_id='main_datatable', component_property='derived_virtual_selected_row_ids'),
#      Input(component_id='main_datatable', component_property='selected_rows'),
#      Input(component_id='main_datatable', component_property='derived_virtual_indices'),
#      Input(component_id='main_datatable', component_property='derived_virtual_row_ids'),
#      Input(component_id='main_datatable', component_property='active_cell'),
#      Input(component_id='main_datatable', component_property='selected_cells')])
# def update_scatter(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
#                order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
#     dff = df if len(all_rows_data) == 0 else pd.DataFrame(all_rows_data)
#     sizeref = 2.0 * max(dff[FG_count]) / (max_marker_size ** 2)
#     return [dcc.Graph(id='scatter-plot',
#                  figure=px.scatter(data_frame=dff, x=logFDR, y=effectSize, color=category, size=FG_count, hover_data={term: True, description: True, FG_count: True, logFDR: False, effectSize: False, category: False, color: False, }, custom_data=[term, description, FG_count, color], color_discrete_map=color_discrete_map).update_traces(hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", mode='markers', marker={'sizemode': 'area', 'sizeref': sizeref, 'sizemin': 3, }).update_layout(hoverlabel=dict(font_size=12), template=layout_template_DBL_v2, title=None, xaxis_title="-log(FDR)", yaxis_title="effect size", legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.5, xanchor="left", x=0)))]

def update_table_style(selectedData):
    """
    https://stackoverflow.com/questions/62516573/update-dash-table-by-selecting-points-on-scatter-plot?answertab=active#tab-top
    """
    if selectedData is not None:
        selected_styles = [{'if': {'row_index': point['pointIndex']},
                            'backgroundColor': 'gold'} for point in selectedData['points']]
        table_style_conditions = (selected_styles + [{'if': {'row_index': 'odd'}, 'backgroundColor': "#F5F5F5", }] + [{"if": {"state": "selected"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }] + [{"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }] + data_bars(df, s_value))
    else:
        table_style_conditions = ([{'if': {'row_index': 'odd'}, 'backgroundColor': "#F5F5F5", }] + [{"if": {"state": "selected"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }] + [{"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }] + data_bars(df, s_value))
    return table_style_conditions

@app.callback(Output('main_datatable', 'style_data_conditional'),
              [Input('scatter_plot', 'selectedData')])
def display_selected_data(selectedData):
    table_style_conditions = update_table_style(selectedData)
    return table_style_conditions


if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port="5922")
