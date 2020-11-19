import dash
from server import server

app = dash.Dash(name="app_dash_1", sharing=True, server=server, url_base_pathname="/app_dash_1")

