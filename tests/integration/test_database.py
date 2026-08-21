"""
Integration tests for database operations.
"""

import pytest
from sqlalchemy import text

from app.models.base import Base
from app.models.task import Task
from app.models.category import Category


class TestDatabaseIntegration:
    """Test database operations."""

    def test_database_initialization(self, db_manager):
        """Test database initialization."""
        assert db_manager.engine is not None

        # Check if tables exist
        with db_manager.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ))
            tables = [row[0] for row in result]

            assert 'tasks' in tables
            assert 'categories' in tables
            assert 'reminders' in tables
            assert 'settings' in tables

    def test_foreign_key_constraints(self, db_manager):
        """Test foreign key constraints."""
        with db_manager.session_scope() as session:
            # Create category
            category = Category(name="Test Category")
            session.add(category)
            session.commit()

            # Create task with category
            task = Task(
                title="Test Task",
                category_id=category.id,
            )
            session.add(task)
            session.commit()

            # Try to create task with invalid category
            with pytest.raises(Exception):
                invalid_task = Task(
                    title="Invalid Task",
                    category_id=9999,
                )
                session.add(invalid_task)
                session.commit()

            session.rollback()

    def test_cascade_delete(self, db_manager):
        """Test cascade delete."""
        with db_manager.session_scope() as session:
            # Create category and task
            category = Category(name="Test")
            session.add(category)
            session.commit()

            task = Task(title="Test", category_id=category.id)
            session.add(task)
            session.commit()

            # Delete category
            session.delete(category)
            session.commit()

            # Check if task still exists
            result = session.query(Task).filter_by(id=task.id).first()
            assert result is not None
            assert result.category_id is None

    def test_transaction_rollback(self, db_manager):
        """Test transaction rollback."""
        session = db_manager.create_session()

        try:
            # Start transaction
            task = Task(title="Rollback Test")
            session.add(task)
            session.flush()

            # Force error
            raise ValueError("Test error")

        except ValueError:
            session.rollback()

            # Verify task was not saved
            result = session.query(Task).filter_by(title="Rollback Test").first()
            assert result is None

        finally:
            session.close()

    def test_concurrent_sessions(self, db_manager):
        """Test concurrent database sessions."""
        session1 = db_manager.create_session()
        session2 = db_manager.create_session()

        try:
            # Create task in session 1
            task1 = Task(title="Session 1 Task")
            session1.add(task1)
            session1.commit()

            # Create task in session 2
            task2 = Task(title="Session 2 Task")
            session2.add(task2)
            session2.commit()

            # Both sessions should see both tasks
            count1 = session1.query(Task).count()
            count2 = session2.query(Task).count()

            assert count1 == 2
            assert count2 == 2

        finally:
            session1.close()
            session2.close()