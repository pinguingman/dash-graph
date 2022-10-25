from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from database import Base


class TradeTool(Base):
    __tablename__ = "trade_tool"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)


class TradeData(Base):
    __tablename__ = "trade_data"

    id = Column(Integer, primary_key=True)
    tool_id = Column(Integer, ForeignKey("trade_tool.id", ondelete="CASCADE"))
    value = Column(Float)
    created_at = Column(DateTime)
