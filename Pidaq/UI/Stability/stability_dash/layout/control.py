import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

# Modals
start_warn_modal = dbc.Modal([
                            dbc.ModalHeader("WARNING !!!"),
                            dbc.ModalBody("Attempting to start test with the chosen profile:\n"
                                           "Would you like to continue?"),
                            dbc.ModalFooter([
                                html.Div([
                                    dbc.Button("Abort", 
                                            id="abort-start",
                                            color="danger",
                                            className="ml-auto pad-right-s"),
                                    dbc.Button("Start",
                                            id="submit-start",
                                            color="success",
                                            className="ml-auto")
                                ])
                            ])
                        ],
                        id="start-confirm-dialog")

# Main Control GUI Bootstrap Layout
control_layout = html.Div([
    
    
dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("RUNTIME", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("TIMESTEP", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("DISPLACEMENT STEP", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("VELOCITY STEP", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("ACCELERATION STEP", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("PROFILE NAME", addon_type="prepend"),
                dbc.Input(),
            ],
        )],
            body=True)  
        ],
        width={"size": 6, "offset": 3})
    ]),

dbc.Row([
    dbc.ButtonGroup(
        [
            dbc.Button("SAVE PROFILE"),
            dbc.DropdownMenu(
                [dbc.DropdownMenuItem("PROFILE 1"), dbc.DropdownMenuItem("PROFILE 2")],
                label="LOAD PROFILE",
                group=True,
            ),
        ]
    )
    ]),

])