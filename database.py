"""Database models and session management for S1NGULARITY.

Implements feedback logging and analytics as described in:
- s1ngularity-security-feedback.json
- s1ngularity-analytics-insights.json
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import AsyncGenerator, Optional

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

# Base class for models
Base = declarative_base()


class FeedbackLog(Base):
    """Feedback and error logging.

    Implements logging structure from s1ngularity-security-feedback.json
    """
    __tablename__ = "feedback_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)

    # Error/Feedback categorization
    error_type = Column(String(100), nullable=True, index=True)  # hallucination, bias, technical_error
    category = Column(String(100), nullable=True)  # resume_analysis, jd_breakdown, boolean_search
    severity = Column(String(20), default="info")  # info, warning, error, critical

    # Context
    user_input = Column(Text, nullable=True)
    system_response = Column(Text, nullable=True)
    context = Column(JSON, nullable=True)  # Additional metadata

    # Correction & Impact
    correction = Column(Text, nullable=True)  # What was the correct answer
    impact = Column(String(50), nullable=True)  # low, medium, high

    # Resolution
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)


class SessionHistory(Base):
    """User session history and conversation state."""
    __tablename__ = "session_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Session metadata
    task_type = Column(String(50), nullable=True)  # jd_analysis, resume_screening, etc.
    active_role_id = Column(String(100), nullable=True)  # JobDiva role ID if applicable
    conversation_state = Column(JSON, nullable=True)  # Stateful conversation data

    # Analytics
    message_count = Column(Integer, default=0)
    token_usage = Column(Integer, default=0)


class CandidateInteraction(Base):
    """Track candidate evaluations and interactions.

    Supports analytics from s1ngularity-analytics-insights.json
    """
    __tablename__ = "candidate_interactions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)

    # Candidate info
    candidate_id = Column(String(100), nullable=True, index=True)  # JobDiva candidate ID
    candidate_email = Column(String(255), nullable=True, index=True)

    # Evaluation
    job_id = Column(String(100), nullable=True, index=True)
    match_score = Column(Float, nullable=True)  # 0-100 score
    skill_match = Column(Float, nullable=True)
    experience_match = Column(Float, nullable=True)

    # Flags
    green_flags = Column(JSON, nullable=True)
    yellow_flags = Column(JSON, nullable=True)
    red_flags = Column(JSON, nullable=True)
    bias_flags = Column(JSON, nullable=True)

    # Action taken
    action = Column(String(50), nullable=True)  # viewed, shortlisted, rejected, contacted
    outcome = Column(String(50), nullable=True)  # hired, declined, no_response


class JobAnalysis(Base):
    """Store job description analyses.

    Supports context awareness from s1ngularity-context-awareness.json
    """
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)

    # Job info
    job_id = Column(String(100), nullable=True, unique=True, index=True)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)

    # Parsed JD
    core_skills = Column(JSON, nullable=True)
    nice_to_have = Column(JSON, nullable=True)
    tools_platforms = Column(JSON, nullable=True)
    red_flags = Column(JSON, nullable=True)

    # Generated artifacts
    layman_guide = Column(Text, nullable=True)
    boolean_query = Column(Text, nullable=True)
    ideal_profile = Column(JSON, nullable=True)


class AnalyticsMetric(Base):
    """Store aggregate analytics metrics.

    Implements analytics from s1ngularity-analytics-insights.json
    """
    __tablename__ = "analytics_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    metric_name = Column(String(100), nullable=False, index=True)  # avg_match_score, bias_flag_rate
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)  # percentage, count, score

    # Dimensions
    dimension_type = Column(String(50), nullable=True, index=True)  # job_role, industry, location
    dimension_value = Column(String(255), nullable=True, index=True)

    # Aggregation period
    period = Column(String(20), nullable=True)  # hourly, daily, weekly, monthly
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)


# Database connection and session management
class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self, database_url: Optional[str] = None):
        """Initialize database manager.

        Args:
            database_url: Database connection URL (defaults to DATABASE_URL env var)
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite+aiosqlite:///./s1ngularity.db"  # Fallback to SQLite
        )

        # Create async engine
        self.engine = create_async_engine(
            self.database_url,
            echo=os.getenv("DEBUG", "false").lower() == "true",
            poolclass=NullPool if "sqlite" in self.database_url else None,
            pool_pre_ping=True,
        )

        # Create session maker
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_tables(self):
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """Drop all database tables (use with caution)."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session (use with async context manager)."""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get or create global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions."""
    db_manager = get_db_manager()
    async for session in db_manager.get_session():
        yield session


# Initialize database on import (optional)
async def init_db():
    """Initialize database tables."""
    db_manager = get_db_manager()
    await db_manager.create_tables()
    print("✅ Database tables created successfully")


__all__ = [
    "Base",
    "FeedbackLog",
    "SessionHistory",
    "CandidateInteraction",
    "JobAnalysis",
    "AnalyticsMetric",
    "DatabaseManager",
    "get_db_manager",
    "get_db_session",
    "init_db",
]
