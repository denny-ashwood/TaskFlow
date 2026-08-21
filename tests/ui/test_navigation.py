"""
UI tests for navigation.
"""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from app.widgets.sidebar import Sidebar


@pytest.fixture
def app():
    """Create QApplication for testing."""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    return application


class TestSidebar:
    """Test sidebar navigation."""

    def test_sidebar_creation(self, app):
        """Test sidebar creation."""
        sidebar = Sidebar()

        assert sidebar is not None
        assert len(sidebar.nav_buttons) > 0

    def test_navigation_signal(self, app):
        """Test navigation signal emission."""
        sidebar = Sidebar()

        navigation_received = []
        sidebar.navigation_changed.connect(
            lambda view: navigation_received.append(view)
        )

        # Click dashboard button
        sidebar.nav_buttons['dashboard'].click()

        assert len(navigation_received) == 1
        assert navigation_received[0] == 'dashboard'

    def test_set_active(self, app):
        """Test setting active navigation item."""
        sidebar = Sidebar()

        sidebar.set_active('today')

        assert sidebar.nav_buttons['today'].isChecked()
        assert not sidebar.nav_buttons['dashboard'].isChecked()