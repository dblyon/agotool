import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
# import dash_table_experiments as dt
import dash_table
import json
import pandas as pd
import numpy as np
import plotly

app = dash.Dash()

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]

print(DF_GAPMINDER.head())

app.layout = html.Div([
    html.H3('Customized Selection Attributes'),
    dash_table.DataTable(
        id='datatable-gapminder',
        # rows=DF_GAPMINDER.to_dict('records'),
        data=DF_GAPMINDER.to_dict('records'),
        # optional - sets the order of columns
        # columns=sorted(DF_GAPMINDER.columns),
        columns=[{"name": colName, "id": colName} for colName in DF_GAPMINDER.columns],
        # row_selectable=True,
        # filterable=True,
        # sortable=True,
        # selected_row_indices=[0, 5, 10],
        selected_rows=[0, 5, 10],
    ),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")

@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    return {
        'data': [{
            'x': dff['gdpPercap'],
            'y': dff['lifeExp'],
            'text': dff['country'],
            'mode': 'markers',
            'textposition': 'top center',
            'selectedpoints': selected_row_indices,
            'marker': {
                'size': 10
            },

            'selected': {
                'marker': {
                    'line': {
                        'width': 1,
                        'color': 'rgb(0, 41, 124)'
                    },
                    'color': 'rgba(0, 41, 124, 0.7)',
                }
            },

            'unselected': {
                'marker': {
                    'line': {
                        'width': 0.5,
                        'color': 'rgb(0, 116, 217)'
                    },
                    'color': 'rgba(0, 116, 217, 0.5)',
                },

            }

        }],
        'layout': {'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}}
    }

    # return fig


# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)