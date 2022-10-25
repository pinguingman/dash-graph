from dash import dcc
from dash import html


def init_layout(app):
    app.layout = html.Div(
        [
            dcc.Dropdown(id="selector", multi=True),
            dcc.Graph(id="timeseries-component"),
            dcc.Input(
                id="input-on-submit",
                type="number",
                max=100,
                min=1,
                required=True,
            ),
            html.Button("Add", id="submit-add-val", n_clicks=0),
            html.Div(id="submit-add-label"),
            html.Button("Remove all", id="submit-remove-val", n_clicks=0),
            html.Div(id="submit-remove-label"),
            dcc.Interval(id="interval-component", interval=10000),
        ]
    )
