# Fever Code Challenge App by Nikolai Sviridov aka luchanos
<p>
<img src="https://raw.githubusercontent.com/gist/brudnak/aba00c9a1c92d226f68e8ad8ba1e0a40/raw/e1e4a92f6072d15014f19aa8903d24a1ac0c41a4/nyan-cat.gif" alt="drawing" width="500"/>
</p>

# Summary
This is a brief implementation of service for operating with external providers events due to Fever Job Interview
test task.

# Content
- [Overview](#Overview)
- [Ideas](#ideas)
- [Migrations](#migrations)
- [Deployment](#deployment)
- [Tests](#tests)


# Overview
The system consists of 3 main blocks:
- API

Let us get an information about events in any datetime ranges, even historically.

- Events updater worker

This part responsible for refreshing actual data about events in database.

- Events deactivator worker

This part responsible for deactivation non-actual events in case of cancelling for example.

# Ideas and Solutions

Our API must be independent of providers side in situations, when provider is out of service. Furthermore, we need to
keep RPS to providers side in acceptable ranges.

Solution:
We can get data from our providers periodically. This data we can store in database for future usage. For that reason
in [.workers/event_refresher_worker.py](workers/event_refresher_worker.py) codebase was implemented. It creates new events and updates information about
old ones.

Events have last_updated_dt field which shows last moment, when information about event was updated. If event cancelled
then this field outdated more and more on each cycle of refreshing. On that way we can highlight them by simple query
and deactivate by setting is_active field to False value by worker in [.workers/event_deactivator_worker.py](workers/event_deactivator_worker.py)

If event just changed in time (early or later) - it's not a problem for us. Our worker handle with it too by refreshing
datetime ranges fields.

# Migrations

For running migrations use [alembic](https://alembic.sqlalchemy.org/en/latest/) and follow this steps:

## For local dev

- Be sure that you have virtual environment on your project and activate it by ```venv/bin/activate```
- Install all requirements by ```pip install -r requirements.txt```
- Init alembic migrations by ```alembic init migrations```
- Go to created alembic.ini file and set sqlalchemy.url to desirable database url address. Set postgresql://postgres:postgres@localhost:5432/postgres
if you want to use default settings for local deployment (BUT! previously then you need to run ```make local_up``` then previously).
- Go to created migrations/env.py file and change target_metadata value to ```target_metadata = Base.metadata``` (don't forget import Base class previously from db.models then).
- Run ```alembic revision --autogenerate -m "comment to your migration"``` - migration file(s) will be generated.
- Run ```alembic upgrade heads``` - all generated migrations will be run to the database.
- Check database structure and make sure that everything run successfully.
- PROFIT!!!

## For production

**<text style="color:red;">WARNING! SENSITIVE AREA!</text>** Before running migrations on production state BE SURE that your other services or critical functionality wouldn't be affected by changes! It's mandatory to ask your TechLead or
other authorised responsible person for support!

You must run migrations on production according to your corporate rules, but if you have nothing of them you can use quite the same way as for local dev:

- Go to container with your app service on the server by ```docker exec -it <your_app_container_id> sh```
- Init alembic migrations by ```alembic init migrations```
- Go to created alembic.ini file and set sqlalchemy.url to desirable database url address - set here the value from env REAL_DATABASE_URL.
- Go to created migrations/env.py file and change target_metadata value to ```target_metadata = Base.metadata``` (don't forget import Base class previously from db.models then).
- Run ```alembic revision --autogenerate -m "comment to your migration"``` - migration file(s) will be generated.
- Run ```alembic upgrade heads``` - all generated migrations will be run to the database.
- Check database structure and make sure that everything run successfully.
- PROFIT!!!

# Deployment

## Local

For local development please use settings from [docker-compose-local.yaml](docker-compose-local.yaml) file (change it if necessary).

- Run ```make local_up``` and wait until all containers started.

## Production

**<text style="color:red;">WARNING! SENSITIVE AREA!</text>** Before deployment on production state BE SURE that your other services or critical functionality wouldn't be affected by changes! It's mandatory to ask your TechLead or
other authorised responsible person for support!
For production development please use settings from [docker-compose-ci.yaml](docker-compose-local.yaml) file (change it if necessary).

- Run ```make run``` and wait until all containers started.
