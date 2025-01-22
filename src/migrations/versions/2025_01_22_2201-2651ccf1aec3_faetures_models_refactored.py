"""faetures models refactored

Revision ID: 2651ccf1aec3
Revises: 4113a9412669
Create Date: 2025-01-22 22:01:41.579663

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2651ccf1aec3"
down_revision: Union[str, None] = "4113a9412669"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
