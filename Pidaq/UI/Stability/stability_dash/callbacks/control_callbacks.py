import json
import os

import dash
from dash.dependencies import Input, Output, State
from dash.dash import no_update 

from stability_dash.app import app
from stability_dash.layout.control import control_layout


@app.callback(
    Output("save-load-connection", "value"),
    [Input("save-profile", "n_clicks")],
    [State("profile-name", "value"),
     State("runtime", "value"),
     State("timestep", "value"),
     State("displacement-step", "value"),
     State("velocity-step", "value"),
     State("acceleration-step", "value")]
)
def save_profile(save_clicks, profile_name, runtime, timestep, displacement, velocity, acceleration):
    
    if not save_clicks:
        raise dash.exceptions.PreventUpdate

    folder_path = os.getcwd()
    path_to_file = os.path.join(folder_path, "profiles.json")

    if not os.path.isfile(path_to_file):
        profiles_json = {}
        profiles_json['profiles'] = []
        profiles_json['profiles'].append({
        'name': profile_name,
        'runtime': runtime,
        'timestep': timestep,
        'displacement-step' : displacement,
        'velocity-step' : velocity,
        'acceleration-step' : acceleration
        })

        with open(path_to_file, 'w') as profiles_file:
            json.dump(profiles_json, profiles_file, indent=4)

    else:
        with open(path_to_file, 'r') as profiles_file:
            profiles_json = json.load(profiles_file)
            for profile in profiles_json['profiles']:
                if profile['name'] == profile_name:
                    profile['runtime'] = runtime
                    profile['timestep'] = timestep
                    profile['displacement-step'] = displacement
                    profile['velocity-step'] = velocity
                    profile['acceleration-step'] = acceleration
                    with open(path_to_file, 'w') as profiles_file:
                        json.dump(profiles_json, profiles_file, indent=4)
                    break
            else:
                profiles_json['profiles'].append({
                'name': profile_name,
                'runtime': runtime,
                'timestep': timestep,
                'displacement-step' : displacement,
                'velocity-step' : velocity,
                'acceleration-step' : acceleration
                }) 
                with open(path_to_file, 'w') as profiles_file:
                    json.dump(profiles_json, profiles_file, indent=4)

    return profile_name

@app.callback(
    [Output("load-profile", "options"),
    Output("load-profile", "value")],
    [Input("save-load-connection", "value"),
    Input("delete-load-connection", "value"),
    Input("save-profile", "n_clicks")]
)
def update_load_profile(profile_name, empty, save_clicks):
    folder_path = os.getcwd()
    path_to_file = os.path.join(folder_path, "profiles.json")
    with open(path_to_file, 'r') as profiles_file:
        profiles_json = json.load(profiles_file)
        profile_labels = []
        options=[]
        for profile in profiles_json['profiles']:
            profile_labels.append(profile['name'])
        for i in profile_labels:
            options.append({'label': i, 'value': i})
        return options, profile_name

@app.callback(
    [Output("profile-name", "value"),
    Output("runtime", "value"),
    Output("timestep", "value"),
    Output("displacement-step", "value"),
    Output("velocity-step", "value"),
    Output("acceleration-step", "value")],
    [Input("load-profile", "value")]
)
def load_profile(load_profile_value):
    if not load_profile_value:
        return '', '', '', '', '', ''

    folder_path = os.getcwd()
    path_to_file = os.path.join(folder_path, "profiles.json")
    with open(path_to_file, 'r') as profiles_file:
        profiles_json = json.load(profiles_file)
        for profile in profiles_json['profiles']:
            if profile['name'] == load_profile_value:
                profile_name = profile['name']
                runtime = profile['runtime']
                timestep = profile['timestep']
                displacement = profile['displacement-step']
                velocity = profile['velocity-step']
                acceleration = profile['acceleration-step']

    return profile_name, runtime, timestep, displacement, velocity, acceleration

@app.callback(
    Output("delete-load-connection", "value"),
    [Input("delete-profile", "n_clicks")],
    [State("load-profile", "value")]

)
def delete_profile(delete_clicks, load_profile_value ):
    if not delete_clicks:
        raise dash.exceptions.PreventUpdate

    folder_path = os.getcwd()
    path_to_file = os.path.join(folder_path, "profiles.json")
    with open(path_to_file, 'r') as profiles_file:
        profiles_json = json.load(profiles_file)
        new_profiles_json = {}
        new_profiles_json['profiles'] = [x for x in profiles_json['profiles'] if x['name'] != load_profile_value]
        with open(path_to_file, 'w') as profiles_file:
            json.dump(new_profiles_json, profiles_file, indent=4)
        return load_profile_value