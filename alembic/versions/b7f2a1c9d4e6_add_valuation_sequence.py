"""add valuation sequence

Revision ID: b7f2a1c9d4e6
Revises: 04811d707da2
Create Date: 2026-03-26 12:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7f2a1c9d4e6"
down_revision: Union[str, Sequence[str], None] = "04811d707da2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    bind.execute(
        sa.text("CREATE SEQUENCE IF NOT EXISTS valuation_seq START WITH 1 INCREMENT BY 1")
    )

    max_existing_suffix = bind.execute(
        sa.text(
            """
            SELECT COALESCE(
                MAX(CAST(split_part(valuation_id, '-', 3) AS BIGINT)),
                0
            )
            FROM valuation_reports
            WHERE valuation_id ~ '^DV-[0-9]{8}-[0-9]+$'
            """
        )
    ).scalar()

    if max_existing_suffix:
        bind.execute(
            sa.text("SELECT setval('valuation_seq', :value, true)"),
            {"value": int(max_existing_suffix)},
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SEQUENCE IF EXISTS valuation_seq")
