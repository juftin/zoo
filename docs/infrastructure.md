## zoo Infrastucture

### API Framework

`zoo` is built on top of [FastAPI](https://fastapi.tiangolo.com/), a modern, high-performance,
asynchronous web framework for building APIs with Python. FastAPI, in turn, is built on top
of [Starlette](https://www.starlette.io/), a lightweight ASGI framework/toolkit, and
[pydantic](https://docs.pydantic.dev/latest/), a data validation and settings management library.

??? example "FastAPI"

    ```python
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    ```

### Database ORM

`zoo` uses [SQLAlchemy 2.0](https://www.sqlalchemy.org/), an Object Relational Mapper (ORM), which means it provides
a way to interact with databases using Python objects instead of raw SQL. SQLAlchemy 2.0
is the latest version of SQLAlchemy, which includes support for async/await and the
latest Python features such as type annotations.

??? example "SQLAlchemy"

    ```python
    from typing import Optional

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import Mapped, mapped_column
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()


    class Hero(Base):
        """
        Heroes Database Model
        """

        __tablename__ = "heroes"

        hero_id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str]
        powers: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)
        secret_identity_id: Mapped[Optional[int]] = mapped_column(ForeignKey("identities.identity_id"),
                                                                  nullable=True, default=None)
    ```

### Data Models

`zoo` uses [Pydantic v2](https://docs.pydantic.dev/latest/), a data validation and settings management library.
Pydantic is used to define the data models for the API endpoints, as well as the
interface between the API endpoints and the SQLAlchemy ORM models.

??? example "Pydantic"

    ```python
    from typing import Optional

    from pydantic import BaseModel


    class HeroBase(BaseModel):
        """
        Hero Base Data Model
        """

        hero_id: int
        name: str
        powers: Optional[str] = None
        secret_identity_id: Optional[int] = None
    ```

### API Authentication

`zoo` leverages [fastapi-users](https://frankie567.github.io/fastapi-users/), a high-level library for
building user authentication on top of FastAPI. fastapi-users provides a set of utilities
for registering, authenticating, and managing users, as well as a set of endpoints for
interacting with the user database.

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
