# 🗄️ S1NGULARITY Database Guide

**Why You Need a Database: Real-World Memory**

Without a database, S1NGULARITY is a calculator - it forgets everything the moment you close the tab. With a database, it becomes a **product** that remembers candidates, logs compliance issues, and saves you money on API calls.

---

## 🧠 What the Database Stores

### **1. Session History** (`session_history` table)
**Why**: When a recruiter says "Compare him to the previous candidate," the AI needs to remember who that was.

**Example**:
```json
{
  "session_id": "session-abc123",
  "task_type": "resume_screening",
  "message_count": 15,
  "created_at": "2024-12-02T10:00:00Z",
  "last_active": "2024-12-02T10:45:00Z"
}
```

### **2. Feedback Logs** (`feedback_logs` table)
**Why**: Your `s1ngularity-governance-resilience.json` requires logging "Who accessed what data when" for EEOC compliance.

**Example**:
```json
{
  "session_id": "session-abc123",
  "error_type": "bias_detected",
  "category": "resume_analysis",
  "severity": "warning",
  "user_input": "Screened candidate John Doe",
  "context": {"flagged_terms": ["young", "recent grad"]},
  "timestamp": "2024-12-02T10:30:00Z"
}
```

### **3. Candidate Interactions** (`candidate_interactions` table)
**Why**: Store analysis results so you can say "Show me all candidates with 80%+ match for this role."

**Example**:
```json
{
  "candidate_email": "jane.smith@example.com",
  "job_id": "job-12345",
  "match_score": 85,
  "skill_match": 90,
  "experience_match": 80,
  "green_flags": ["Strong Python", "AWS certified"],
  "yellow_flags": ["No Go experience"],
  "action": "shortlisted",
  "timestamp": "2024-12-02T10:35:00Z"
}
```

### **4. Redis Cache** (separate from PostgreSQL)
**Why**: Your `jobdiva_auth.py` uses Redis to cache authentication tokens. Without it, you'll spam the JobDiva API for a new token with every request.

**Example**:
```
auth_token:jobdiva = "Bearer xyz123..."
web_search:devops_salary_austin = "{results: [...]}"
```

---

## 🚂 Option 1: Railway (Easiest, $5/mo)

### **Step 1: Create Railway Project**

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `arkv2.1` repo

### **Step 2: Add PostgreSQL**

```bash
# In Railway dashboard:
1. Click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-generates:
   - DATABASE_URL
   - Database credentials
```

**Copy the DATABASE_URL** (looks like):
```
postgresql://postgres:password@hostname.railway.app:5432/railway
```

### **Step 3: Add Redis**

```bash
# In Railway dashboard:
1. Click "+ New"
2. Select "Database" → "Redis"
3. Railway auto-generates:
   - REDIS_URL
```

**Copy the REDIS_URL** (looks like):
```
redis://default:password@hostname.railway.app:6379
```

### **Step 4: Update Your .env**

```bash
# Edit /home/user/arkv2.1/.env
DATABASE_URL=postgresql+asyncpg://postgres:password@hostname.railway.app:5432/railway
REDIS_URL=redis://default:password@hostname.railway.app:6379
```

**Note**: Change `postgresql://` to `postgresql+asyncpg://` for async support!

### **Step 5: Initialize Database**

```bash
cd /home/user/arkv2.1
python3 init_db.py
```

**Expected Output**:
```
🗄️  Initializing S1NGULARITY Database...
============================================================
📋 Creating database tables...
✅ Tables created successfully

🔍 Verifying tables...
   Found 5 tables:
   ✓ session_history
   ✓ feedback_logs
   ✓ candidate_interactions
   ✓ job_analyses
   ✓ analytics_metrics

🧪 Testing database operations...
✅ Created test session
✅ Created test feedback log
✅ Successfully retrieved test session

🔴 Checking Redis connection...
✅ Redis connection successful
✅ Redis set/get test passed

✨ All systems ready!
```

---

## 🐘 Option 2: Supabase (Free Tier, Managed PostgreSQL)

### **Step 1: Create Supabase Project**

1. Go to https://supabase.com
2. Sign up
3. Click "New Project"
4. Choose a name, region, and password

### **Step 2: Get Connection String**

```bash
# In Supabase dashboard:
1. Go to "Settings" → "Database"
2. Find "Connection string" section
3. Choose "Connection pooling" (recommended)
4. Copy the URI
```

**Format**:
```
postgresql://postgres.xxxxx:[password]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### **Step 3: Convert to AsyncPG**

```bash
# Change:
postgresql://...
# To:
postgresql+asyncpg://...
```

### **Step 4: Update .env**

```bash
DATABASE_URL=postgresql+asyncpg://postgres.xxxxx:[password]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### **Step 5: Add Redis (Upstash)**

Supabase doesn't include Redis, so use Upstash:

1. Go to https://upstash.com
2. Create free Redis database
3. Copy the connection string

```bash
REDIS_URL=rediss://default:password@endpoint.upstash.io:6379
```

---

## 🌊 Option 3: Neon (Free Tier, Serverless PostgreSQL)

### **Step 1: Create Neon Project**

1. Go to https://neon.tech
2. Sign up with GitHub
3. Click "Create Project"
4. Choose a name and region

### **Step 2: Get Connection String**

```bash
# In Neon dashboard:
1. Click on your project
2. Go to "Connection Details"
3. Copy "Connection string"
```

