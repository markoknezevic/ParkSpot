"""Reusable slug model behavior."""

import re
import unicodedata

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates


class SlugMixin:
    """Adds a slug generated from a model's name field."""

    slug: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    @validates("name")
    def generate_slug(self, _: str, name: str) -> str:
        """Generate the URL-safe slug whenever the name changes."""

        normalized_name = unicodedata.normalize("NFKD", name)
        ascii_name = normalized_name.encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
        if not slug:
            raise ValueError("Name must contain letters or numbers")

        self.slug = slug
        return name
