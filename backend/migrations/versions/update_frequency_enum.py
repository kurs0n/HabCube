"""Update frequency enum values

Revision ID: update_frequency_enum
Revises: 29b716086a11
Create Date: 2025-10-20 16:57:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "update_frequency_enum"
down_revision = "29b716086a11"
branch_labels = None
depends_on = None


def upgrade():
    # Drop the old enum and recreate with new values
    # (using uppercase to match SQLAlchemy enum names)
    op.execute("ALTER TYPE frequency_enum RENAME TO frequency_enum_old")
    op.execute(
        "CREATE TYPE frequency_enum AS ENUM "
        "('EVERY_30_MIN', 'HOURLY', 'EVERY_3_HOURS', 'EVERY_6_HOURS', "
        "'DAILY', 'WEEKLY', 'MONTHLY')"
    )
    op.execute(
        "ALTER TABLE habits ALTER COLUMN frequency TYPE frequency_enum "
        "USING UPPER(frequency::text)::frequency_enum"
    )
    op.execute("DROP TYPE frequency_enum_old")


def downgrade():
    # Revert back to old enum
    op.execute("ALTER TYPE frequency_enum RENAME TO frequency_enum_new")
    op.execute("CREATE TYPE frequency_enum AS ENUM ('daily', 'weekly', 'custom')")
    op.execute(
        "ALTER TABLE habits ALTER COLUMN frequency TYPE frequency_enum USING frequency::text::frequency_enum"
    )
    op.execute("DROP TYPE frequency_enum_new")
