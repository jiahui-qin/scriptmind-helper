"""Shared test fixtures for ScriptMind AI backend tests."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import Base, engine, SessionLocal


@pytest.fixture
def db():
    """Create a fresh SQLite database for each test."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
