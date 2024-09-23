### Installation

To get started with the API, you'll need to install the necessary dependencies. First, clone the repository:

```bash
git clone https://github.com/BojanaDrobnjak/mdpi-fastapi-api.git
```

Next, navigate to the project directory and install the dependencies:

```bash
cd mdpi-fastapi-api
poetry install
```

Before installing the dependencies, create a .env file based on the provided .env.example file:

```bash
cp .env.example .env
```

### Database Setup

If you’re running the project locally, make sure you have a PostgreSQL database running. The configuration for the database should match the values specified in your .env file. For example, start your PostgreSQL server and ensure it is accessible with the following credentials (replace these with your values from .env):

```bash
	•	MDPI_API_DB_BASE: mdpi_api_db
	•	MDPI_API_DB_USER: mdpi_api_user
	•	MDPI_API_DB_PASSWORD: mdpi_api_pass
	•	MDPI_API_DB_HOST: localhost
	•	MDPI_API_DB_PORT: 5432
```

You can use the psql command to start your database:

```bash
psql -h localhost -U mdpi_api_user -d mdpi_api_db -W
```

### Running the Project

To run the API, use the following command:

```bash
poetry run python -m mdpi_api
```

This will start the server on the configured host.
You can find swagger documentation at `/api/docs`.

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

#### Automatic Migration with Docker

When you run and build your Docker container using the provided docker-compose.yml file, pending migrations will be automatically applied with the following command:

```bash
alembic upgrade head
```


### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate -m "Your message"

# For empty file generation.
alembic revision
```

## Running tests

If you want to run tests, you can use this command:

```bash
poetry run pytest
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);

## API Introduction

To interact with the API, make sure you have the necessary authentication tokens. Most endpoints require valid authentication.

### Getting a JWT Token

To obtain a JWT token, you need to use the /api/auth/token endpoint. Use the credentials sent in the email.

```bash
email: example@mdpi.com
password: example_pass
```

The token you receive will be valid for 15 minutes. You can include this token in the Authorization header as Bearer <your_token> when accessing secured endpoints.

For detailed information on each route, check out the specific documentation pages:

- [Authentication](./api/auth.md): Details about user login, registration, and token handling.
- [Favorites](./api/favorites.md): Information on managing favorite cities and notifications.
- [Cities](./api/cities.md): Learn about endpoints for fetching and managing city data.
