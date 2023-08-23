"""
Application Info
"""

from textwrap import dedent

__version__ = "0.1.1"
__application__ = "zoo"
__description__ = (
    "An asynchronous zoo API, powered by FastAPI, SQLAlchemy 2.0, Pydantic v2, and Alembic"
)
__favicon__ = "https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png"

_md_desc = f"""
### {__description__}

[<img src="{__favicon__}" width="120" height="120"  alt="juftin logo">](https://juftin.com)
"""

__markdown_description__ = dedent(_md_desc).strip()
