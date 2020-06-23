import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd


# Alerts
exceed_60s_alert = dbc.Alert("WARNING: Current test length exceeds 60s!",
                             id="exceed-60s-alert",
                             is_open=False,
                             duration=5000,
                             color="warning",
                             dismissable=True)

no_name_alert = dbc.Alert("ERROR: Please select a test profile name!",
                             id="no-name-alert",
                             is_open=False,
                             duration=5000,
                             color="warning",
                             dismissable=True)

# Buttons
add_command_btn = dbc.Button("Add Command",
                            color="primary",
                            className="mr-1",
                            id="add-command-btn",
                            style={"text-align": "center"})

start_test_btn =  dbc.Button("Start",
                            color="success",
                            className="mr-1",
                            id="test-start-btn",
                            style={"width": "100%"})

stop_test_btn =  dbc.Button("Stop",
                            color="danger",
                            className="mr-1 pad-top",
                            id="test-stop-btn",
                            style={"width": "100%"})

estop_btn =  dbc.Button("ESTOP", 
                        color="danger",
                        className="mr-1",
                        style={"height": "100%",
                                "width": "100%"})

clear_last_btn =  dbc.Button("Clear Last",
                            color="primary",
                            className="mr-1",
                            style={"width": "100%"},
                            id="clear-last-btn")

clear_all_btn =  dbc.Button("Clear All",
                            color="primary",
                            className="mr-1 pad-top",
                            style={"width": "100%"},
                            id="clear-all-btn")

update_title_btn = dbc.Button("Update",
                              color="primary",
                              className="mr-1",
                              id="update-title-btn")

torque_toggle_btn = dbc.Button("Torque",
                                color="primary",
                                className="mr-1",
                                id="torque-toggle-btn")

rpm_toggle_btn = dbc.Button("RPM",
                            color="primary",
                            className="mr-1",
                            id="rpm-toggle-btn")

export_profile_btn = dbc.Button("Export Profile",
                                color="primary",
                                className="mr-1 align-right",
                                id="export-profile-btn")

load_profiles_btn = dbc.Button("Load Profile",
                                color="primary",
                                className="mr-1 align-right",
                                id="load-profile-btn")

# Modals
start_warn_modal = dbc.Modal([
                            dbc.ModalHeader("WARNING !!!"),
                            dbc.ModalBody("Attempting to start test with the chosen profile:\n"
                                           "Would you like to continue?"),
                            dbc.ModalFooter([
                                html.Div([
                                    dbc.Button("Abort", 
                                            id="abort-start-btn",
                                            color="danger",
                                            className="ml-auto pad-right-s"),
                                    dbc.Button("Start",
                                            id="submit-start-btn",
                                            color="success",
                                            className="ml-auto")
                                ])
                            ])
                        ],
                        id="start-confirm-dialog")

# Tables
df = pd.DataFrame(columns=["Type", "Step Duration(ms)", "Value"])

timestep_readout_table = dash_table.DataTable(
    id="timestep-readout-tbl",
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    editable=False,
    style_as_list_view=True,
    style_table={"height": 300, "overflowY": "auto"}
)

# Main Control GUI Bootstrap Layout
control_layout = html.Div([
    
    # Modals
    start_warn_modal,
    
    # Alerts
    exceed_60s_alert,
    no_name_alert,
    
    # Bootstrap Layout
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(placeholder="Enter test title here",
                        type="text",
                        id="test-title-input"),
                
                dbc.InputGroupAddon(update_title_btn,
                                    addon_type="append")  
            ])
        ],
        width={"size": 4, "offset": 4}),
    ],
    className='pad-bot pad-top'),
    
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(["DTS", html.Br(), "CONTROLS"],
                            style={"text-align": "center"})
                ])
            ], className="custom-card")
        ],
        className="pad-left"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    html.H3("Test Title Here", 
                            id="test-title-header",
                            style={"text-align": "center"},
                            className="vertical-center")
                )
            ],
            className="custom-card")
        ],
        width={"size": 4,}),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("RPM", 
                            id="rpm-torque-display",
                            style={"text-align": "center"},
                            className="vertical-center")    
                ])
            ],
            className="custom-card")
        ],
        className="pad-right")
    ],
    className="pad-bot pad-top"),


    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("RPM / Torque", style={"text-align": "center"}),
                dbc.CardBody([
                    dbc.ButtonGroup(
                        [torque_toggle_btn, rpm_toggle_btn],
                        style={ "text-align": "center", "margin-left": "15%", "width": "70%"},
                        className="vertical-center")
                ])
            ],
            className="custom-card center-content")
        ], 
        className="pad-left"),
        
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Step Duration (ms)", style={"text-align": "center"}),
                dbc.CardBody([
                    dbc.Input(
                        id="step-duration-input",
                        type="number",
                        min=0,
                        max=10000, 
                        step=100,
                        value=0,
                        style={"text-align": "center", "width": "80%", "margin": "auto"},
                        className="vertical-center")
                ])
            ],
            className="custom-card")
        ),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("RPM / Torque Value", style={"text-align": "center"}),
                dbc.CardBody([
                    dbc.InputGroup([
                        dbc.Input(type="number",
                                  id="rpm-torque-value",
                                  step=100,
                                  min=0,
                                  max=10000,
                                  value=0),
                        dbc.InputGroupAddon(add_command_btn,
                                            addon_type="append")
                    ])
                ])
            ],
            className="custom-card"),  
        ],
        className="pad-right"),
    ]),
    
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    "Time-Step Readout of Test Torque/RPM Input Profile",
                    export_profile_btn
                    ], 
                    style={"text-align": "center"}),
                
                dbc.CardBody([
                    timestep_readout_table
                ])
            ], 
            className="pad-right pad-left")
        ])
    ],
    className="pad-top pad-bot"),
    
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                       start_test_btn
                    ]),
                    html.Div([
                       stop_test_btn
                    ])
                ])
            ], className="custom-card")
        ],
        className="pad-left"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                   estop_btn
                ])
            ], className="custom-card")
        ],
        width={"size": 5}),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                       clear_last_btn
                    ]),
                    html.Div([
                       clear_all_btn
                    ])
                ])
            ], className="custom-card")
        ],
        className="pad-right")
    ],
    className="pad-top pad-bot"),
    
    # Empty divs to store output of callbacks with no output
    html.Div("", id="dump-abort-start"),
    html.Div("", id="dump-export-profile"),
    html.Div("", id="dump-start-clicked")
])
