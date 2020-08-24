""" layout.py

Wind Tunnel GUI dash layout
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq


# CONSTANTS
MAX_AIRSPEED = 100
MIN_AIRSPEED = 0

MAX_INCREMENTS = 100
MIN_INCREMENTS = 100

MIN_GROUNDSPEED = 0
MAX_GROUNDSPEED = 200

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

update_profile_btn = dbc.Button("UPDATE PROFILE",
                                 color="primary",
                                 className="mr-1",
                                 id="update-profile-btn")

init_stepper_btn = dbc.Button("INITIALIZE STEPPER",
                                 color="warning",
                                 className="mr-1",
                                 id="init-stepper-btn")

start_btn = dbc.Button("START",
                        color="success",
                        className="mr-1",
                        id="start-btn",
                        style={"height":"100%",
                               "width":"100%"})

estop_btn = dbc.Button("ESTOP",
                        color="danger",
                        className="mr-1",
                        id="estop-btn",
                        style={"height":"100%",
                                "width":"100%"})


### Input Groups ###
air_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Air Speed", className="input-label"),
        dbc.Input(id="air-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Air velocity",
                  min=MIN_AIRSPEED,
                  max=MAX_AIRSPEED),
        dbc.InputGroupAddon("units", addon_type="append")
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
        dbc.InputGroupAddon("units", addon_type="append")
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
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

# Ground speed input disabled for the time being
ground_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Ground Speed", className="input-label"),
        dbc.Input(id="ground-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Treadmill speed",
                  min=MIN_GROUNDSPEED,
                  max=MAX_GROUNDSPEED,
                  disabled=True),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

height_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Height", className="input-label"),
        dbc.Input(id="height-input",
                  bs_size="md",
                  type="number",
                  placeholder="Stepper height",
                  min=MIN_HEIGHT,
                  max=MAX_HEIGHT),
        dbc.InputGroupAddon("units", addon_type="append")
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
        dbc.InputGroupAddon("units", addon_type="append")
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
        dbc.InputGroupAddon("units", addon_type="append")
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
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

# TODO Center vertically
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
            air_speed_input,
            increments_input,
            timestep_input,
            ground_speed_input   
    ])
])

stepper_config_card = dbc.Card([
    dbc.CardHeader("STEPPER CONFIG"),
    dbc.CardBody([
          height_input,
          surface_area_input,
          fra_input,
          aoa_input  
    ])
])

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
], className="custom-card")

update_profile_card = dbc.Card([
    update_profile_btn
], 
body=True)

init_stepper_card = dbc.Card([
    init_stepper_btn
], 
body=True)

start_card = dbc.Card([
    start_btn
], 
body=True,
style={"height":"150px"})

estop_card = dbc.Card([
    estop_btn
], 
body=True,
style={"height":"150px"})

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

### DISPLAY CARDS ###
kin_viscosity_card = dbc.Card(
            dbc.CardBody([
                html.P("Kinematic Viscosity", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="kin-viscosity-value"),
                html.P("cSt", className="numerical-display-units", style={"display":"inline-block"})
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
                html.P("cP", className="numerical-display-units", style={"display":"inline-block"})
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
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist1_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 1", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist1-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist2_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 2", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist2-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist2_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 2", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist2-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist3_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 3", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist3-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist3_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 3", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist3-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

exp_dist4_card = dbc.Card(
            dbc.CardBody([
                html.P("Expected Distance 4", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="exp-dist4-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
            ])
        )

act_dist4_card = dbc.Card(
            dbc.CardBody([
                html.P("Actual Distance 4", className="numerical-display-title"),
                html.P("0", className="numerical-display-value", style={"display":"inline-block"}, id="act-dist4-value"),
                html.P("mm", className="numerical-display-units", style={"display":"inline-block"}),
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
    
    # System Communication Row
    dbc.Row([
        dbc.Col([
            system_communication_card
        ]),
        dbc.Col([
            environmental_config_card 
       ]) 
    ],
    className="pad-top pad-bot pad-left pad-right"),
        
    # Inverter and Stepper Config Row
    dbc.Row([
       dbc.Col([
         stepper_config_card  
       ]),
       
       dbc.Col([
           inverter_config_card
       ])
    ],
    className="pad-bot pad-left pad-right"),
    
    # Update Profile / Initialize Stepper Button Row
    dbc.Row([
        dbc.Col([
            update_profile_card
        ]),
        dbc.Col([
            init_stepper_card
        ])
    ],
    className="pad-left pad-right pad-bot"),
    
    # Start and ESTOP Button Row
    dbc.Row([
        dbc.Col([
            start_card
        ]),
        dbc.Col([
            estop_card
        ])
    ],
    className="pad-left pad-right pad-bot"),
    

    # Calculated Values Collapse
    dbc.Row([
        dbc.Col([
            calculated_values_collapse
        ])
    ],
    className="pad-left pad-right pad-bot"),
    
    # Distance Sensor Readings Collapse
    dbc.Row([
        dbc.Col([
            distance_values_collapse
        ])
    ],
    className="pad-left pad-right pad-bot")
])

control_gui = html.Div([
    dbc.Row([
        # CONTROLS
        dbc.Col([
            control_gui_column
        ]),
    ])    
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