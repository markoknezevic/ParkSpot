"""Allow local embeddings while retaining existing document vectors."""

from alembic import op
from pgvector.sqlalchemy import VECTOR

revision = "f7a291c4d608"
down_revision = "e5c9f8a12b30"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("parking_documents", "embedding", existing_type=VECTOR(1536), type_=VECTOR(), existing_nullable=False)
    op.create_check_constraint(
        "local_embedding_dimensions",
        "parking_documents",
        "embedding_model != 'BAAI/bge-small-en-v1.5' OR vector_dims(embedding) = 384",
    )


def downgrade() -> None:
    # This cast intentionally refuses to discard or resize 384-dimensional data.
    # Restore/regenerate the previous model's vectors before downgrading.
    op.alter_column(
        "parking_documents", "embedding", existing_type=VECTOR(), type_=VECTOR(1536),
        existing_nullable=False, postgresql_using="embedding::vector(1536)",
    )
    op.drop_constraint(op.f("ck_parking_documents_local_embedding_dimensions"), "parking_documents", type_="check")
