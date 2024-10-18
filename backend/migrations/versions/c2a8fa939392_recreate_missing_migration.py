"""Recreate missing migration

Revision ID: c2a8fa939392
Revises: 
Create Date: 2024-10-16 09:58:27.466242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2a8fa939392'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    # Allow nulls initially when adding the column
    with op.batch_alter_table('file_types', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allowed_extensions', sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table('file_types', schema=None) as batch_op:
        batch_op.drop_column('allowed_extensions')

    # ### end Alembic commands ###
