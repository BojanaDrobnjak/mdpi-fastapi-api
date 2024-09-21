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
