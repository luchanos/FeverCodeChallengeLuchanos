import datetime

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event


class EventDAL:
    """Data Access Layer for operating event info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_events_by_time_range(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ):
        query = select(Event).where(
            and_(Event.event_start_date >= start_date, Event.event_end_date <= end_date)
        )
        res = await self.db_session.execute(query)
        events_row = res.fetchall()
        if events_row is not None:
            return [event[0] for event in events_row]

    async def write_events_to_database(self, events_list):
        for event in events_list:
            new_event = Event(
                base_event_id=event["base_event_id"],
                title=event["title"],
                price=event["price"],
                event_start_date=event["event_start_date"],
                event_end_date=event["event_start_date"],
                zone_id=event["zone_id"],
            )
            self.db_session.add(new_event)
        await self.db_session.flush()
