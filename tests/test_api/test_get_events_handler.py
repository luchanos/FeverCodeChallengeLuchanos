import datetime
import uuid


async def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200


async def test_get_events_by_time_range(
    client, create_base_event_in_database, create_event_in_database
):
    base_events_for_database = [
        {
            "base_event_id": "111",
            "sell_mode": "online",
            "title": "Test Base Event",
            "is_active": True,
        }
    ]
    events_for_database = [
        {
            "_id": uuid.uuid4(),
            "event_id": "000111",
            "base_event_id": "111",
            "zones": [
                {"price": 10, "zone_id": "1"},
                {"price": 20, "zone_id": "2"},
                {"price": 30, "zone_id": "3"},
            ],
            "is_active": True,
            "event_start_date": datetime.datetime.strptime(
                "2021-07-31T20:00:00", "%Y-%m-%dT%H:%M:%S"
            ),
            "event_end_date": datetime.datetime.strptime(
                "2021-07-31T21:00:00", "%Y-%m-%dT%H:%M:%S"
            ),
        }
    ]
    for base_event in base_events_for_database:
        await create_base_event_in_database(**base_event)
    for event in events_for_database:
        await create_event_in_database(**event)
