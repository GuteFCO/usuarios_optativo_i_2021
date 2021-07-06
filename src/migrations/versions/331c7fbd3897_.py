"""empty message

Revision ID: 331c7fbd3897
Revises: 79c80b05ba17
Create Date: 2021-06-09 13:15:55.007637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '331c7fbd3897'
down_revision = '79c80b05ba17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #  op.execute("ALTER TABLE usuario ALTER COLUMN edad TYPE INTEGER USING edad::numeric")
    op.drop_column('usuario', 'edad')
    op.add_column('usuario', sa.Column('edad', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #  op.execute("ALTER TABLE usuario ALTER COLUMN edad TYPE INTEGER USING edad::numeric")
    op.drop_column('usuario', 'edad')
    op.add_column('usuario', sa.Column('edad', sa.String(), nullable=True))
    # ### end Alembic commands ###
