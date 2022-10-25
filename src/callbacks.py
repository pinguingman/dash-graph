import dash
import plotly.express as px
from dash import Output, Input, State, ctx
from sqlalchemy import func, cast, Integer

from database import Session
from models import TradeTool
from utils import get_df, get_tools


def add_tools(value, *args):
    if value is None or ctx.triggered_id is None:
        return "Enter a number of tools and press submit to add them"

    value = int(value)
    with Session.begin() as session:
        max_tool_number = session.query(
            func.max(cast(func.replace(TradeTool.name, "ticker_", ""), Integer))
        ).scalar()

        start = 0 if max_tool_number is None else max_tool_number + 1
        new_trade_tools = []
        for tool_number in range(start, start + value):
            new_trade_tools.append(TradeTool(name=f"ticker_{tool_number}"))
        session.bulk_save_objects(new_trade_tools)
        tool_count = session.query(TradeTool.id).count()

    return f"You added {value} new tools, total count is {tool_count}"


def remove_tools(n_clicks):
    if not n_clicks:
        return "Press to delete all data"

    with Session.begin() as session:
        session.query(TradeTool).delete()
    return f"Data deleted"


def update_live_graph(n_intervals, tools):
    figure = px.line(
        get_df(tools=tools),
        x="created_at",
        y="value",
        color="name",
        template="plotly_dark",
    )
    figure["layout"]["uirevision"] = "some-constant"

    options = get_tools()
    options = [{"label": option, "value": option} for option in options]
    return figure, options


def register_callbacks():
    dash.callback(
        Output("submit-add-label", "children"),
        State("input-on-submit", "value"),
        Input("submit-add-val", "n_clicks"),
    )(add_tools)

    dash.callback(
        Output("submit-remove-label", "children"),
        Input("submit-remove-val", "n_clicks"),
    )(remove_tools)

    dash.callback(
        [
            Output("timeseries-component", "figure"),
            Output("selector", "options"),
        ],
        [
            Input("interval-component", "n_intervals"),
            Input("selector", "value"),
        ],
    )(update_live_graph)
