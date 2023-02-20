from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres",
)
PROVIDER_URL = env.str(
    "PROVIDE_URL", default="https://provider.code-challenge.feverup.com/api/events"
)
EVENT_REFRESHER_MINUTES_PERIOD = env.int("EVENT_REFRESHER_MINUTES_PERIOD", default=1)
EVENT_DEACTIVATOR_MINUTES_PERIOD = env.int(
    "EVENT_DEACTIVATOR_MINUTES_PERIOD", default=1
)
EVENT_DEACTIVATOR_DAYS_VALID_PERIOD = env.int(
    "EVENT_DEACTIVATOR_DAYS_VALID_PERIOD", default=7
)


# test envs
TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test",
)
