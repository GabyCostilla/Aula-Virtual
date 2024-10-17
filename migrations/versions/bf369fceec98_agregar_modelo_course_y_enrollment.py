"""Agregar modelo Course y Enrollment

Revision ID: bf369fceec98
Revises: 8fe4e947ffb8
Create Date: 2024-10-14 18:23:21.458559

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bf369fceec98'
down_revision = '8fe4e947ffb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enrollment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('start_date', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('end_date', sa.Date(), nullable=False))
        batch_op.drop_constraint('course_ibfk_1', type_='foreignkey')
        batch_op.drop_column('title')
        batch_op.drop_column('instructor_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course', schema=None) as batch_op:
        batch_op.add_column(sa.Column('instructor_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('title', mysql.VARCHAR(length=150), nullable=False))
        batch_op.create_foreign_key('course_ibfk_1', 'user', ['instructor_id'], ['id'])
        batch_op.drop_column('end_date')
        batch_op.drop_column('start_date')
        batch_op.drop_column('name')

    op.drop_table('enrollment')
    # ### end Alembic commands ###