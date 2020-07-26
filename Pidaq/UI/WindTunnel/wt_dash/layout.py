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


### Input Groups ###
air_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Air Speed", addon_type="prepend"),
        dbc.Input(id="air-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Enter air velocity",
                  min=MIN_AIRSPEED,
                  max=MAX_AIRSPEED),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

increments_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Increments", addon_type="prepend"),
        dbc.Input(id="increments-input",
                  bs_size="md",
                  type="number",
                  placeholder="Number of test increments",
                  min=MIN_INCREMENTS,
                  max=MAX_INCREMENTS)
    ],
    className="mb-3"
)

timestep_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Timestep", addon_type="prepend"),
        dbc.Input(id="timestep-input",
                  bs_size="md",
                  type="number",
                  placeholder="Duration to remain on each step",
                  min=MIN_TIMESTEP,
                  max=MAX_TIMESTEP),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

# TODO Disable
ground_speed_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Ground Speed", addon_type="prepend"),
        dbc.Input(id="ground-speed-input",
                  bs_size="md",
                  type="number",
                  placeholder="Treadmill speed",
                  min=MIN_GROUNDSPEED,
                  max=MAX_GROUNDSPEED),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

height_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Height", addon_type="prepend"),
        dbc.Input(id="height-input",
                  bs_size="md",
                  type="number",
                  placeholder="stepper height",
                  min=MIN_HEIGHT,
                  max=MAX_HEIGHT),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

height_input1 = dbc.InputGroup(
    [
        html.H2("Height"),
        dbc.Input(id="height-input",
                  bs_size="md",
                  type="number",
                  placeholder="stepper height",
                  min=MIN_HEIGHT,
                  max=MAX_HEIGHT),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

surface_area_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Surface Area", addon_type="prepend"),
        dbc.Input(id="surface-area-input",
                  bs_size="md",
                  type="number",
                  placeholder="surface area",
                  min=MIN_SA,
                  max=MAX_SA),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

fra_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Frontal Ref. Area", addon_type="prepend"),
        dbc.Input(id="fra-input",
                  bs_size="md",
                  type="number",
                  placeholder="frontal reference area",
                  min=MIN_FRA,
                  max=MAX_FRA),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

aoa_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Angle of Attack", addon_type="prepend"),
        dbc.Input(id="aoa-input",
                  bs_size="md",
                  type="number",
                  placeholder="Angle of attack",
                  min=MIN_AOA,
                  max=MAX_AOA),
        dbc.InputGroupAddon("units", addon_type="append")
    ],
    className="mb-3"
)

temp_input = dbc.InputGroup(
    [
        dbc.InputGroupAddon("TEMP", addon_type="prepend", id="current-temp"),
        dbc.Input(id="temp-input",
                  bs_size="md",
                  type="number",
                  placeholder="temperature",
                  min=MIN_TEMP,
                  max=MAX_TEMP),
        dbc.InputGroupAddon(
            [
                load_temp_btn
            ],
            addon_type="append")
    ],
    className="mb-3"
)


#### DISPLAYS ###
kinematic_viscosity_display = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Kinematic Viscosity", addon_type="prepend"),
        dbc.Input(
                value="TEST",
                id="kinematic-viscosity-input",
                disabled=True,
            ),
    ],
    className="mb-3"
)


### Cards ###
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
    dbc.CardHeader("ENVIRONMENT CONFIG"),
    dbc.CardBody([
        # TODO - Rolling average temp
        temp_input
    ])
])

system_communication_card = dbc.Card([
    dbc.CardHeader("SYSTEM COMMUNICATION"),
    dbc.CardBody([
        html.Div(
        daq.Indicator(
            id="sense-indicator",
            label="SENSE",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#00FF00",
            height=30,
        ),style={"width":"33.33%","display": "inline-block"}),
        
        html.Div(
        daq.Indicator(
            id="stepper-indicator",
            label="STEPPER",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#00FF00",
            height=30,
        ),style={"width":"33.33%","display": "inline-block"}),
        
        html.Div(
        daq.Indicator(
            id="blower-indicator",
            label="BLOWER",
            labelPosition="bottom",
            value=False, # Default false for indicators
            color="#00FF00",
            height=30,
        ),style={"width":"33.33%","display": "inline-block"}), 
    ])
])

calculated_values_card = html.Div([
    # TODO - Place a plus badge, title, and open collapse button
    
])

### Dropdown Content ###
row1 = dbc.Row([
    dbc.Col(kinematic_viscosity_display),
    dbc.Col(),
    dbc.Col()
])

row2 = dbc.Row([
    dbc.Col(),
    dbc.Col(),
    dbc.Col()
    
])

row3 = dbc.Row([
    dbc.Col(),
    dbc.Col(),
    dbc.Col()
])

calculated_values_collapse = html.Div([
    dbc.Card([
        dbc.CardHeader([
            "CONSTANTS BLAH",
            collapse_constants_btn
        ])  
    ]),
        
    dbc.Collapse([
        dbc.Card([
            "TEST CARD BODY"
            
        ], 
        body=True)
    ], is_open=True)
   
])

# Primary GUI Tab Layout
control_gui = html.Div([
    
    dbc.Row([
        dbc.Col([
            system_communication_card
        ])    
    ],
    className="pad-top pad-bot pad-left pad-right"),
    

    dbc.Row([
       dbc.Col([
          environmental_config_card 
       ]) 
    ],
    className="pad-bot pad-left pad-right"),
    
    
    dbc.Row([
       dbc.Col([
         stepper_config_card  
       ]),
       
       dbc.Col([
           inverter_config_card
       ])
   ],
    className="pad-bot pad-left pad-right"),
    
    
    dbc.Row([
        dbc.Col([
            calculated_values_collapse
        ])
    ],
    className="pad-top pad-left pad-right")
    
    
])

manual = html.Div("MANUAL HERE")