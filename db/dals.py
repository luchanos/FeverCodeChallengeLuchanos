import datetime

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Zone


class EventDAL:
    """Data Access Layer for operating event info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_events_by_time_range(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ):
        query = select(Zone).where(
            and_(Zone.start_date <= start_date, Zone.end_date >= end_date)
        )
        res = await self.db_session.execute(query)
        event_row = res.fetchall()
        if event_row is not None:
            return event_row[0]
