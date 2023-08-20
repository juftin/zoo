## zoo Infrastucture

### API Framework

`zoo` is built on top of [FastAPI](https://fastapi.tiangolo.com/), a modern, high-performance,
asynchronous web framework for building APIs with Python. FastAPI, in turn, is built on top
of [Starlette](https://www.starlette.io/), a lightweight ASGI framework/toolkit, and
[pydantic](https://docs.pydantic.dev/latest/), a data validation and settings management library.

#### FastAPI

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Database ORM

`zoo` uses [SQLModel](https://sqlmodel.tiangolo.com/), a library that provides a declarative
interface for interacting with databases in Python. SQLModel is built on top
of [Pydantic](https://pydantic-docs.helpmanual.io/) and
[SQLAlchemy](https://www.sqlalchemy.org/), a popular SQL toolkit and ORM for Python.

#### SQLModel

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

### Database Migrations

`zoo` uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations. Alembic
is a lightweight database migration tool for SQLAlchemy. It includes a command-line tool for
generating migrations, and a Python API for creating migrations programmatically.

#### Starting a New Migration

Before starting a new migration or making changes, make sure the database
is up to date with the latest migration:

```shell
alembic upgrade head
```

Once the database is up to date, make your changes to the underlying database schema
using the SQLModel ORM models. Once your code changes are complete, generate a new
migration script and use the `--autogenerate` flag to automatically generate the migration:

=== "alembic"

    ```shell
    alembic revision --autogenerate -m "Add hero table"
    ```

=== "hatch"

    ```python
    hatch run app:migrate --autogenerate -m "Add hero table"
    ```

#### Notes on a Migration Cold Start

When running a migration for the first time, Alembic will generate a migration script that
includes the entire database schema.

Start from a clean database by removing the `zoo/zoo.sqlite` file.

```shell
rm zoo/zoo.sqlite
```

Initialize the alembic migrations directory. Make notes of the `migration/env.py` file, as well as
the `migration/script.py.mako` file. These files have some modifications to fit the `zoo` project.

```shell
alembic init migrations --template async
```

Generate the initial migration automatically - this will create a new
migration script in `migrations/versions/` containing the entire database schema.

```shell
alembic revision --autogenerate -m "Initial migration"
```

Run the database migration:

```shell
alembic upgrade head
```
