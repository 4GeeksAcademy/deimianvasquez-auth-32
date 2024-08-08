"""empty message

Revision ID: 895f4cc0bd7c
Revises: 8c78b52dff33
Create Date: 2024-08-08 03:21:51.059838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895f4cc0bd7c'
down_revision = '8c78b52dff33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=180),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=180),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###