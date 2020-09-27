import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

# Main Control GUI Bootstrap Layout
control_layout = html.Div([

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody(
                html.H3("PARAMETERS",
                    style={"text-align": "center"})
            )
        ])
    ],
    width={"size": 4, "offset": 4})
]),


dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("RUNTIME", style={"width":"180px"}),
                dbc.Input(id="runtime"),
            ])
        ], 
        body=True)  
    ], 
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("TIMESTEP", style={"width":"180px"}),
                dbc.Input(id="timestep"),
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("DISPLACEMENT STEP", style={"width":"180px"}),
                dbc.Input(id="displacement-step"),
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("VELOCITY STEP", style={"width":"180px"}),
                dbc.Input(id="velocity-step"),
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("ACCELERATION STEP", style={"width":"180px"}),
                dbc.Input(id="acceleration-step"),
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.InputGroup([
                dbc.InputGroupAddon("PROFILE NAME", style={"width":"180px"}),
                dbc.Input(id="profile-name"),
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.ButtonGroup([
                dbc.Button("SAVE PROFILE", id="save-profile", style={"width":"100%"}),
                dbc.Button("DELETE PROFILE", id="delete-profile", style={"width":"100%"}),
                dcc.Dropdown(
                    id = "load-profile",
                    options = [],
                    placeholder="LOAD PROFILE",
                    style={"width":"100%"})
            ])
        ],
        body=True)  
    ],
    width={"size": 4, "offset": 4})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.Button("RECORD", id="record", color="success", style={"height":"100%","width":"100%"})
        ], style={"height":"100%","width":"100%"})  
    ],
    width={"size": 1, "offset": 4}),
    dbc.Col([
        dbc.Card([
            dbc.Button("TARE", color="warning"),
            dbc.Button("CLEAR DATA", color="warning")
        ])  
    ],
    width={"size": 2, "offset": 0}),
    dbc.Col([
        dbc.Card([
            dbc.Button("STOP", id="stop", color="danger", style={"height":"100%","width":"100%"})
        ], style={"height":"100%","width":"100%"})  
    ],
    width={"size": 1, "offset": 0})
]),

dbc.Row([
    dbc.Col([
        dbc.Card([dbc.Button("EMERGENCY STOP", color="danger", size="lg", block = True, style={"height":"100%","width":"100%"} )])  
    ],
    width={"size": 4, "offset": 4})
]),

html.Div("", id="save-load-connection"),
html.Div("", id="delete-load-connection"),

])