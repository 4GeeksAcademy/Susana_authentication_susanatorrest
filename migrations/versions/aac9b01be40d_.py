"""empty message

Revision ID: aac9b01be40d
Revises: 0fc85fc6eeb0
Create Date: 2024-03-04 20:16:59.631102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aac9b01be40d'
down_revision = '0fc85fc6eeb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=250), nullable=False))
        batch_op.add_column(sa.Column('username', sa.String(length=250), nullable=False))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('is_active')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('password',
               existing_type=sa.String(length=250),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.drop_column('username')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
