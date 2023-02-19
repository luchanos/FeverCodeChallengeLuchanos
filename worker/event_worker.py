import asyncio
import datetime
import pathlib

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from db.models import BaseEvent
from db.models import Event
from worker.models import eventList

# import aiohttp


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
    # todo если у нас что-то упадет по одному, то получится, что завалится все сразу
    return (
        insert(Event)
        .values(
            [
                dict(
                    event_start_date=event.event_start_date,
                    event_end_date=event.event_end_date,
                    event_id=event.event_id,
                    base_event_id=base_event_id,
                    zones=[x.dict() for x in event.zones],
                )
            ]
        )
        .on_conflict_do_update(
            index_elements=[Event.base_event_id, Event.event_id],
            set_=dict(last_updated_dt=datetime.datetime.now()),
        )
    )


async def main():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('https://provider.code-challenge.feverup.com/api/events', ssl=False) as resp:
    #         xml_from_resp = await resp.text()
    #         event_list = eventList.from_xml(xml_from_resp)

    xml_doc = pathlib.Path("response.xml").read_text()
    event_list = eventList.from_xml(xml_doc)

    async with async_session() as db_session:
        async with db_session.begin():
            # todo luchanos add chunks
            update_base_events_query = create_update_base_events_query(
                event_list.output.base_events
            )
            await db_session.execute(update_base_events_query)
            for base_event in event_list.output.base_events:
                if (
                    base_event.sell_mode not in APPROVED_SELL_MODE
                ):  # todo тут можно прописывать все типы и не делать проверку - делать только на выдаче
                    continue
                base_event_id = base_event.base_event_id
                for event in base_event.events:
                    update_events_query = create_update_events_query(
                        event, base_event_id
                    )
                    await db_session.execute(update_events_query)


asyncio.run(main())
