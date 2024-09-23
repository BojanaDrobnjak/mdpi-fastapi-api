# mdpi_api

This is a FastAPI project that provides an API for MDPI.

## Poetry

This project uses poetry. It's a dependency management tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m mdpi_api
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build -d
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

## Accessing the API

The API is available at http://localhost/api:8000 if you run it locally.
API is also accessible at public IP address: http://ec2-35-158-17-70.eu-central-1.compute.amazonaws.com:8000.

### Getting a JWT Token

To obtain a JWT token, you need to use the /api/auth/token endpoint. Use the credentials sent in the email.

```bash
email: example@mdpi.com
password: example_pass
```

The token you receive will be valid for 15 minutes. You can include this token in the Authorization header as Bearer <your_token> when accessing secured endpoints.

## MkDocs Documentation

This project uses MkDocs to generate and serve documentation.

### Running MkDocs Locally

To run MkDocs locally, you can use the following command:

```bash
mkdocs serve -a 0.0.0.0:8001
```

By default, the documentation will be available at http://localhost:8001. You can access it from your web browser while the MkDocs server is running.
If you do not specify port, default port is 8000.

### Building MkDocs

To build MkDocs, you can use the following command:

```bash
mkdocs build
```

This command will create a site directory containing all the static files for your documentation, which you can serve using any web server.
