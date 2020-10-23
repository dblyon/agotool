import json
import pandas as pd

import dash
import dash_html_components as html
from dash_table import DataTable
from dash.dependencies import Input, Output

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
data = df.to_dict("rows")
for row in data:
    row['id'] = 'id:' + row['State'].lower()
print(data)

app = dash.Dash(__name__)
app.layout = html.Div([
    DataTable(
        id='main',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=data,
        row_selectable='multi',
        row_deletable=True,
        # pagination_settings={'page_size': 3, 'current_page': 0}
    ),
    html.Hr(),
    DataTable(
        id='out',
        columns=[{'name': 'prop', 'id': 'prop'}, {'name': 'val', 'id': 'val'}],
        data=[],
        style_cell_conditional=[
            {'if': {'column_id': 'val'}, 'textAlign': 'left'}
        ]
    )
])


props = [
    'active_cell', 'start_cell', 'end_cell', 'selected_cells',
    'selected_rows', 'selected_row_ids',
    'derived_viewport_indices', 'derived_viewport_row_ids',
    'derived_virtual_indices', 'derived_virtual_row_ids',
    'derived_viewport_selected_rows', 'derived_viewport_selected_row_ids',
    'derived_virtual_selected_rows', 'derived_virtual_selected_row_ids'
]


@app.callback(Output('out', 'data'), [Input('main', v) for v in props])
def show_props(*args):
    return [
        {'prop': prop, 'val': json.dumps(val)}
        for prop, val in zip(props, args)
    ]

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)
