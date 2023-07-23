CREATE TABLE "cities" (
  "id" integer PRIMARY KEY,
  "name" string,
  "lat" float,
  "lon" float,
  "country" string
);

CREATE TABLE "forecasts" (
  "id" integer PRIMARY KEY,
  "city_id" integer,
  "fetch_time" timestamp
);

CREATE TABLE "measurements" (
  "id" integer PRIMARY KEY,
  "time_measured" timestamp,
  "temperature" float,
  "humidity" float,
  "wind_speed" float,
  "forecast_id" integer
);

ALTER TABLE "measurements" ADD FOREIGN KEY ("forecast_id") REFERENCES "forecasts" ("id");

ALTER TABLE "forecasts" ADD FOREIGN KEY ("city_id") REFERENCES "cities" ("id");
