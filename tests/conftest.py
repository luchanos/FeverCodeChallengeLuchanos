import asyncio
import datetime
import os
import uuid
from typing import Any
from typing import Callable
from typing import Generator

import asyncpg
import pytest
from asyncpg import Pool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import settings
from db.session import get_db
from main import app

CLEAN_TABLES = ["events", "base_events"]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test() -> sessionmaker:
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    f"""TRUNCATE TABLE {table_for_cleaning} CASCADE;"""
                )


async def _get_test_db() -> sessionmaker:
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            settings.TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        print("test session closed")


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool() -> Pool:
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture
async def create_base_event_in_database(asyncpg_pool: Pool):
    async def create_base_event_in_database_inner(
        base_event_id: str,
        sell_mode: str,
        title: str,
        is_active: bool = True,
        last_update_dt: datetime.datetime = datetime.datetime.now(),
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO base_events (base_event_id, sell_mode, title, is_active, last_updated_dt)
                 VALUES ($1, $2, $3, $4, $5)""",
                base_event_id,
                sell_mode,
                title,
                is_active,
                last_update_dt,
            )

    return create_base_event_in_database_inner


@pytest.fixture
async def create_event_in_database(asyncpg_pool: Pool) -> Callable:
    async def create_event_in_database_inner(
        _id: uuid.UUID,
        event_id: str,
        base_event_id: str,
        event_start_date: datetime.datetime,
        event_end_date: datetime.datetime,
        is_active: bool = True,
        last_updated_dt: datetime.datetime = datetime.datetime.now(),
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO events (id, event_id, base_event_id, event_start_date, event_end_date, is_active, last_updated_dt)
                 VALUES ($1, $2, $3, $4, $5, $6, $7)""",
                _id,
                event_id,
                base_event_id,
                event_start_date,
                event_end_date,
                is_active,
                last_updated_dt,
            )

    return create_event_in_database_inner


@pytest.fixture
async def create_zone_in_database(asyncpg_pool: Pool) -> Callable:
    async def create_zone_in_database_inner(
        _id: uuid.UUID,
        zone_id: str,
        capacity: int,
        price: float,
        name: str,
        event_id: str,
        base_event_id: str,
        numbered: bool = True,
        is_active: bool = True,
        last_updated_dt: datetime.datetime = datetime.datetime.now(),
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                """INSERT INTO zones (id, zone_id, capacity, price, name, numbered, event_id, base_event_id, is_active, last_updated_dt)
                 VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)""",
                _id,
                zone_id,
                capacity,
                price,
                name,
                numbered,
                event_id,
                base_event_id,
                is_active,
                last_updated_dt,
            )

    return create_zone_in_database_inner
