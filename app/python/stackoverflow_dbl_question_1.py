import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

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
palette_dict[14] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'] # palettes.d3[
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


df = pd.DataFrame.from_dict(
    {'term': {0: 'GOCC:0043229', 1: 'GOCC:0098588', 2: 'GOCC:0005730', 3: 'GO:0005730', 4: 'GO:0005783', 5: 'GO:0031410', 6: 'KW-0732', 7: 'KW-0156', 8: 'KW-0010'},
    'description': {0: 'Intracellular organelle', 1: 'Bounding membrane of organelle', 2: 'Nucleolus', 3: 'nucleolus', 4: 'endoplasmic reticulum', 5: 'cytoplasmic vesicle', 6: 'Signal', 7: 'Chromatin regulator', 8: 'Activator'},
     'FG_count': {0: 370, 1: 92, 2: 126, 3: 31, 4: 63, 5: 23, 6: 9, 7: 410, 8: 500},
     'logFDR': {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 5, 7: 1, 8: 2},
     'effectSize': {0: 0.053, 1: -0.049, 2: 0.046, 3: 0.047, 4: -0.040, 5: -0.027, 6: -0.024, 7: 0.025, 8: 0.025},
     'category': {0: 'TM', 1: 'TM', 2: 'TM', 3: 'GOCC', 4: 'GOCC', 5: 'UPK', 6: 'UPK', 7: 'GOCC', 8: 'UPK'}})
# df["id"] = df["term"]
# df = df.set_index("id", drop=False)
color_discrete_map = {category_: color_hex_val for category_, color_hex_val in zip(df[category].unique(), palette_dict[df.category.unique().shape[0]])}
df[color] = df[category].apply(lambda x: color_discrete_map[x])
df["marker_line_width"] = 1
df["marker_line_color"] = "white"

