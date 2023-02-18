import asyncio
import pathlib
from copy import deepcopy

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from db.dals import EventDAL
from worker.models import eventList


class VendorClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_events(self):
        pass


engine = create_async_engine(
    settings.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def make_events(base_events) -> list:
    events = []
    for base_event in base_events:
        new_event = {
            "title": base_event.title,
            "base_event_id": base_event.base_event_id,
        }
        for event in base_event.events:
            new_event["event_start_date"] = event.event_start_date
            new_event["event_end_date"] = event.event_end_date
            for zone in event.zones:
                new_event["price"] = zone.price
                new_event["zone_id"] = zone.zone_id
                events.append(deepcopy(new_event))
    return events


async def main():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get('https://provider.code-challenge.feverup.com/api/events', ssl=False) as resp:
    #         xml_from_resp = await resp.text()
    #         modeled = eventList.from_xml(xml_from_resp)

    xml_doc = pathlib.Path("response.xml").read_text()
    modeled = eventList.from_xml(xml_doc)

    async with async_session() as db_session:
        async with db_session.begin():
            event_dal = EventDAL(db_session=db_session)
            events_list = make_events(modeled.output.base_events)
            await event_dal.write_events_to_database(events_list)


asyncio.run(main())
