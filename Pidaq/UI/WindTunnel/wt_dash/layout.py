""" layout.py

Wind Tunnel GUI dash layout
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

ground_speed_active = False

# MIN/MAX CONSTANTS
MIN_AIRSPEED = 0
MAX_AIRSPEED = 100

MIN_INCREMENTS = 1
MAX_INCREMENTS = 100

MIN_GROUNDSPEED = 0
MAX_GROUNDSPEED = 100

MIN_HEIGHT = 0
MAX_HEIGHT = 100

MIN_SA = 0
MAX_SA = 100

MIN_FRA = 0
MAX_FRA = 100

MIN_AOA = 0
MAX_AOA = 90

MIN_TEMP = 0
MAX_TEMP = 40

MIN_TIMESTEP = 0
MAX_TIMESTEP = 100

#### Buttons ###
update_profile_btn = dbc.Button("SAVE",
                                color="primary",
                                className="mr-1",
                                id="update-profile-btn",
                                style={"text-align": "center"})

load_temp_btn = dbc.Button("LOAD",
                            color="primary",
                            className="mr-1",
                            id="load-temp-btn")

collapse_constants_btn = dbc.Button("+",
                                    color="primary",
                                    className="mr-1 align-right",
                                    id="collapse-constants-btn")

distance_sensor_btn = dbc.Button("+",
                                 color="primary",
                                 className="mr-1 align-right",
                                 id="distance-sensor-btn")

abort_btn = dbc.Button("Abort",
                        color="danger",
                        className="mr-1 align-right",
                        id="collapse-constants-btn")

init_stepper_btn = dbc.Button("INITIALIZE STEPPER",
                                 color="warning",
                                 className="mr-1",
                                 id="init-stepper-btn",
                                 style={"width":"100%",
                                        "height":"100%"})

lock_stepper_btn = dbc.Button("LOCK STEPPERS",
                                 color="success",
                                 className="mr-1",
                                 id="lock-stepper-btn",
                                 style={"width":"100%",
                                        "height":"100%"})

start_btn = dbc.Button("START",
                        color="secondary",
                        className="mr-1",
                        id="start-btn",
                        disabled=True,
                        style={"height":"100%",
                               "width":"100%"})

estop_btn = dbc.Button("STOP",
                        color="danger",
                        className="mr-1",
                        id="estop-btn",
                        style={"height":"100%",
                                "width":"100%"})


### Inputs ###
test_name_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Test Name", className="input-label"),
        dbc.Input(id="test-name-input",
                  bs_size="md",
                  type="text"),
        dbc.InputGroupAddon("n/a", className="input-units")
    ],
    className="mb-3"
)

air_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Air Speed", className="input-label"),
        dbc.Input(id="air-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Air velocity",
                  min=MIN_AIRSPEED,
                  max=MAX_AIRSPEED),
        dbc.InputGroupAddon("m/s", className="input-units")
    ],
    className="mb-3"
)

increments_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Increments", className="input-label"),
        dbc.Input(id="increments-input",
                  bs_size="md",
                  type="number",
                  placeholder="# of test increments",
                  min=MIN_INCREMENTS,
                  max=MAX_INCREMENTS),
        dbc.InputGroupAddon("n/a", className="input-units")
    ],
    className="mb-3"
)

timestep_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Timestep", className="input-label"),
        dbc.Input(id="timestep-input",
                  bs_size="md",
                  type="number",
                  placeholder="Step duration",
                  min=MIN_TIMESTEP,
                  max=MAX_TIMESTEP),
        dbc.InputGroupAddon("s", className="input-units")
    ],
    className="mb-3"
)

#TODO Disable ground speed input
ground_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Ground Speed", className="input-label"),
        dbc.Input(id="ground-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Treadmill speed",
                  min=MIN_GROUNDSPEED,
                  max=MAX_GROUNDSPEED,
                  disabled=False),
        dbc.InputGroupAddon("m/s", className="input-units")
    ],
    className="mb-3"
)

stepper_height_input = dbc.InputGroup(
    [
       dbc.InputGroupAddon("Height", className="input-label"),
        dbc.Input(id="height-input",
                  bs_size="md",
                  type="number",
                  placeholder="Stepper Height",
                  min=MIN_HEIGHT,
                  max=MAX_HEIGHT),
        dbc.InputGroupAddon(f"m", className="input-units")
    ],
    className="mb-3"
)

surface_area_input = dbc.InputGroup(
    [
       dbc.InputGroupAddon("SA", className="input-label"),
        dbc.Input(id="surface-area-input",
                  bs_size="md",
                  type="number",
                  placeholder="Surface area",
                  min=MIN_SA,
                  max=MAX_SA),
        dbc.InputGroupAddon(f"m\N{SUPERSCRIPT TWO}", className="input-units")
    ],
    className="mb-3"
)

fra_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("FRA", className="input-label"),
        dbc.Input(id="fra-input",
                  bs_size="md",
                  type="number",
                  placeholder="Frontal ref. area",
                  min=MIN_FRA,
                  max=MAX_FRA),
        dbc.InputGroupAddon(f"m\N{SUPERSCRIPT TWO}", className="input-units")
    ],
    className="mb-3"
)

aoa_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("AOA", className="input-label"),
        dbc.Input(id="aoa-input",
                  bs_size="md",
                  type="number",
                  placeholder="Angle of attack",
                  min=MIN_AOA,
                  max=MAX_AOA,
                  step=5),
        dbc.InputGroupAddon("°", className="input-units")
    ],
    className="mb-3"
)

temp_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("TEMP", addon_type="prepend", id="current-temp"),
        dbc.Input(id="temp-input",
                  type="number",
                  placeholder="temperature",
                  min=MIN_TEMP,
                  max=MAX_TEMP),
        dbc.InputGroupAddon(
            load_temp_btn,
            addon_type="append")
    ],
    className="mb-3",
    size="md",
    style={"width":"80%"}
)

### CARDS ###
inverter_config_card = dbc.Card([
    dbc.CardHeader("INVERTER CONFIG"),
    dbc.CardBody([
            test_name_input,
            air_speed_input,
            ground_speed_input, 
            increments_input,
            timestep_input,
    ])
], className="custom-card")

stepper_config_card = dbc.Card([
    dbc.CardHeader("STEPPER CONFIG"),
    dbc.CardBody([
        stepper_height_input,
        surface_area_input,
        fra_input,
        aoa_input,    
    ])
], className="custom-card")

environmental_config_card = dbc.Card([
    dbc.CardBody([
        # TODO - Rolling average temp
        dbc.Row([
            dbc.Col([
                html.P("Current Temperature", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}),
                html.P("°C", className="numerical-display-units", style={"display":"inline-block"}),
            ], style={"text-align":"center"}),
            dbc.Col([
                html.P("Rolling Average", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}),
                html.P("°C", className="numerical-display-units", style={"display":"inline-block"}),
            ], style={"text-align":"center"})
        ]),
        dbc.Row([
            temp_input
        ], style={"justify-content":"center"})
    ])
], 
body=True,
className="custom-card")

system_communication_card = dbc.Card([
    dbc.CardHeader("SYSTEM COMMUNICATION"),
    dbc.CardBody([
        html.Div(
        daq.Indicator(
            id="sense-indicator",
            label="SENSE",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#808080",
            height=30,
        ),style={"width":"25%","display": "inline-block"}),
        
        html.Div(
        daq.Indicator(
            id="stepper-indicator",
            label="STEPPER",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#808080",
            height=30,
        ),style={"width":"25%","display": "inline-block"}),
        
        html.Div(
        daq.Indicator(
            id="blower-indicator",
            label="BLOWER",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#808080",
            height=30,
        ),style={"width":"25%","display": "inline-block"}), 
        
        html.Div(
        daq.Indicator(
            id="treadmill-indicator",
            label="TREADMILL",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#808080",
            height=30,
        ),style={"width":"25%","display": "inline-block"}), 
    ])
], className="custom-card")

state_indicator_card = dbc.Card([
                daq.Indicator(
                    id="state-1",
                    label="STEPPERS CONFIGURED",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),
                     
                daq.Indicator(
                    id="state-2",
                    label="STEPPERS INITIALIZED",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),
                
                daq.Indicator(
                    id="state-3",
                    label="STEPPERS LOCKED",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),
                                
                daq.Indicator(
                    id="state-4",
                    label="INVERTERS CONFIGURED",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),
                                                
                daq.Indicator(
                    id="state-5",
                    label="READY",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),  
                
                daq.Indicator(
                    id="state-6",
                    label="TEST ACTIVE",
                    labelPosition="bottom",
                    value=False, # Default false for indicators
                    color="#808080",
                    height=30,
                    className="pad-top indicator-label"
                ),   
            ],body=True, className="custom-card", style={"text-align":"center"})
    
### DISPLAY CARDS ###
kin_viscosity_card = dbc.Card(
            dbc.CardBody([
                html.P("Kinematic Viscosity", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="kin-viscosity-value"),
                html.P(f"m\N{SUPERSCRIPT TWO}/s*10\u207B\u2076", className="numerical-display-units", style={"display":"inline-block"})
            ])
        )

mach_number_card = dbc.Card(
            dbc.CardBody([
                html.P("Mach Number", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="mach-number-value"),
            ])
        )

reynolds_number_card = dbc.Card(
            dbc.CardBody([
                html.P("Reynolds Number", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="reynolds-number-value"),
            ])
        )

compressibility_card = dbc.Card(
            dbc.CardBody([
                html.P("Compressibility", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="compressibility-value"),
            ])
        )

airflow_nature_card = dbc.Card(
            dbc.CardBody([
                html.P("Nature of Airflow", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="airflow-nature-value"),
            ])
        )

dynamic_viscosity_card = dbc.Card(
            dbc.CardBody([
                html.P("Dynamic Viscosity", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="dynamic-viscosity-value"),
                html.P("Pa.s", className="numerical-display-units", style={"display":"inline-block"})
            ])
        )

drag_coeff_card = dbc.Card(
            dbc.CardBody([
                html.P("Drag Coefficient", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="drag-coeff-value"),
            ])
        )

lift_coeff_card = dbc.Card(
            dbc.CardBody([
                html.P("Lift Coefficient", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="lift-coeff-value"),
            ])
        )

lift_drag_ratio_card = dbc.Card(
            dbc.CardBody([
                html.P("Lift / Drag Ratio", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="lift-drag-ratio-value"),
            ])
        )

exp_dist1_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 1", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist1-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist1_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 1", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist1-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist2_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 2", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist2-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist2_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 2", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist2-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist3_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 3", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist3-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist3_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 3", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist3-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist4_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 4", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist4-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist4_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 4", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist4-value"),
                html.P("m", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

### Dropdowns ###

# Calculated Value Dropdown 
constant_cards_1 = dbc.CardGroup([
    kin_viscosity_card,
    mach_number_card,
    reynolds_number_card
], style={"width":"100%"})

constant_cards_2 = dbc.CardGroup([
    compressibility_card,
    airflow_nature_card,
    dynamic_viscosity_card
], style={"width":"100%"})

constant_cards_3 = dbc.CardGroup([
    drag_coeff_card,
    lift_coeff_card,
    lift_drag_ratio_card
], style={"width":"100%"})

constants_row1 = dbc.Row([
    constant_cards_1
])

constants_row2 = dbc.Row([
    constant_cards_2
])

constants_row3 = dbc.Row([
    constant_cards_3
])

calculated_values_collapse = html.Div([
    dbc.Card([
        dbc.CardHeader([
            "CALCULATED VALUES",
            collapse_constants_btn
        ])  
    ]),
        
    dbc.Collapse([
        dbc.Card([
            constants_row1,
            constants_row2,
            constants_row3,        
        ], 
        body=True)
    ], 
    is_open=False,
    id="calculated-values-collapse",
    style={"text-align":"left"})
])

# Distance Sensor Reading Dropdown
distance_cards_1 = dbc.CardGroup([
    exp_dist1_card,
    act_dist1_card
], style={"width":"100%"})

distance_cards_2 = dbc.CardGroup([
    exp_dist2_card,
    act_dist2_card
], style={"width":"100%"})

distance_cards_3 = dbc.CardGroup([
    exp_dist3_card,
    act_dist3_card
], style={"width":"100%"})

distance_cards_4 = dbc.CardGroup([
    exp_dist4_card,
    act_dist4_card
], style={"width":"100%"})

distance_row1 = dbc.Row([
    distance_cards_1
])

distance_row2 = dbc.Row([
    distance_cards_2
])

distance_row3 = dbc.Row([
    distance_cards_3
])

distance_row4 = dbc.Row([
    distance_cards_4
])

distance_values_collapse = html.Div([
    dbc.Card([
        dbc.CardHeader([
            "DISTANCE SENSOR READINGS",
            distance_sensor_btn
        ])  
    ]),
        
    dbc.Collapse([
        dbc.Card([
            distance_row1,
            distance_row2,
            distance_row3, 
            distance_row4       
        ], 
        body=True)
    ], 
    is_open=False,
    id="distance-values-collapse",
    style={"text-align":"left"}) 
])


# GUI Control Column 
control_gui_column = html.Div([
    
    # Stepper config Row
    dbc.Row([
       dbc.Col([
            stepper_config_card  
       ]),
       
       dbc.Col([
            dbc.Card([
                init_stepper_btn,    
            ], body=True, className="half-height-card"),
        
            dbc.Card([
                lock_stepper_btn,    
            ], body=True, className="half-height-card")
            
        ],)
    ],
    className="pad-bot pad-left"),
    
    # Distance Sensor Readings Collapse
    dbc.Row([
        dbc.Col([
            distance_values_collapse
        ])
    ],
    className="pad-left  pad-bot"),

    # Inverter config row
    dbc.Row([
        dbc.Col([
            inverter_config_card
        ]),
        
        dbc.Col([
            dbc.Card([
                start_btn
            ],
            className="half-height-card" ,
            body=True),
            
            dbc.Card([
                estop_btn
            ], 
            body=True,
            className="half-height-card")            
        ]) 
    ],  
    className="pad-bot pad-left"),
    
    # Calculated Values Collapse
    dbc.Row([
        dbc.Col([
            calculated_values_collapse
        ])
    ],
    className="pad-left pad-bot"),
    
])

control_gui = html.Div([
    
    # System Comunication Row
    dbc.Row([
        dbc.Col([
            system_communication_card
        ], width=5),
        
        dbc.Col([
            environmental_config_card    
       ], width=5)
    ],
    className="pad-top pad-bot pad-left"),
    
    dbc.Row([
        # Control Column
        dbc.Col([
            control_gui_column
        ],
        width=10),
        
        dbc.Col([
            state_indicator_card
        ], className="pad-right pad-bot"),
    ]),

    # Output Dumps
    html.Div(id="update-profile-dump")   ,
    
    # State Divs
    html.Div(id="1-InitialState"),
    html.Div(id="2-StepperInitReadyState"),
    html.Div(id="3-StepperInitState"),
    html.Div(id="4-StepperLockState"),
    html.Div(id="5-InverterConfigState"),
    html.Div(id="6-PrimedState"),
    html.Div(id="7-ActiveTestState"),
     
])

manual = dcc.Markdown(
    '''
    ### Hyperloop Ground Effect Wind Tunnel Control Software
    
    This is the Paradigm Hyperloop Ground Effect Wind Tunnel
    Control Software.
    
    **Authorized users only.**
    
    **Contacts**                                     
    * Colton Smith 
    * Daniel Burke
    * Rohan Seelan 
    '''
)