style_data_conditional_basic = [{"if": {"state": "selected"}, "backgroundColor": "gold", "border": "inherit !important", "text_align": "inherit !important", }] + [{"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }]

app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

max_marker_size = 40
sizeref = 2.0 * max(df["FG_count"]) / (max_marker_size ** 2)
app.layout = html.Div(id='general_div',
    children=[
        html.Div(id='first_row',
            children=[
                    # html.Div(dcc.Graph(id='scatter_plot',
                    #  figure=px.scatter(data_frame=df, x="logFDR", y="effectSize", color="category", size="FG_count", hover_data={"term": True, "description": True, "FG_count": True, "logFDR": False, "effectSize": False, "category": False }, custom_data=["term", "description", "FG_count"]).update_traces(hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", mode='markers', marker={'sizemode': 'area', 'sizeref': sizeref, 'sizemin': 3, }).update_layout(hoverlabel=dict(font_size=12, )))),

                html.Div(id="scatter_container", children=[]),


                ]
            ),

        html.Br(),

        html.Div(id="second_row",
            children=[html.Div(dash_table.DataTable(
                id='main_datatable',
                columns= [{"name": colName, "id": colName} for colName in df.columns],
                data=df.to_dict('records'),
                sort_action="native",
                row_selectable="multi",
                selected_columns=[],
                selected_rows=[],
                style_as_list_view=True,
                style_data={'if': {'row_index': 'odd'}, 'backgroundColor': "#F5F5F5", },
                style_data_conditional=[],
                style_cell={'minWidth': "10px", "width": "50px", "maxWidth": "80px", "fontSize": "12px", "font-family": "sans-serif", "text_align": "center", "border": "1px",}, )),
                      ]
            ),

        html.Br(),

        ]
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
    dff = df if len(derived_virtual_data) == 0 else pd.DataFrame(derived_virtual_data)
    dff["marker_line_width"] = 1
    dff["marker_line_color"] = "white"
    dff.loc[derived_virtual_selected_rows, "marker_line_width"] = 4
    dff.loc[derived_virtual_selected_rows, "marker_line_color"] = "black"

    fig = go.Figure()
    sizeref = 0.05
    marker_sizemin_ = 4
    for category_name, group in dff.groupby("category"):
        fig.add_trace(go.Scatter(name=category_name, x=group["logFDR"].tolist(), y=group["effectSize"].tolist(), ids=group["term"].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_color=group["color"].iloc[0], marker_size=group["FG_count"], marker_sizemin=marker_sizemin_, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group["marker_line_width"], marker_line_color=group["marker_line_color"], customdata=[list(ele) for ele in zip(group["term"], group["description"], group["FG_count"])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
    fig.update_layout(xaxis={'title': 'log(FDR)'}, yaxis={'title': 'effect size'})
    scatter_plot_fig = dcc.Graph(id='scatter_plot', figure=fig)

    if selected_rows is not None:
        selected_term_list = dff.loc[selected_rows, "term"].tolist()
        style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
        return style_data_conditional_extension + style_data_conditional_basic, scatter_plot_fig
    else:
        return style_data_conditional_basic, scatter_plot_fig
#####
# # {'points': [
# # {'curveNumber': 0, 'pointNumber': 0, 'pointIndex': 0, 'x': 3, 'y': 0.053, 'marker.size': 370, 'customdata': ['GOCC:0043229', 'Intracellular organelle', 370, 3, 0.053, 'TM']},
# # {'curveNumber': 1, 'pointNumber': 2, 'pointIndex': 2, 'x': 1, 'y': 0.025, 'marker.size': 410, 'customdata': ['KW-0156', 'Chromatin regulator', 410, 1, 0.025, 'GOCC']},
# # {'curveNumber': 2, 'pointNumber': 2, 'pointIndex': 2, 'x': 2, 'y': 0.025, 'marker.size': 500, 'customdata': ['KW-0010', 'Activator', 500, 2, 0.025, 'UPK']}],
# # 'lassoPoints': {'x': [2.1099478252905777, 2.253195791626579, 2.659835179935227, 3.0017819382856814, 3.2051016324400057, 3.357591403055749, 3.431525837293685, 3.445388543713298, 2.0729806081716093, 1.837314599038188, 1.684824828422445, 1.6201321984642507, 1.2273555165752152, 1.1719046908967632, 1.000931311721536, 0.8946505625045028, 0.8715460518051478, 0.8715460518051478], 'y': [0.002742805205836079, 0.002742805205836079, 0.00967401011810582, 0.020682394390534233, 0.031690778662962646, 0.044330034679454525, 0.06267734180016855, 0.06716223909634308, 0.06675452116032722, 0.05493070101586707, 0.044330034679454525, 0.042699162935391055, 0.04188372706335933, 0.041476009127343456, 0.03699111183116892, 0.02924447104686744, 0.02272098407061357, 0.01701293296639143]}}


###### working solution start
# @app.callback(Output(component_id="main_datatable", component_property="style_data_conditional"),
#               Input(component_id="main_datatable", component_property="selected_rows"))
# def highlight_dataTableRows_on_select_in_dataTable_v1(selected_rows):
#     if selected_rows is not None:
#         selected_term_list = df.loc[selected_rows, "term"].tolist()
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
#         return style_data_conditional_extension + style_data_conditional_basic
#     return style_data_conditional_basic
#
# @app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
#                Output(component_id="main_datatable", component_property="selected_rows")],
#               [Input(component_id="scatter_plot", component_property="selectedData")])
# def highlight_and_select_dataTableRows_on_select_inScatter(selectedData):
#     selected_term_list, selected_rows = [], []
#     if selectedData is not None:
#         print(selectedData)
#         for point in selectedData["points"]:
#             selected_term_list.append(point["customdata"][0])
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}='+"{}".format(term)},
#                             'backgroundColor': 'gold'} for term in selected_term_list]
#         selected_rows = df[df["term"].isin(selected_term_list)].index.tolist()
#         print("selected_term_list: {}".format(selected_term_list))
#         print(selected_rows)
#         return style_data_conditional_extension + style_data_conditional_basic, selected_rows
#     return style_data_conditional_basic, selected_rows
###### working solution stop

# @app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
#                Output(component_id='scatter-container', component_property='children'),],
#               Input(component_id="main_datatable", component_property="selected_rows"))
# def highlight_dataTableRows_and_PointsInPlot_on_select_in_dataTable_v1(selected_rows):
#     if selected_rows is not None:
#         selected_term_list = df.loc[selected_rows, "term"].tolist()
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
#         return style_data_conditional_extension + style_data_conditional_basic
#     return style_data_conditional_basic




# @app.callback(Output(component_id="main_datatable", component_property="style_data_conditional"),
#               Input(component_id="main_datatable", component_property="selected_rows"))
# def highlight_dataTableRows_on_select_in_dataTable_v1(selected_rows):
#     if selected_rows is not None:
#         selected_term_list = df.loc[selected_rows, "term"].tolist()
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
#         return style_data_conditional_extension + style_data_conditional_basic
#     return style_data_conditional_basic

# @app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
#                Output(component_id="main_datatable", component_property="selected_rows")],
#               [Input(component_id="scatter_plot", component_property="selectedData"),
#                Input(component_id="main_datatable", component_property="selected_rows")])
# def combi(selectedData):
#     selected_term_list, selected_rows = [], []
#     if selectedData is not None:
#         print(selectedData)
#         for point in selectedData["points"]:
#             selected_term_list.append(point["customdata"][0])
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}='+"{}".format(term)},
#                             'backgroundColor': 'gold'} for term in selected_term_list]
#         selected_rows = df[df["term"].isin(selected_term_list)].index.tolist()
#         print("selected_term_list: {}".format(selected_term_list))
#         print(selected_rows)
#         return style_data_conditional_extension + style_data_conditional_basic, selected_rows
#     return style_data_conditional_basic, selected_rows


if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)