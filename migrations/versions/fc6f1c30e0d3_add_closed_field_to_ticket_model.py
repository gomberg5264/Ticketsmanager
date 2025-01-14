"""Add closed field to Ticket model

Revision ID: fc6f1c30e0d3
Revises: fce1b712a347
Create Date: 2024-10-16 01:29:19.688460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc6f1c30e0d3'
down_revision = 'fce1b712a347'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('closed', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_column('closed')

    # ### end Alembic commands ###
