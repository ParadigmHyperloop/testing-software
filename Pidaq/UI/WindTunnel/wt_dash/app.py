import dash
import dash_auth
import dash_bootstrap_components as dbc

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'paradigm': 'password'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.config['SECRET_KEY'] = 'password'
app.config.suppress_callback_exceptions=True
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)