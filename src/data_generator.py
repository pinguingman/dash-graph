from datetime import datetime
from random import random

from apscheduler.schedulers.background import BlockingScheduler
from sqlalchemy import desc
from sqlalchemy.sql.functions import coalesce

from database import Session
from models import TradeTool, TradeData


def generate_trade_data():
    with Session.begin() as session:
        trade_data = (
            session.query(
                coalesce(TradeData.value, 0).label("value"), TradeTool.id
            )
            .select_from(TradeTool)
            .distinct(TradeTool.id)
            .join(TradeData, TradeTool.id == TradeData.tool_id, isouter=True)
            .order_by(TradeTool.id, desc(TradeData.created_at))
            .all()
        )

        updated_values = []
        datetime_now = datetime.now().replace(microsecond=0)
        for trade_data_row in trade_data:
            updated_values.append(
                TradeData(
                    tool_id=trade_data_row.id,
                    value=trade_data_row.value + generate_movement(),
                    created_at=datetime_now,
                )
            )
        session.bulk_save_objects(updated_values)
        session.commit()


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


scheduler = BlockingScheduler()

# this job runs generation every second
scheduler.add_job(generate_trade_data, "cron")

if __name__ == "__main__":
    scheduler.start()
