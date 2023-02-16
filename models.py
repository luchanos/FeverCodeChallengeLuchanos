from typing import Tuple

from pydantic_xml import BaseXmlModel, attr, element


class BaseXmlTunedModel(BaseXmlModel):
    class Config:
        anystr_strip_whitespace = True


class Zone(BaseXmlTunedModel):
    zone_id: str = attr()


class Event(BaseXmlTunedModel):
    zones: Tuple[Zone, ...] = element(tag='zone')
    event_start_date: str = attr()
    event_end_date: str = attr()
    event_id: str = attr()


class BaseEvent(BaseXmlTunedModel):
    base_event_id: str = attr()
    sell_mode: str = attr()
    title: str = attr()
    events: Tuple[Event, ...] = element(tag='event')


class Output(BaseXmlTunedModel):
    base_events: Tuple[BaseEvent, ...] = element(tag='base_event')


class eventList(BaseXmlTunedModel):
    output: Output
    version: str = attr()
