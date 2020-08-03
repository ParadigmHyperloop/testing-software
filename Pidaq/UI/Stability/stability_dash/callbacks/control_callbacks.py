import json
import os

import dash
from dash.dependencies import Input, Output, State
from dash.dash import no_update 

from stability_dash.app import app
from stability_dash.layout.control import control_layout


@app.callback(
    Output("dump-save-profile", "children"),
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
