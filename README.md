# Fever Code Challenge App by Nikolai Sviridov aka luchanos
<p>
<img src="https://raw.githubusercontent.com/gist/brudnak/aba00c9a1c92d226f68e8ad8ba1e0a40/raw/e1e4a92f6072d15014f19aa8903d24a1ac0c41a4/nyan-cat.gif" alt="drawing" width="500"/>
</p>

# Summary
This is a brief implementation of service for operating with external providers events due to Fever Job Interview
test task.

✋ PLEASE! IF YOU HAVE ANY QUESTIONS - LET'S DISCUSS IT! COOPERATION AND INTERACTION - WAY TO THE BEST PRODUCT EVER 😊

# Content
- [Overview](#Overview)
- [Ideas](#ideas)
- [Migrations](#migrations)
- [Deployment](#deployment)
- [Tests](#tests)
- [APIDocs](#apidocs)
- [Improvements](#improvements)
- [ExtraMile](#extramile)
- [FindedErrors](#findederrors)


# Overview
The system consists of 3 main blocks:
- API

Let us get an information about events in any datetime ranges, even historically.

- Events updater worker

This part responsible for refreshing actual data about events in database.

- Events deactivator worker

This part responsible for deactivation non-actual events in case of cancelling for example.

# Ideas

Our API must be independent of providers side in situations, when provider is out of service. Furthermore, we need to
keep RPS to providers side in acceptable ranges.

Solution:
We can get data from our providers periodically and then use it on our side. For that reason
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
- Go to created alembic.ini file and set sqlalchemy.url to desirable database url address. Set `postgresql://postgres:postgres@localhost:5432/postgres`
if you want to use default settings for local deployment (BUT! previously then you need to run ```make local_up``` then previously).
- Go to created migrations/env.py file and change target_metadata value to ```target_metadata = Base.metadata``` (don't forget import Base class previously from db.models then).
- Run ```alembic revision --autogenerate -m "comment to your migration"``` - migration file(s) will be generated.
- Run ```alembic upgrade heads``` - all generated migrations will be run to the database.
- Check database structure and make sure that everything run successfully.
- PROFIT!!!

## For production

**<text style="color:red;">WARNING! SENSITIVE AREA!</text>** Before running migrations on production state BE SURE that your other services or critical functionality wouldn't be affected by changes! It's mandatory to ask your TechLead or
other authorised responsible person for support!

Pay attention, that we use nginx as reverse-proxy server for our project via Docker. If you have already installed nginx on your target server please exclude nginx from docker-compose-ci and
make other changes if necessary.

You must run migrations on production according to your corporate rules, but if you have nothing of them you can use quite the same way as for local dev:

- Go to container with your app service on the server by ```docker exec -it <your_app_container_id> sh```
- Init alembic migrations by ```alembic init migrations```
- Go to created alembic.ini file and set sqlalchemy.url to desirable database url address - set here the value from env `REAL_DATABASE_URL`.
- Go to created migrations/env.py file and change target_metadata value to ```target_metadata = Base.metadata``` (don't forget import Base class previously from db.models then).
- Run ```alembic revision --autogenerate -m "comment to your migration"``` - migration file(s) will be generated.
- Run ```alembic upgrade heads``` - all generated migrations will be run to the database.
- Check database structure and make sure that everything run successfully.
- PROFIT!!!

According to the task my implementation of database tables is:

![alt text](docs/images/db_diagram.png)

We use indexes for column of date types, because according to our task we have lots of requests for searching by that fields.

# Deployment

## Local

For local development please use settings from [docker-compose-local.yaml](docker-compose-local.yaml) file (change it if necessary).

- Run ```make local_up``` and wait until all containers started.

## Production

**<text style="color:red;">WARNING! SENSITIVE AREA!</text>** Before deployment on production state BE SURE that your other services or critical functionality wouldn't be affected by changes! It's mandatory to ask your TechLead or
other authorised responsible person for support!
For production development please use settings from [docker-compose-ci.yaml](docker-compose-local.yaml) file (change it if necessary).

- Run ```make run``` and wait until all containers started.

# Tests

For local testing in this project we don't use mocks of request to the database. We use containers - it let us check
integrations between life-important components. This attitude good recommended itself in big projects with complex business logic in case
of decreasing bugs appearance level. After building CI/CD pipeline it's possible use docker-in-docker attitude to run it
on server side as a part of pipeline.

For running local tests:
- Run `make local_up` and wait until all containers started.
- Run tests in project via IDE or in terminal by `pytest run` (make sure all requirement dependencies had been installed previously).
- On the first time running it should fail, because we need to change alembic database to the test url (check credentials in [docker-compose-local.yaml](docker-compose-local.yaml)).
- Rerun tests. If it's failed again because of database structure you can run migrations manually as mentioned above but with test database credentials.

# APIDocs

FastAPI is a framework which generates apidocs automatically based on created request/response Pydantic schemas.
Documentation for APIs can be found on /docs endpoint of the webapp (by local default it is http://0.0.0.0:8000/docs).

![alt text](docs/images/swagger.png)

# Improvements

Of course, I undertand that we need to set up here some sort of:
- Metrics (Grafana, Prometheus)
- Logs (Kibana, Elasticsearch)
- Errors (Sentry)
- Tests, tests, tests + coverage more than 85%
- MyPy typings

I can do it, but I think that as test task implementation it is not important.

# ExtraMile

For scaling our application we should understand the way of our product in the future. For example:
- SLA
- read/write relation
- geography of users

If we have geographically widespread usage of our application we can create several DNS servers with instances of our
service and database. Database should be replicated and data there must be sharded into pieces for better accessibility
and durability.

We can use Kubernetes for orchestration our application. It let us run additional instances at peak hours automatically.

Import of new events with hundreds of providers and hundreds of zones inside - operation with high time complexity.
Because of that we can create standalone import service with common interface for all events, and it can be implemented
via rabbitMQ or Kafka + several consumers.

According to future task types it's possible to choose NoSQL database (as MongoDB) for solving specific searching tasks.

We can provide cache on web-app side (time of expiry depends on time of data changing on provider side)

On the Python side - we can use asyncio for better speed of I/O tasks.

Anyway a lot of architecture decisions should be done according to business tasks, company resources and team expertise.

# FindedErrors

Due to author's experience in checking [reference instance](https://app.swaggerhub.com/apis-docs/luis-pintado-feverup/backend-test/1.0.0) of API and data from provider it should be mentioned here some moments, which can be
fixed in the future:

- Now it's possible to set starts_at later than ends_at. The application tries to get data from database that is not necessary. It's better
to have validation request params for that reason.
- Now in [reference of providers data](https://provider.code-challenge.feverup.com/api/events) 31st September 2021 may be found. But September
has only 30 days. It's a bug on provider side. The behaviour of our web service that way should be discussed - here several possible attitudes
could be implemented.
- Small mistake in description of max_price field. Now it's 'Min price from all the available tickets'
