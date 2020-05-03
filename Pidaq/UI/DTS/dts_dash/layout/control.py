import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html

# Buttons
add_command_btn = dbc.Button("Add Command",
                            color="primary",
                            className="mr-1",
                            id="add-command",
                            style={"text-align": "center"})

start_test_btn =  dbc.Button(
                            "Start",
                            color="success",
                            className="mr-1",
                            id="test-start",
                            style={"width": "100%"})

stop_test_btn =  dbc.Button("Stop",
                            color="danger",
                            className="mr-1 pad-top",
                            id="test-stop",
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
                            id="clear-last")

clear_all_btn =  dbc.Button("Clear All",
                            color="primary",
                            className="mr-1 pad-top",
                            style={"width": "100%"},
                            id="clear-all")

update_title_btn = dbc.Button("Update",
                              color="primary",
                              className="mr-1",
                              id="update-title")

torque_toggle_button = dbc.Button("Torque",
                                  color="primary",
                                  className="mr-1",
                                  id="torque-toggle")

rpm_toggle_button = dbc.Button("RPM",
                                  color="primary",
                                  className="mr-1",
                                  id="rpm-toggle")

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
    dcc.ConfirmDialog(
    id='confirm-start',
    message='WARNING: Are you sure that you want to continue?'),
    
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
                dbc.CardBody(
                    html.H2("Current Test Title Here", 
                            id="test_title_header",
                            style={"text-align": "center"})
                )
            ],
            className="custom-card")
        ],
        width={"size": 6, "offset":3})
    ],
    className="pad-bot pad-top"),
    
 
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("RPM / Torque", style={"text-align": "center"}),
                dbc.CardBody([
                    dbc.ButtonGroup(
                        [torque_toggle_button, rpm_toggle_button],
                        style={"justify-content": "center", "text-align": "center", "margin-left": "15%", "width": "70%"},# TODO This is just gross
                        className="vertical-center")
                ])
            ],
            className="custom-card")
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
                        max=10000, #TODO MAX STEP DURATION CONFIG
                        step=10,
                        style={"text-align": "center", "width": "80%", "margin": "auto"},
                        className="auto-margins vertical-center")
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
                                  max=10000, # TODO MAX RPM/TORQUE VALUE
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
                dbc.CardHeader("Time-Step Readout of Test Torque/RPM Input Profile", 
                               style={"text-align": "center"}),
                dbc.CardBody([
                    "Body"
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
            ], style={"height": "100%"})
        ],
        className="pad-left"),
        
        dbc.Col([
            dbc.Card([
                #dbc.CardHeader("ESTOP"),
                dbc.CardBody([
                   estop_btn
                ])
            ], style={"height": "100%"})
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
            ], style={"height": "100%"})
        ],
        className="pad-right")
    ],
    className="pad-top pad-bot"),
    
    # Modals
    start_warn_modal,
    
    # Empty, invisible div 
    html.Div("", id="dump"),
])