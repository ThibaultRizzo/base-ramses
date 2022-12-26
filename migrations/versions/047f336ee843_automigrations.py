"""automigrations

Revision ID: 047f336ee843
Revises: 
Create Date: 2022-12-26 18:46:58.463530

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '047f336ee843'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instrument',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('yfinance_code', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('yfinance_code')
    )
    op.create_index(op.f('ix_instrument_code'), 'instrument', ['code'], unique=True)
    op.create_index(op.f('ix_instrument_description'), 'instrument', ['description'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_instrument_description'), table_name='instrument')
    op.drop_index(op.f('ix_instrument_code'), table_name='instrument')
    op.drop_table('instrument')
    # ### end Alembic commands ###
