"""Add Auth0 identity to users.

Revision ID: a8f24c9d71e3
Revises: c21752904d32
"""

from alembic import op
import sqlalchemy as sa


revision: str = "a8f24c9d71e3"
down_revision: str = "c21752904d32"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("auth_issuer", sa.String(255), nullable=True)
    )
    op.add_column(
        "users", sa.Column("auth_subject", sa.String(255), nullable=True)
    )
    op.create_unique_constraint(
        "uq_users_auth_identity", "users", ["auth_issuer", "auth_subject"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_users_auth_identity", "users", type_="unique")
    op.drop_column("users", "auth_subject")
    op.drop_column("users", "auth_issuer")
