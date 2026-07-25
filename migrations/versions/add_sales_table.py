"""Create sales table

Revision ID: add_sales_table
Revises: 3eeebfeb62ed
Create Date: 2026-07-21

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_sales_table"
down_revision = "3eeebfeb62ed"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "sales",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "sale_date",
            sa.Date(),
            nullable=False
        ),

        sa.Column(
            "customer_name",
            sa.String(length=150),
            nullable=False
        ),

        sa.Column(
            "invoice_no",
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            "value",
            sa.Float(),
            nullable=False,
            default=0
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint("id")
    )


def downgrade():

    op.drop_table("sales")