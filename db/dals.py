import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event
from db.raw_sql_queries import GET_EVENTS_BY_TIME_RANGE_QUERY


class EventDAL:
    """Data Access Layer for operating event info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_events_by_time_range(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ):
        res = await self.db_session.execute(
            GET_EVENTS_BY_TIME_RANGE_QUERY,
            {"start_date": start_date, "end_date": end_date},
        )
        fetched_result = res.fetchall()
        return fetched_result

    async def deactivate_events_older_than_limit(self, limit_days: int):
        query = (
            update(Event)
            .where(
                Event.last_updated_dt
                <= datetime.datetime.now() - datetime.timedelta(days=limit_days)
            )
            .values({"is_active": False})
        )
        await self.db_session.execute(query)
