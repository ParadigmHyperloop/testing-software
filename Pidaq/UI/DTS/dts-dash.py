import dash
import dash_bootstrap_components as dbc

from dts_dash.app import app
from dts_dash import control_callbacks
from dts_dash.control_layout import control_layout
from dts_dash.manual_layout import manual_layout


tabs = dbc.Tabs(
    [
        dbc.Tab(control_layout, label="Controls", tabClassName="hov-pointer"),
        dbc.Tab(manual_layout, label="Manual", tabClassName="hov-pointer")
    ] 
)

app.layout = tabs

if __name__ == "__main__":
    app.run_server(debug=False)
    