**Format**:
```
postgresql://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require
```

### **Step 3: Convert to AsyncPG**

```bash
postgresql+asyncpg://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require
```

### **Step 4: Update .env**

```bash
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.aws.neon.tech/neondb?sslmode=require
```

---

## 🧪 Test Your Database Connection

### **Method 1: Run Init Script**

```bash
cd /home/user/arkv2.1
pip install -r requirements.txt
python3 init_db.py
```

### **Method 2: Manual Test**

```bash
cd /home/user/arkv2.1
python3 << EOF
import asyncio
from database import get_db_manager

async def test():
    db = get_db_manager()
    await db.create_tables()
    print("✅ Database tables created!")

asyncio.run(test())
EOF
```

### **Method 3: Via API**

```bash
# Start backend
uvicorn main:app --reload &

# Wait for startup
sleep 5

# Test analytics endpoint (proves database works)
curl http://localhost:8000/analytics/summary
```

**Expected Response**:
```json
{
  "total_sessions": 1,
  "total_messages": 1,
  "total_candidate_interactions": 0,
  "average_match_score": 0.0,
  "total_feedback_logs": 1,
  "feedback_by_type": {
    "test": 1
  },
  "database_status": "operational",
  "persistence_enabled": true
}
```

---

## 🔍 Prove the Database "Remembers"

### **Demo 1: Session Persistence**

```bash
# Start backend
uvicorn main:app --reload &

# Send first message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the salary for a DevOps Engineer?",
    "session_id": "demo-session-1"
  }'

# Send second message in SAME session
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How about in New York?",
    "session_id": "demo-session-1"
  }'

# Check if session was remembered
curl http://localhost:8000/sessions/demo-session-1
```

**Expected**: Session shows `message_count: 2` - proves memory!

### **Demo 2: List All Sessions**

```bash
curl http://localhost:8000/sessions
```

**Expected**:
```json
{
  "sessions": [
    {
      "session_id": "demo-session-1",
      "task_type": "salary_research",
      "message_count": 2,
      "created_at": "2024-12-02T10:00:00Z",
      "last_active": "2024-12-02T10:05:00Z"
    }
  ],
  "total": 1
}
```

### **Demo 3: Analytics Dashboard**

```bash
curl http://localhost:8000/analytics/summary
```

**Expected**:
```json
{
  "total_sessions": 5,
  "total_messages": 37,
  "average_match_score": 82.5,
  "database_status": "operational"
}
```

This proves your system is storing and aggregating data!

---

## 📊 Database Schema Reference

### **Tables Created**

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `session_history` | Track conversations | session_id, message_count, task_type |
| `feedback_logs` | Compliance & errors | error_type, severity, timestamp |
| `candidate_interactions` | Candidate analysis | match_score, flags, action |
| `job_analyses` | Parsed JDs | core_skills, red_flags, boolean_query |
| `analytics_metrics` | Aggregate insights | metric_name, metric_value, period |

### **Relationships**

```
session_history (1) → (many) feedback_logs
session_history (1) → (many) candidate_interactions
session_history (1) → (many) job_analyses
```

---

## 🔧 Troubleshooting

### Issue: "asyncpg.exceptions.InvalidPasswordError"

**Cause**: Wrong database credentials

**Solution**:
```bash
# Check your DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Test connection manually
psql "postgresql://user:password@host:5432/db"
```

### Issue: "tables already exist"

**Cause**: Running init script multiple times

**Solution**:
```bash
# Reset database (DELETES ALL DATA)
python3 init_db.py --reset
```

### Issue: "Redis connection failed"

**Cause**: REDIS_URL not configured or wrong

**Solution**:
```bash
# System still works without Redis (uses in-memory fallback)
# To fix, check REDIS_URL in .env

# Test Redis manually
redis-cli -u redis://your-redis-url ping
```

### Issue: "No module named 'asyncpg'"

**Solution**:
```bash
pip install asyncpg psycopg2-binary redis
```

---

## 💰 Cost Comparison

| Provider | PostgreSQL | Redis | Total/Month |
|----------|-----------|-------|-------------|
| **Railway** | $5 | Included | **$5** |
| **Supabase + Upstash** | Free | Free | **$0** |
| **Neon + Upstash** | Free | Free | **$0** |

**Recommendation**: Start with Supabase or Neon (free), migrate to Railway when you need more power.

---

## 🚀 Next Steps

1. **Choose a provider** (Railway/Supabase/Neon)
2. **Get DATABASE_URL and REDIS_URL**
3. **Update .env file**
4. **Run**: `python3 init_db.py`
5. **Test**: `curl http://localhost:8000/analytics/summary`
6. **Deploy**: See `DEPLOYMENT_GUIDE.md`

---

## 🎯 What This Enables

With a real database, you can now:

✅ **Remember conversations** - "Compare to previous candidate"
✅ **Log compliance** - EEOC audit trails
✅ **Cache expensive data** - Save money on API calls
✅ **Build analytics** - "Average match score this week"
✅ **Track feedback** - "How many hallucinations did we catch?"
✅ **Support multi-user** - Each recruiter gets their own history

**Your system is no longer a calculator. It's a product with memory.**

---

**Questions? Check the troubleshooting section or open a GitHub issue.**

**Built with ❤️ • Persistence enabled • Real-world ready**
