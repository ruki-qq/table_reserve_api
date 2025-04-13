"""add cascade deletion

Revision ID: f2eb8b96b246
Revises: d52b05aa3aec
Create Date: 2025-04-12 21:06:28.961134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2eb8b96b246"
down_revision: Union[str, None] = "d52b05aa3aec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("reservations_table_id_fkey", "reservations", type_="foreignkey")
    op.create_foreign_key(None, "reservations", "tables", ["table_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "reservations", type_="foreignkey")
    op.create_foreign_key("reservations_table_id_fkey", "reservations", "tables", ["table_id"], ["id"])
    # ### end Alembic commands ###
