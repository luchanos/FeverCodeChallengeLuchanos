import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Event


class EventDAL:
    """Data Access Layer for operating event info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_events_by_time_range(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ):
        query = """
SELECT d.id, be.title, d.event_start_date, d.event_end_date, d.max_price, d.min_price FROM (
SELECT e.id, e.event_start_date, e.event_end_date, right_table.base_event_id, right_table.max_price, right_table.min_price
FROM events e
LEFT JOIN (
SELECT id, base_event_id, max(prices.price_value) AS max_price, min(prices.price_value) AS min_price FROM (
WITH cte AS (
SELECT id, base_event_id, (jsonb_array_elements(zones) ->> 'price')::decimal AS price_value FROM events GROUP BY id)
SELECT id, base_event_id, price_value FROM cte) AS prices GROUP BY prices.id, base_event_id) right_table
ON e.id = right_table.id
WHERE event_start_date >= :start_date AND event_end_date <= :end_date) d
LEFT JOIN base_events be ON d.base_event_id = be.base_event_id;
"""
        res = await self.db_session.execute(
            query, {"start_date": start_date, "end_date": end_date}
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
        await self.db_session.flush()
