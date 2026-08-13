"""initialize schema

Revision ID: f58de391993e
Revises: 
Create Date: 2026-08-13 11:32:19.232172

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'f58de391993e'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
