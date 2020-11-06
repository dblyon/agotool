import igraph as ig
# import plotly.plotly as py
from plotly.graph_objs import *

import os, sys, json
import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', 300) # in order to prevent 50 character cutoff of to_html export / ellipsis
# from plotly_tools import data_bars
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

fn_netscience = os.path.join(variables.STATIC_DIR_FLASK, "plotly/netscience.gml")

G = ig.Graph.Read_GML(fn_netscience)
labels = list(G.vs['label'])
N = len(labels)
# N = 10
E = [e.tuple for e in G.es] # list of edges
layt = G.layout('kk') #kamada-kawai layout
# type(layt)

### Nodes
Xn = [layt[k][0] for k in range(N)]
Yn = [layt[k][1] for k in range(N)]
### Edges
Xe = []
Ye = []
for e in E:
    Xe += [layt[e[0]][0],layt[e[1]][0], None]
    Ye += [layt[e[0]][1],layt[e[1]][1], None]

trace1 = go.Scatter(x=Xe,
               y=Ye,
               mode='lines',
               line= dict(color='rgb(210,210,210)', width=1),
               hoverinfo='none'
               )
trace2 = go.Scatter(x=Xn,
               y=Yn,
               mode='markers',
               name='ntw',
               marker=dict(symbol='circle-dot',
                                        size=5,
                                        color='#6959CD',
                                        line=dict(color='rgb(50,50,50)', width=0.5)
                                        ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

width=800
height=800
layout=go.Layout(title= "Coauthorship network of scientists working on network theory and experiment"+\
              "<br> Data source: <a href='https://networkdata.ics.uci.edu/data.php?id=11'> [1]</a>",
    font= dict(size=12),
    showlegend=False,
    autosize=False,
    width=width,
    height=height,
    xaxis=layout.XAxis(axis),
    yaxis=layout.YAxis(axis),
    margin=layout.Margin(
        l=40,
        r=40,
        b=85,
        t=100,
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text='This igraph.Graph has the Kamada-Kawai layout',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ]
    )

data = [trace1, trace2]
network_fig = go.Figure(data=data, layout=layout)
network_fig_graph = dcc.Graph(id='network_plot', figure=network_fig)

# py.iplot(fig, filename='Coautorship-network-igraph')

app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(network_fig_graph)

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=5922)