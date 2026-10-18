"""add users and user_id to tasks

Revision ID: 2d571b906991
Revises: 7288379ae176
Create Date: 2026-10-17 23:53:17.988254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d571b906991'
down_revision: Union[str, Sequence[str], None] = '7288379ae176'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Создаем таблицу пользователей
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # 2. Добавляем user_id как NULLABLE (чтобы не упало на старых задачах)
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=True))

    # 3. УДАЛЯЕМ старые тестовые задачи (у них нет владельца)
    # В реальном проекте здесь был бы UPDATE, привязывающий старые задачи к админу,
    # но для учебного проекта проще снести их.
    op.execute("DELETE FROM tasks")

    # 4. Теперь безопасно делаем поле NOT NULL
    op.alter_column('tasks', 'user_id', nullable=False)

    # 5. Добавляем индекс и ИМЕНОВАННЫЙ внешний ключ
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    op.create_foreign_key('fk_tasks_user_id', 'tasks', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем внешний ключ по имени
    op.drop_constraint('fk_tasks_user_id', 'tasks', type_='foreignkey')
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    op.drop_column('tasks', 'user_id')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')