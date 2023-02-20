import asyncio

from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from db.dals import EventDAL


class EventDeactivator:
    def __init__(self, days_limit: int, event_dal: EventDAL):
        self.days_limit = days_limit
        self.event_dal = event_dal

    async def __call__(self):
        await self.event_dal.deactivate_events_older_than_limit(self.days_limit)


async def event_deactivator_func():
    engine = create_async_engine(
        settings.REAL_DATABASE_URL,
        future=True,
        echo=True,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as db_session:
        async with db_session.begin():
            event_dal = EventDAL(db_session=db_session)
            event_deactivator = EventDeactivator(
                event_dal=event_dal,
                days_limit=settings.EVENT_DEACTIVATOR_DAYS_VALID_PERIOD,
            )
            await event_deactivator()


def main():
    asyncio.run(event_deactivator_func())


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=settings.EVENT_DEACTIVATOR_MINUTES_PERIOD)
scheduler.start()
