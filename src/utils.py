import pandas as pd
from sqlalchemy import select

from database import engine, Session
from models import TradeTool, TradeData


def get_df(tools=None, since=None):
    query = select(TradeTool.name, TradeData.value, TradeData.created_at).join(
        TradeData, TradeTool.id == TradeData.tool_id
    ).order_by(TradeData.created_at)
    if tools:
        query = query.filter(TradeTool.name.in_(tools))
    if since:
        query = query.filter(TradeData.created_at > since)
    df = pd.read_sql(query, engine)

    return df


def get_tools():
    with Session.begin() as session:
        result = session.query(TradeTool.name).all()
    return [row.name for row in result]
