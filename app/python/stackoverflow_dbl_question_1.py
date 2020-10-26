import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

df = pd.DataFrame.from_dict(
    {'term': {0: 'GOCC:0043229', 1: 'GOCC:0098588', 2: 'GOCC:0005730', 3: 'GO:0005730', 4: 'GO:0005783', 5: 'GO:0031410', 6: 'KW-0732', 7: 'KW-0156', 8: 'KW-0010'},
    'description': {0: 'Intracellular organelle', 1: 'Bounding membrane of organelle', 2: 'Nucleolus', 3: 'nucleolus', 4: 'endoplasmic reticulum', 5: 'cytoplasmic vesicle', 6: 'Signal', 7: 'Chromatin regulator', 8: 'Activator'},
     'FG_count': {0: 370, 1: 92, 2: 126, 3: 31, 4: 63, 5: 23, 6: 9, 7: 410, 8: 500},
     'logFDR': {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 5, 7: 1, 8: 2},
     'effectSize': {0: 0.053, 1: -0.049, 2: 0.046, 3: 0.047, 4: -0.040, 5: -0.027, 6: -0.024, 7: 0.025, 8: 0.025},
     'category': {0: 'TM', 1: 'TM', 2: 'TM', 3: 'GOCC', 4: 'GOCC', 5: 'UPK', 6: 'UPK', 7: 'GOCC', 8: 'UPK'}})

df["id"] = df["term"]
df = df.set_index("id", drop=False)

app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

max_marker_size = 40
sizeref = 2.0 * max(df["FG_count"]) / (max_marker_size ** 2)
app.layout = html.Div(id='general_div',
    children=[
        html.Div(id='first_row',
            children=[
                    html.Div(dcc.Graph(id='scatter_plot',
                     figure=px.scatter(data_frame=df, x="logFDR", y="effectSize", color="category", size="FG_count", hover_data={"term": True, "description": True, "FG_count": True, "logFDR": False, "effectSize": False, "category": False }, custom_data=["term", "description", "FG_count"]).update_traces(hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Size: %{customdata[2]}<extra></extra>", mode='markers', marker={'sizemode': 'area', 'sizeref': sizeref, 'sizemin': 3, }).update_layout(hoverlabel=dict(font_size=12, )))),
                ]),
        html.Br(),
        html.Div(id="second_row",
            children=[html.Div(dash_table.DataTable(id='main_datatable', columns= [{"name": colName, "id": colName} for colName in df.columns], data=df.to_dict('records'), sort_action="native", row_selectable="multi", selected_columns=[], selected_rows=[], style_as_list_view=True,  style_cell={'minWidth': "10px", "width": "50px", "maxWidth": "80px", "fontSize": "12px", "font-family": "sans-serif", "text_align": "center", "border": "1px",}, style_data={'if': {'row_index': 'odd'}, 'backgroundColor': "#F5F5F5",}, )),
                      ]),
        html.Br(),
        ])

def update_table_style(selectedData):
    table_style_conditions = [{"if": {"state": "selected"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }] + [{"if": {"state": "active"}, "backgroundColor": "inherit !important", "border": "inherit !important", "text_align": "inherit !important", }]
    selected_term_list = []
    if selectedData is not None:
        for point in selectedData["points"]:
            selected_term_list.append(point["customdata"][0])
        print("selected_term_list: {}".format(selected_term_list))
        selected_styles = [{'if': {'filter_query': '{id}='+"{}".format(term)},
                            'backgroundColor': 'gold'} for term in selected_term_list]
        return selected_styles + table_style_conditions
    return table_style_conditions

@app.callback(Output('main_datatable', 'style_data_conditional'),
              [Input('scatter_plot', 'selectedData')])
def display_selected_data(selectedData):
    table_style_conditions = update_table_style(selectedData)
    return table_style_conditions






if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)
