"""Allow incomplete user profiles during Auth0 provisioning."""

from alembic import op
import sqlalchemy as sa

revision = "b9e35da802f4"
down_revision = "a8f24c9d71e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for name, length in (("first_name", 120), ("last_name", 120), ("email", 254)):
        op.alter_column("users", name, existing_type=sa.String(length), nullable=True)


def downgrade() -> None:
    # Complete missing profiles before downgrade; do not invent contact data.
    for name, length in (("first_name", 120), ("last_name", 120), ("email", 254)):
        op.alter_column("users", name, existing_type=sa.String(length), nullable=False)
