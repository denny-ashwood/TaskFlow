"""
Setting model.
"""

from sqlalchemy import Column, String, Text

from app.models.base import Base


class Setting(Base):
    """Application setting entity."""

    __tablename__ = 'settings'

    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Setting(key='{self.key}', value='{self.value}')>"
