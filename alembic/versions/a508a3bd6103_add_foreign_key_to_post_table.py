"""add foreign key to post table

Revision ID: a508a3bd6103
Revises: 7ca0bc23f7f2
Create Date: 2023-10-07 07:58:30.677580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a508a3bd6103'
down_revision: Union[str, None] = '7ca0bc23f7f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("fk_posts_user_id_users", source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("fk_posts_user_id_users", "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
    pass
