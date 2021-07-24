# spy
this project will help you to manage the best hitmen :).

1. [Requirements](#requirements)
2. [Run](#run)
3. [Collection](#collection)
3. [ToDo](#todo)

## Requirements
1. - [docker compose](https://docs.docker.com/compose/)

## Run
Just run:
```
SETTINGS_MODULE=settings docker-compose up --build --remove-orphans
```

and wait to the app starts, the default host for the app is "http://0.0.0.0:5000".

The db will contain the required users, nota that the user id needs be sending almost in all the services will get a
404 code if the user id does not exist.

Can access to the db by a client with the following settings:
```
HOST=localhost
USER=postgres
PASSWORD=postgres
NAME=spy
PORT=5432
```

Remember free the 5000 and 5432 ports before running the app.

## Collection
Import this collection in order to get the services paths and payloads:

[postman collection](https://www.getpostman.com/collections/db06a55db3bf5b238b8d)

## ToDo
1. - Add tests.
2. - Hardest payload/headers/path_vars validation.
3. - LogIn services in order to implement in the UI.
4. - Auth, with auth0 or firebase or another JWT based technology as recommendation.
