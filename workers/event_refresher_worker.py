import asyncio
import datetime

import aiohttp
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from db.models import BaseEvent
from db.models import Event
from workers.models import eventList


engine = create_async_engine(
    settings.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

APPROVED_SELL_MODE = [
    "online",
]


def create_update_base_events_query(base_events):
    return (
        insert(BaseEvent)
        .values(
            [
                dict(
                    base_event_id=base_event.base_event_id,
                    sell_mode=base_event.sell_mode,
                    title=base_event.title,
                )
                for base_event in base_events
                if base_event.sell_mode in APPROVED_SELL_MODE
            ]
        )
        .on_conflict_do_update(
            index_elements=[BaseEvent.base_event_id],
            set_=dict(last_updated_dt=datetime.datetime.now()),
        )
    )


def create_update_events_query(event, base_event_id):
    return (
        insert(Event)
        .values(
            [
                dict(
                    event_start_date=event.event_start_date,
                    event_end_date=event.event_end_date,
                    event_id=event.event_id,
                    base_event_id=base_event_id,
                    zones=[zone.dict() for zone in event.zones],
                )
            ]
        )
        .on_conflict_do_update(
            index_elements=[Event.base_event_id, Event.event_id],
            set_=dict(
                last_updated_dt=datetime.datetime.now(),
                is_active=True,
                event_start_date=event.event_start_date,
                event_end_date=event.event_end_date,
            ),
        )
    )


async def get_event_list_from_provider() -> eventList:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.PROVIDER_URL, ssl=False) as resp:
            xml_from_resp = await resp.text()
            return eventList.from_xml(xml_from_resp)


async def event_refresher_worker():
    event_list = await get_event_list_from_provider()

    async with async_session() as db_session:
        async with db_session.begin():
            update_base_events_query = create_update_base_events_query(
                event_list.output.base_events
            )
            await db_session.execute(update_base_events_query)
            for base_event in event_list.output.base_events:
                if base_event.sell_mode not in APPROVED_SELL_MODE:
                    continue
                base_event_id = base_event.base_event_id
                for event in base_event.events:
                    update_events_query = create_update_events_query(
                        event, base_event_id
                    )
                    await db_session.execute(update_events_query)


def main():
    asyncio.run(event_refresher_worker())


scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=settings.EVENT_REFRESHER_MINUTES_PERIOD)
scheduler.start()
