"""
Category model.
"""

from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Category(Base):
    """Category entity."""

    __tablename__ = 'categories'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Relationships
    tasks = relationship("Task", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"