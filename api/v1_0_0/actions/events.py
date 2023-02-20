import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1_0_0.models import EventSummary
from db.dals import EventDAL


async def get_events_by_date_range(
    session: AsyncSession, start_date: datetime.datetime, end_date: datetime.datetime
) -> list[EventSummary]:
    async with session.begin():
        user_dal = EventDAL(session)
        events = await user_dal.get_events_by_time_range(
            start_date=start_date, end_date=end_date
        )
        result = []
        for event in events:
            event = dict(event)
            result.append(
                EventSummary(
                    **{
                        "id": event["id"],
                        "title": event["title"],
                        "start_date": event["event_start_date"].date(),
                        "start_time": event["event_start_date"].time(),
                        "end_date": event["event_end_date"].date(),
                        "end_time": event["event_end_date"].time(),
                        "max_price": event["max_price"],
                        "min_price": event["min_price"],
                    }
                )
            )
        return result
