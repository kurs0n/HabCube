"""add_icon_to_habits

Revision ID: 7b3ce3e44354
Revises: update_frequency_enum
Create Date: 2025-11-19 16:57:38.620103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3ce3e44354'
down_revision = 'update_frequency_enum'
branch_labels = None
depends_on = None


def upgrade():
    # Add the icon column as VARCHAR (not using native enum to match FrequencyType pattern)
    op.add_column(
        'habits',
        sa.Column('icon', sa.String(length=50), nullable=True, server_default='star')
    )


def downgrade():
    # Remove the icon column
    op.drop_column('habits', 'icon')
