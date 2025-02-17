"""Add secret field

Revision ID: 9d286eeb033f
Revises: 7a517d44ae9f
Create Date: 2025-01-13 11:33:26.513953

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d286eeb033f"
down_revision: Union[str, None] = "7a517d44ae9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "check", sa.Column("sectet", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
    )
    op.create_index(op.f("ix_check_sectet"), "check", ["sectet"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_check_sectet"), table_name="check")
    op.drop_column("check", "sectet")
    # ### end Alembic commands ###
