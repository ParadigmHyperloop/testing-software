import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from wt_dash.app import app
from wt_dash import callbacks
from wt_dash import layout


tabs = dbc.Tabs(
    [
        dbc.Tab(layout.control_gui, label="Controls", tabClassName="hov-pointer"),
        dbc.Tab(layout.manual, label="Manual", tabClassName="hov-pointer")
    ] 
)

app.layout = tabs

if __name__ == "__main__":
    app.run_server(debug=False)