"""add contents to post table

Revision ID: 096ec77e8680
Revises: 134d70571eed
Create Date: 2023-10-07 07:44:30.538870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '096ec77e8680'
down_revision: Union[str, None] = '134d70571eed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("contents", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "contents")
    pass
