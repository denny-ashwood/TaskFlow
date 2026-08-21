"""
Views package initialization.
"""

from app.ui.views.dashboard_view import DashboardView
from app.ui.views.today_view import TodayView
from app.ui.views.upcoming_view import UpcomingView
from app.ui.views.overdue_view import OverdueView
from app.ui.views.completed_view import CompletedView
from app.ui.views.calendar_view import CalendarView
from app.ui.views.settings_view import SettingsView

__all__ = [
    'DashboardView',
    'TodayView',
    'UpcomingView',
    'OverdueView',
    'CompletedView',
    'CalendarView',
    'SettingsView',
]