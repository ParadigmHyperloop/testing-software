import dash

app = dash.Dash(__name__)
server = app.server
server.config['SECRET_KEY'] = 'password'
app.config.suppress_callback_exceptions=True

