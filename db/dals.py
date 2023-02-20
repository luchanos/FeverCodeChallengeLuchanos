import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event
from db.raw_sql_query import GET_EVENTS_BY_TIME_RANGE_QUERY


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
        # todo luchanos тут я записываю всё сразу
        await self.db_session.flush()

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
