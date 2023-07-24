Weather Collector
================================
Weather Collector is a service that fetches weather data for 50 biggest cities in the world from https://api.openweathermap.org.

Weather Collector fetches 5 days / 3 hour forecasts for loaded cities and parses temperature, humidity and wind_speed data for further saving to PostrgreSQL database.

Installation
------------
**Clone project with git:**

    git clone https://github.com/versuffer/weather_collector.git

or

    git clone git@github.com:versuffer/weather_collector.git

**Build application with docker compose**:

    docker compose build

Exploitation
------------
**To launch application use this command:**

    docker compose up -d

**To connect to PostgreSQL database with default application configuration use this command:**

    docker compose exec postgres psql -U collector -d collector_db

**To gracefully stop application use this command:**

    docker compose stop

**To check all application services logs use this command:**

    docker compose logs -f

**To check specific application service logs use this command:**

    docker compose logs {service_name} -f

Application services list:

- postgres;
- redis;
- collector;
- collector-scheduler;
- collector-worker.

Additional information
----------------------
1. Application always starts fetching data right after launching and then do it with 1 hour interval;
2. You can find database schema information in `data/schema.png` or `data/schema.sql`;
3. `data/cities.csv` contains cities data that loads to database on every application startup.
4. List of used technologies, libraries and frameworks:
- `FastAPI` - web-framefork;
- `Uvicorn` - ASGI web-server;
- `Celery` (`worker` + `beat`) - task queue + scheduler;
- `PostgreSQL` - database management system;
- `Redis` - broker for `Celery`;
- `asyncio` - async programming library;
- `asyncpg` - `PostgreSQL` async driver;
- `SQLAlchemy` - database ORM;
- `docker [compose]` - as containerization system.
5. Listed technologies were chosen to satisfy these application demands:
- horizontal scalability - `Celery` and `Redis`;
- async http-requests support - `asyncio` + `FastAPI` + `Uvicorn` + `asyncpg` (`asyncpg` is not used for async operations yet);
- reliable data storage - `PostgreSQL`;
- flexible ORM that works with any framework - `SQLAlchemy`;
- application must be easily deployed on any environment - `docker [compose]`  

6. Database schema was chosen to provide further scaling with additional weather parameters without need of duplicating data from one table to another (`normalization`).

Application bottlenecks
----------------------
1. First `fetch_forecasts()` task execution is bound to `collector-worker` service startup but not to `collector` service startup that means that several workers create *duplicated tasks* on startup;
2. Fetched weather data got from OpenWeatherMap API is temporarily stored in `result_dict` that may cause memory leak when monitoring too many cities;
3. `load_cities` is a hardcode that should be rewritten with ***interface*** for getting city data not only from pre-build `.csv` but also from `.xlsx` and other sources like `.txt`, `.xml` and external service APIs if needed;
4. Application has no API-method for getting data from database;
5. Application has no management commands for starting / stopping / rescheduling tasks.

TO DO
----------------------
1. Add migrations management with `Alembic`;
2. Reconfigure task scheduling;
3. Rewrite `load_cities`;
4. Add logging;
5. Add basis unit-tests;
6. Add task monitoring with `Flower`.