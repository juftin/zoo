"""
Application Info
"""

from textwrap import dedent

__version__ = "0.1.0"
__application__ = "zoo"
__description__ = "An asynchronous zoo API, powered by FastAPI and SQLModel"


_md_desc = f"""
### {__description__}

[<img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo">](https://juftin.com)
"""  # noqa: E501

__markdown_description__ = dedent(_md_desc).strip()
