"""Initial migration

Revision ID: 37e8df3f5102
Revises:
Create Date: 2026-05-04 21:59:13.434967

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "37e8df3f5102"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rights",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "write",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "read",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "only_own",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("model", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__rights")),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__roles")),
        sa.UniqueConstraint("name", name=op.f("uq__roles__name")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
        sa.UniqueConstraint("username", name=op.f("uq__users__username")),
    )
    op.create_index(
        op.f("ix__users__username"), "users", ["username"], unique=False
    )
    op.create_table(
        "advertisements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__advertisements__user_id__users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__advertisements")),
    )
    op.create_table(
        "role_right_relation",
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("right_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["right_id"],
            ["rights.id"],
            name=op.f("fk__role_right_relation__right_id__rights"),
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk__role_right_relation__role_id__roles"),
        ),
        sa.PrimaryKeyConstraint(
            "role_id", "right_id", name=op.f("pk__role_right_relation")
        ),
    )
    op.create_table(
        "user_role_relation",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk__user_role_relation__role_id__roles"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__user_role_relation__user_id__users"),
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "role_id", name=op.f("pk__user_role_relation")
        ),
    )


def downgrade() -> None:
    op.drop_table("user_role_relation")
    op.drop_table("role_right_relation")
    op.drop_table("advertisements")
    op.drop_index(op.f("ix__users__username"), table_name="users")
    op.drop_table("users")
    op.drop_table("roles")
    op.drop_table("rights")