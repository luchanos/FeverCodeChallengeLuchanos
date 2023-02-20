import datetime

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BaseEvent
from db.models import Event
from db.models import Zone


class EventDAL:
    """Data Access Layer for operating event info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_events_by_time_range(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ) -> list[Row]:

        subquery = (
            select(
                Event.id,
                Zone.price,
                Event.event_start_date,
                Event.event_end_date,
                Event.base_event_id,
            )
            .join(Event, Event.base_event_id == Zone.base_event_id)
            .where(
                and_(
                    Event.event_start_date >= start_date,
                    Event.event_end_date <= end_date,
                )
            )
            .subquery()
        )

        query = (
            select(
                BaseEvent.title,
                subquery.c.id,
                func.max(subquery.c.price),
                func.min(subquery.c.price),
                subquery.c.event_start_date,
                subquery.c.event_end_date,
            )
            .join(subquery, subquery.c.base_event_id == BaseEvent.base_event_id)
            .group_by(
                subquery.c.id,
                BaseEvent.title,
                subquery.c.event_end_date,
                subquery.c.event_start_date,
            )
        )
        res = await self.db_session.execute(query)
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
