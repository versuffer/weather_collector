Weather Collector
================================
Weather Collector is a service that fetches weather data for 50 biggest cities in the world from https://api.openweathermap.org.

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
