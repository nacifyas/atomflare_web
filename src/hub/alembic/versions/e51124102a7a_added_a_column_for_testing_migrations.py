"""added a column for testing migrations

Revision ID: e51124102a7a
Revises:
Create Date: 2022-04-18 19:05:21.273190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e51124102a7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'services',
        sa.Column(
            'test_mig',
            sa.String(),
            nullable=True
            )
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'test_mig')
    # ### end Alembic commands ###
