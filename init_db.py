"""
Database initialization and migration script for S1NGULARITY.

This script:
1. Creates all database tables
2. Verifies Redis connection
3. Seeds initial data (if needed)
4. Runs health checks
"""

import asyncio
import sys
from datetime import datetime

from sqlalchemy import text
from database import (
    get_db_manager,
    FeedbackLog,
    SessionHistory,
    CandidateInteraction,
    JobAnalysis,
    AnalyticsMetric,
)

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


async def init_database():
    """Initialize database tables."""
    print("🗄️  Initializing S1NGULARITY Database...\n")
    print("=" * 60)

    db_manager = get_db_manager()

    # Drop existing tables (WARNING: only for development)
    if "--reset" in sys.argv:
        print("⚠️  Dropping all existing tables...")
        await db_manager.drop_tables()
        print("✅ Tables dropped\n")

    # Create all tables
    print("📋 Creating database tables...")
    try:
        await db_manager.create_tables()
        print("✅ Tables created successfully\n")
    except Exception as e:
        print(f"❌ Error creating tables: {e}\n")
        return False

    # Verify tables exist
    print("🔍 Verifying tables...")
    async with db_manager.engine.begin() as conn:
        # Get table names
        if "postgresql" in str(db_manager.engine.url):
            result = await conn.execute(
                text(
                    "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
                )
            )
        else:  # SQLite
            result = await conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            )

        tables = [row[0] for row in result]
        print(f"   Found {len(tables)} tables:")
        for table in tables:
            print(f"   ✓ {table}")

    print("\n" + "=" * 60)

    # Test insert and retrieve
    print("\n🧪 Testing database operations...")
    async for session in db_manager.get_session():
        # Test 1: Create a session
        test_session = SessionHistory(
            session_id="test-init-session",
            task_type="test",
            message_count=1,
        )
        session.add(test_session)
        await session.commit()
        print("✅ Created test session")

        # Test 2: Create a feedback log
        test_feedback = FeedbackLog(
            session_id="test-init-session",
            error_type="test",
            category="initialization",
            severity="info",
            user_input="Database initialization test",
            system_response="Success",
        )
        session.add(test_feedback)
        await session.commit()
        print("✅ Created test feedback log")

        # Test 3: Query back
        from sqlalchemy import select

        stmt = select(SessionHistory).where(
            SessionHistory.session_id == "test-init-session"
        )
        result = await session.execute(stmt)
        retrieved = result.scalar_one_or_none()

        if retrieved:
            print("✅ Successfully retrieved test session")
            print(f"   Session ID: {retrieved.session_id}")
            print(f"   Created: {retrieved.created_at}")
        else:
            print("❌ Failed to retrieve test session")
            return False

    print("\n" + "=" * 60)
    print("\n✅ Database initialization complete!")
    return True


async def check_redis():
    """Check Redis connection."""
    print("\n🔴 Checking Redis connection...\n")
    print("=" * 60)

    if not REDIS_AVAILABLE:
        print("⚠️  Redis library not installed")
        print("   Run: pip install redis")
        return False

    import os

    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        print("⚠️  REDIS_URL not configured")
        print("   Using in-memory cache fallback")
        print("   For production, add REDIS_URL to .env")
        return False

    try:
        r = redis.from_url(redis_url, decode_responses=True)
        r.ping()
        print("✅ Redis connection successful")

        # Test set/get
        test_key = "test:init"
        r.setex(test_key, 60, "Hello from S1NGULARITY")
        value = r.get(test_key)
        print(f"✅ Redis set/get test passed: {value}")

        # Clean up
        r.delete(test_key)
        print("✅ Redis cleanup complete")

        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("   Using in-memory cache fallback")
        return False


async def seed_demo_data():
    """Seed demo data for testing."""
    if "--seed-demo" not in sys.argv:
        return

    print("\n🌱 Seeding demo data...\n")
    print("=" * 60)

    db_manager = get_db_manager()

    async for session in db_manager.get_session():
        # Demo session
        demo_session = SessionHistory(
            session_id="demo-session-1",
            task_type="resume_screening",
            message_count=5,
        )
        session.add(demo_session)

        # Demo feedback
        demo_feedback = FeedbackLog(
            session_id="demo-session-1",
            error_type="user_feedback",
            category="resume_analysis",
            severity="info",
            user_input="This match score seems accurate",
            system_response="Thank you for the feedback!",
        )
        session.add(demo_feedback)

        # Demo candidate interaction
        demo_interaction = CandidateInteraction(
            session_id="demo-session-1",
            candidate_email="john.doe@example.com",
            job_id="job-12345",
            match_score=85.0,
            skill_match=90.0,
            experience_match=80.0,
            green_flags=["Strong Python experience", "AWS certified"],
            yellow_flags=["No Go experience"],
            red_flags=[],
            action="shortlisted",
        )
        session.add(demo_interaction)

        # Demo job analysis
        demo_job = JobAnalysis(
            session_id="demo-session-1",
            job_id="job-12345",
            job_title="Senior Backend Engineer",
            company="TechCorp",
            core_skills=["Python", "AWS", "Docker", "Kubernetes"],
            nice_to_have=["Go", "Terraform"],
            tools_platforms=["GitHub", "Jenkins", "Datadog"],
            red_flags=["Unrealistic experience requirements"],
        )
        session.add(demo_job)

        await session.commit()

    print("✅ Demo data seeded")
    print("   - 1 demo session")
    print("   - 1 feedback log")
    print("   - 1 candidate interaction")
    print("   - 1 job analysis")


async def main():
    """Main initialization function."""
    print("\n" + "=" * 60)
    print("S1NGULARITY DATABASE INITIALIZATION")
    print("=" * 60 + "\n")

    # Initialize database
    db_success = await init_database()

    if not db_success:
        print("\n❌ Database initialization failed")
        sys.exit(1)

    # Check Redis
    await check_redis()

    # Seed demo data if requested
    await seed_demo_data()

    print("\n" + "=" * 60)
    print("\n✨ All systems ready!")
    print("\nNext steps:")
    print("1. Start the backend: uvicorn main:app --reload")
    print("2. Check health: curl http://localhost:8000/health")
    print("3. View API docs: http://localhost:8000/docs")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
