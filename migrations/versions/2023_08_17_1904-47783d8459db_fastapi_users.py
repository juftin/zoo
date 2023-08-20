"""fastapi-users

Revision ID: 47783d8459db
Revises: 5ff3a5bf3a14
Create Date: 2023-08-17 19:04:26.774702

"""

from typing import Sequence, Union

import fastapi_users_db_sqlmodel
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "47783d8459db"
down_revision: Union[str, None] = "5ff3a5bf3a14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Upgrade the database
    """
    op.create_table(
        "user",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "access_token",
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlmodel.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        op.f("ix_access_token_created_at"), "access_token", ["created_at"], unique=False
    )


def downgrade() -> None:
    """
    Rollback the database upgrade
    """
    op.drop_index(op.f("ix_access_token_created_at"), table_name="access_token")
    op.drop_table("access_token")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
