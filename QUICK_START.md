# ⚡ S1NGULARITY Quick Start

Your API keys have been configured! Here's how to get started immediately.

---

## ✅ Configuration Status

### ✅ **Configured**
- **OpenAI API Key**: ✓ Configured (GPT-4)
- **Tavily API Key**: ✓ Configured (Web Search)
- **LLM Provider**: Set to `openai`

### ⚠️ **Optional (Not Yet Configured)**
- **JobDiva API**: Using placeholder values (add real credentials to test ATS integration)
- **Anthropic API**: Not configured (add if you want to use Claude instead of GPT-4)

---

## 🚀 Start the Application (3 Options)

### **Option 1: Quick Start Script (Recommended)**

```bash
cd /home/user/arkv2.1
./start.sh
```

Choose option 1 (Docker) or option 2 (Local) when prompted.

---

### **Option 2: Manual Backend Only**

```bash
cd /home/user/arkv2.1

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Initialize database
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

---

### **Option 3: Full Stack (Backend + Frontend)**

**Terminal 1 - Backend:**
```bash
cd /home/user/arkv2.1
./start.sh
# Choose option 2 (Local Development)
```

**Terminal 2 - Frontend:**
```bash
cd /home/user/arkv2.1/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Frontend will be available at**: http://localhost:3000

---

## 🧪 Test Your Setup

### 1. **Test Backend Health**

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": true,
    "jobdiva": false,  // Will be false until JobDiva credentials added
    "llm": true,       // Should be true (OpenAI)
    "web_search": true // Should be true (Tavily)
  }
}
```

### 2. **Test Web Search (Anti-Hallucination)**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the salary for a Senior DevOps Engineer in Austin?",
    "task_type": "salary_research"
  }'
```

**Expected**: Real salary data with sources (from Tavily)

### 3. **Test Frontend**

1. Open http://localhost:3000 in browser
2. Type: "What is the market rate for a Data Engineer in San Francisco?"
3. Press Enter

**Expected**:
- Response with real salary data
- Sources listed with clickable links
- "Connected" status in header

---

## 📁 What You Have

```
✅ Backend API (FastAPI)
✅ Database models (PostgreSQL/SQLite)
✅ Redis caching (optional)
✅ Web search integration (Tavily)
✅ LLM integration (OpenAI GPT-4)
✅ Intelligent module loading
✅ Frontend UI (Next.js 14)
✅ Docker configuration
✅ Deployment guides
```

---

## 🔑 Add JobDiva Credentials (Optional)

To test the full ATS integration:

1. **Edit .env file:**
   ```bash
   nano .env
   ```

2. **Update these lines:**
   ```bash
   JOBDIVA_CLIENT_ID=your_actual_client_id
   JOBDIVA_USERNAME=your_actual_username
   JOBDIVA_PASSWORD=your_actual_password
   ```

3. **Restart backend:**
   ```bash
   # Press Ctrl+C to stop
   # Then restart with ./start.sh or uvicorn
   ```

---

## 🎯 Demo the Key Features

### **1. Salary Research (Proves No Hallucinations)**

**User Question:**
> "What's the salary for a Senior React Developer in New York?"

**What Happens:**
1. Backend detects `salary_research` task type
2. Loads web-search module
3. Calls Tavily API (real-time Google search)
4. Returns actual data with sources

**Expected Output:**
```
💰 Senior React Developer in New York

Salary Range: $130,000 - $180,000
Average: $155,000

Sources:
• Glassdoor: $150k average
• Indeed: $160k average
• Salary.com: $152k median

Last updated: [current date]
```

---

### **2. JD Analysis (Proves Explainability)**

**User Action:**
> Upload a job description and ask "Break this down"

**What Happens:**
1. Backend loads `jd-intelligence` module
2. Extracts skills (core vs nice-to-have)
3. Detects red flags
4. Generates layman's guide

**Expected Output:**
```
📋 Job Breakdown

Core Skills (MUST HAVE):
✓ Python (5+ years) - Backend development
✓ AWS (3+ years) - Cloud infrastructure
✓ Docker/Kubernetes - Container orchestration

Nice to Have:
• Go programming
• Terraform experience

⚠️ Red Flags Detected:
• Requires 10 years React experience (React is only 11 years old)
• Junior role but wants 7+ years experience

Layman's Guide:
"This role is like a 'Cloud Developer' who builds backend systems..."
```

---

### **3. Resume Screening (Proves Bias Detection)**

**User Action:**
> Upload resume and click "Screen Resume"

**What Happens:**
1. Backend loads `resume-analysis` + `bias-detection` modules
2. Calculates match scores
3. Flags potential bias
4. Provides recommendations

**Expected Output:**
```
📊 Candidate Analysis

Match Score: 85%
✓ Skill Match: 90%
✓ Experience Match: 80%

Green Flags:
✓ Strong Python background (8 years)
✓ AWS certified
✓ Led team of 5 engineers

Yellow Flags:
⚠ No Go experience (required skill)
⚠ Gap in employment (2021-2022)

🛡️ Bias Check: PASSED
No age, gender, or ethnicity markers detected
```

---

## 🚀 Deploy to Production

When ready to deploy:

1. **Read DEPLOYMENT_GUIDE.md**
   ```bash
   cat DEPLOYMENT_GUIDE.md
   ```

2. **Deploy Backend to Railway** (15 min)
   - https://railway.app
   - Auto-detects Docker
   - Adds PostgreSQL + Redis
   - Cost: $5/mo

3. **Deploy Frontend to Vercel** (10 min)
   - https://vercel.com
   - Auto-detects Next.js
   - Free tier
   - Cost: $0

**Total Production Cost**: ~$25/mo (includes LLM usage)

---

## 🐛 Troubleshooting

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Issue: "Database connection failed"

**Solution:**
```bash
# Using SQLite (default):
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

# Using Docker PostgreSQL:
docker-compose up -d postgres
```

### Issue: Frontend shows "Disconnected"

**Solution:**
```bash
# Check NEXT_PUBLIC_API_URL in frontend/.env.local
cat frontend/.env.local

# Should show:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Restart frontend
cd frontend
npm run dev
```

---

## 📚 Documentation

- **Main README**: `README.md`
- **Frontend README**: `frontend/README.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🎉 You're Ready!

Your S1NGULARITY platform is configured and ready to run.

**Next Step**: Run `./start.sh` and visit http://localhost:3000

Questions? Check the READMEs or open an issue on GitHub.

---

**Built with ❤️ • Deployed in minutes • Running on AI**
