"""
Generic database utility models
"""

import datetime
from typing import Any, ClassVar, Dict

from sqlmodel import Field, SQLModel


class Health(SQLModel):
    """
    Health model
    """

    status: str = Field(description="The status of the application")
    code: int = Field(description="The status code of the response")
    timestamp: datetime.datetime = Field(description="The timestamp of the response generated by the server")

    class Config:
        """
        Config for Health
        """

        schema_extra: ClassVar[Dict[str, Any]] = {
            "examples": [
                {
                    "status": "OK",
                    "code": 200,
                    "timestamp": "2021-05-01T12:00:00.000000+00:00",
                }
            ]
        }