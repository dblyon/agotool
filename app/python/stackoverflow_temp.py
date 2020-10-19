### https://stackoverflow.com/questions/62516573/update-dash-table-by-selecting-points-on-scatter-plot?answertab=active#tab-top

# IMPORT SECTION
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from math import ceil
from matplotlib.cm import Set3


# INPUT DATA
n = 7
d_min = 0.2
d_max = 0.8
d_step = 0.1
N_min = 2000
N_max = 8000
N_step = 1000
D = 40
h = 20
dataframe_file = "data_stackoverflow.txt"


# COLOR AND FONT DEFINITION
grey = '#e0e1f5'
black = '#212121'
scatter_colors = ['#' + ''.join(['{:02x}'.format(int(255*Set3(i)[j])) for j in range(3)]) for i in range(n)]
fontsize = 18
fontfamily = 'Arial, sans-serif'


# READ CSV DATA
df = pd.read_csv(dataframe_file, delimiter=r"\s+")


# CREATE DATA FOR DASH DATATABLE
df_scatter_colors = ceil(len(df) / len(scatter_colors)) * scatter_colors
df_scatter_colors = df_scatter_colors[:len(df)]
df.insert(loc = 0, column = 'COLOR', value = df_scatter_colors)

headers = [{"name": i, "id": i} for i in df.columns]

table = df.to_dict('records')


# CREATE DATA AND LAYOUT FOR THE SCATTERPLOT
x_jitter = 0.05 * N_step * np.random.randn(len(df))
y_jitter = 0.05 * d_step * 1000 * np.random.randn(len(df))
data = [go.Scatter(x = df['NUMBER'] + x_jitter,
                   y = df['DIAMETER'] + y_jitter,
                   text = df['PRODUCT'],
                   mode = 'markers',
                   hoverinfo = 'skip',
                   showlegend = False,
                   marker_color = 'rgba(0, 0, 0, 0)',
                   marker = {'size': 25,
                             'line': {'color': df['COLOR'],
                                      'width': 8}})]

layout = go.Layout(plot_bgcolor = black,
                   hovermode = 'x unified',
                   uirevision = 'value')

figure = go.Figure(data = data, layout = layout)

# DASHBOARD LAYOUT
app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = html.Div(id = 'general_div',
    children=[
        html.Div(id = 'first_row',
             children=[
                 dcc.Graph(id = 'main_graph', figure = figure, style = {'height': 800, 'width': 1400})
                 ], className = 'row'),
        html.Div(id = 'second_row',
            children=[
                dash_table.DataTable(id = 'main_table', columns = headers, data = table, style_table={'margin-left': '3vw', 'margin-top': '3vw'}, style_cell = {'font-family': fontfamily, 'fontSize': fontsize}, style_header = {'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'})
                  ], className = 'row')
              ]
)

def update_table_style(selectedData):
    table_style_conditions = [{'if': {'row_index': 'odd'},
                               'backgroundColor': 'rgb(240, 240, 240)'}]

    if selectedData != None:
        points_selected = []
        for point in selectedData['points']:
            points_selected.append(point['pointIndex'])
        selected_styles = [{'if': {'row_index': i},
                            'backgroundColor': 'pink'} for i in points_selected]
        table_style_conditions.extend(selected_styles)

    table_style_conditions.extend([{'if': {'row_index': i, 'column_id': 'COLOR'},
                                    'background-color': df.iloc[i]['COLOR'],
                                    'color': df.iloc[i]['COLOR']} for i in range(df.shape[0])])

    return table_style_conditions

# CALLBACK DEFINITION
@app.callback(Output('main_table', 'style_data_conditional'),
              [Input('main_graph', 'selectedData')])
def display_selected_data(selectedData):
    table_style_conditions = update_table_style(selectedData)
    return table_style_conditions


if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port="5922")
