"""Add db_type to databaseconnections.

Revision ID: 002
Revises: 001
Create Date: 2025-01-01

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add db_type column to databaseconnections table."""
    # Add db_type column with default value 'postgresql'
    op.add_column(
        'databaseconnections',
        sa.Column('db_type', sa.String(length=20), nullable=False, server_default='postgresql')
    )


def downgrade() -> None:
    """Remove db_type column from databaseconnections table."""
    op.drop_column('databaseconnections', 'db_type')

