import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

df = pd.DataFrame.from_dict(
    {'term': {0: 'GOCC:0043229', 1: 'GOCC:0098588', 2: 'GOCC:0005730', 3: 'GO:0005730', 4: 'GO:0005783', 5: 'GO:0031410', 6: 'KW-0732', 7: 'KW-0156', 8: 'KW-0010'},
    'description': {0: 'Intracellular organelle', 1: 'Bounding membrane of organelle', 2: 'Nucleolus', 3: 'nucleolus', 4: 'endoplasmic reticulum', 5: 'cytoplasmic vesicle', 6: 'Signal', 7: 'Chromatin regulator', 8: 'Activator'},
     'FG_count': {0: 370, 1: 92, 2: 126, 3: 500, 4: 63, 5: 23, 6: 9, 7: 410, 8: 31},
     'logFDR': {0: 2.6, 1: 4, 2: 5, 3: 2, 4: 7, 5: 8, 6: 5, 7: 1, 8: 6},
     'effectSize': {0: 0.053, 1: -0.049, 2: 0.046, 3: 0.025, 4: -0.040, 5: -0.027, 6: -0.024, 7: 0.025, 8: 0.047},
     'category': {0: 'TM', 1: 'TM', 2: 'TM', 3: 'GOCC', 4: 'GOCC', 5: 'GOCC', 6: 'UPK', 7: 'UPK', 8: 'UPK'}})

style_data_conditional_basic = [{"if": {"state": "selected"}, "backgroundColor": "gold", "border": "inherit !important", "text_align": "inherit !important", }] + [{"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }]

app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
marker_size_min_ = 4
sizeref = 0.05

data_table_ex = dash_table.DataTable(
                id='main_datatable',
                columns=[{"name": colName, "id": colName} for colName in df.columns],
                data=df.to_dict('records'),
                sort_action="native",
                row_selectable="multi",
                selected_columns=[],
                selected_rows=[],
                style_as_list_view=True,
                style_data={'if': {'row_index': 'odd'}, 'backgroundColor': "#F5F5F5", },
                style_data_conditional=[],
                style_cell={'minWidth': "10px", "width": "50px", "maxWidth": "80px", "fontSize": "12px", "font-family": "sans-serif", "text_align": "center", "border": "1px",},)

def create_scatter_plot_graph(df):
    fig = go.Figure()
    for category_name, group in df.groupby("category"):
        fig.add_trace(go.Scatter(name=category_name, x=group["logFDR"].tolist(), y=group["effectSize"].tolist(), ids=group["term"].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_size=group["FG_count"], marker_sizemin=marker_size_min_, marker_sizemode="area", marker_sizeref=sizeref, customdata=[list(ele) for ele in zip(group["term"], group["description"], group["FG_count"])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
    fig.update_layout(xaxis={'title': 'log(FDR)'}, yaxis={'title': 'effect size'})
    scatter_plot_graph = dcc.Graph(id='scatter_plot', figure=fig)
    return scatter_plot_graph

scatter_plot_graph = create_scatter_plot_graph(df)

app.layout = html.Div(id='general_div', className="container-fluid",
    children=[
        dbc.Row([
            dbc.Col(
                html.Div(id="scatter_container", children=[scatter_plot_graph]), xs={"size": 12}, sm={"size": 12}, md={"size": 10}, lg={"size": 8}, ),
        ], justify="center", ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div(data_table_ex), xs={"size": 12}, sm={"size": 12}, md={"size": 10}, lg={"size": 10},),
        ], justify="center",),
        html.Br(),
        ])

############ Select either "Option 1" or "Option 2" and comment out the other ############
### Option 1 START
@app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
               Output(component_id="main_datatable", component_property="selected_rows")],
              [Input(component_id="scatter_plot", component_property="selectedData")])
def on_selectInScatter_highlight_and_select_dataTableRows(selectedData):
    selected_term_list, selected_rows = [], []
    if selectedData is not None:
        for point in selectedData["points"]:
            selected_term_list.append(point["customdata"][0])
        style_data_conditional_extension = [{'if': {'filter_query': '{term}='+"{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
        selected_rows = df[df["term"].isin(selected_term_list)].index.tolist()
        return style_data_conditional_extension + style_data_conditional_basic, selected_rows
    return style_data_conditional_basic, selected_rows
### Option 1 STOP
###############################
### Option 2 START
# @app.callback([Output(component_id="main_datatable", component_property="style_data_conditional"),
#                Output(component_id="scatter_container", component_property="children")],
#               [Input(component_id="main_datatable", component_property="selected_rows"),
#                Input(component_id="main_datatable", component_property="derived_virtual_data"),
#                Input(component_id="main_datatable", component_property='derived_virtual_selected_rows')])
# def on_selectInDataTable_highlight_dataTableRows_and_pointsInScatterPlot(selected_rows, derived_virtual_data, derived_virtual_selected_rows):
#     dff = df if len(derived_virtual_data) == 0 else pd.DataFrame(derived_virtual_data)
#     dff["marker_line_width"] = 1
#     dff["marker_line_color"] = "white"
#     dff.loc[derived_virtual_selected_rows, "marker_line_width"] = 4
#     dff.loc[derived_virtual_selected_rows, "marker_line_color"] = "black"
#     fig = go.Figure()
#     for category_name, group in dff.groupby("category"):
#         fig.add_trace(go.Scatter(name=category_name, x=group["logFDR"].tolist(), y=group["effectSize"].tolist(), ids=group["term"].tolist(), legendgroup=category_name, mode="markers", marker_symbol="circle", marker_size=group["FG_count"], marker_sizemin=marker_size_min_, marker_sizemode="area", marker_sizeref=sizeref, marker_line_width=group["marker_line_width"], marker_line_color=group["marker_line_color"], customdata=[list(ele) for ele in zip(group["term"], group["description"], group["FG_count"])], hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", ))
#     fig.update_layout(xaxis={'title': 'log(FDR)'}, yaxis={'title': 'effect size'})
#     scatter_plot_fig = dcc.Graph(id='scatter_plot', figure=fig)
#
#     if selected_rows is not None:
#         selected_term_list = dff.loc[selected_rows, "term"].tolist()
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
#         return style_data_conditional_extension + style_data_conditional_basic, scatter_plot_fig
#     else:
#         return style_data_conditional_basic, scatter_plot_fig
### Option 2 STOP
####################################
############ Select one of the two options above and comment out the other ############

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)



### Option 1 v0 START
# @app.callback(Output(component_id="main_datatable", component_property="style_data_conditional"),
#               Input(component_id="main_datatable", component_property="selected_rows"))
# def on_selectInDataTable_highlight_dataTableRows(selected_rows):
#     if selected_rows is not None:
#         selected_term_list = df.loc[selected_rows, "term"].tolist()
#         style_data_conditional_extension = [{'if': {'filter_query': '{term}=' + "{}".format(term)}, 'backgroundColor': 'gold'} for term in selected_term_list]
#         return style_data_conditional_extension + style_data_conditional_basic
#     return style_data_conditional_basic
### Option 1 v0 STOP
####################################


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
