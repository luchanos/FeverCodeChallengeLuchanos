import datetime
import uuid

import pytest


async def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"Success": True}


@pytest.mark.parametrize(
    "base_events_for_database, events_for_database, zones_for_database",
    [
        (
            [
                {
                    "base_event_id": "111",
                    "sell_mode": "online",
                    "title": "Test Base Event",
                    "is_active": True,
                }
            ],
            [
                {
                    "_id": uuid.uuid4(),
                    "event_id": "000111",
                    "base_event_id": "111",
                    "is_active": True,
                    "event_start_date": datetime.datetime.strptime(
                        "2021-07-31T20:00:00", "%Y-%m-%dT%H:%M:%S"
                    ),
                    "event_end_date": datetime.datetime.strptime(
                        "2021-07-31T21:00:00", "%Y-%m-%dT%H:%M:%S"
                    ),
                }
            ],
            [
                {
                    "_id": uuid.uuid4(),
                    "zone_id": "test_zone_id",
                    "capacity": 200,
                    "price": 20,
                    "name": "Platea",
                    "numbered": True,
                    "event_id": "000111",
                    "base_event_id": "111",
                    "is_active": True,
                }
            ],
        )
    ],
)
async def test_get_events_by_time_range(
    client,
    create_base_event_in_database,
    create_event_in_database,
    create_zone_in_database,
    base_events_for_database,
    events_for_database,
    zones_for_database,
):
    for base_event in base_events_for_database:
        await create_base_event_in_database(**base_event)
    for event in events_for_database:
        await create_event_in_database(**event)
    for zone in zones_for_database:
        await create_zone_in_database(**zone)

    resp = client.get(
        "/search?start_date=2017-07-11T17:32:28Z&end_date=2022-07-21T17:32:28Z"
    )
    assert resp.status_code == 200
    data_from_response = resp.json()
    assert len(data_from_response["data"]["events"]) == 1


@pytest.mark.parametrize(
    "request_params, expected_error_message",
    [
        (
            {},
            {
                "detail": [
                    {
                        "loc": ["query", "start_date"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["query", "end_date"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            {
                "start_date": "2017-07-11T17:32:28Z",
            },
            {
                "detail": [
                    {
                        "loc": ["query", "end_date"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"end_date": "2022-07-21T17:32:28Z"},
            {
                "detail": [
                    {
                        "loc": ["query", "start_date"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"start_date": "bad_start_datetime", "end_date": "bad_end_datetime"},
            {
                "detail": [
                    {
                        "loc": ["query", "start_date"],
                        "msg": "invalid datetime format",
                        "type": "value_error.datetime",
                    },
                    {
                        "loc": ["query", "end_date"],
                        "msg": "invalid datetime format",
                        "type": "value_error.datetime",
                    },
                ]
            },
        ),
        (
            {"start_date": "2022-07-11T17:32:28Z", "end_date": "2021-07-21T17:32:28Z"},
            {"detail": "Start date can't be later, than end date"},
        ),
        (
            {"start_date": "2020-09-31T17:32:28Z", "end_date": "2021-09-31T17:32:28Z"},
            {
                "detail": [
                    {
                        "loc": ["query", "start_date"],
                        "msg": "invalid datetime format",
                        "type": "value_error.datetime",
                    },
                    {
                        "loc": ["query", "end_date"],
                        "msg": "invalid datetime format",
                        "type": "value_error.datetime",
                    },
                ]
            },
        ),
    ],
)
async def test_get_events_by_time_range_422_validation_error(
    client, request_params, expected_error_message
):
    resp = client.get("/search", params=request_params)
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == expected_error_message
