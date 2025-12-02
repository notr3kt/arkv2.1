# 🚀 S1NGULARITY Deployment Guide

**Get your AI recruiting platform live in under 30 minutes**

This guide shows you how to deploy S1NGULARITY to production using free/low-cost cloud services.

---

## 📋 Prerequisites Checklist

Before deploying, ensure you have:

### ✅ **Required API Keys**

| Service | Purpose | Where to Get | Cost |
|---------|---------|--------------|------|
| **Anthropic API** | LLM reasoning (Claude 3.5 Sonnet) | https://console.anthropic.com | ~$20/mo |
| **Tavily API** | Web search (anti-hallucination) | https://tavily.com | Free tier |
| **JobDiva API** | ATS integration | Your JobDiva admin | Custom |

### ✅ **Optional API Keys**

| Service | Purpose | Where to Get | Cost |
|---------|---------|--------------|------|
| OpenAI API | Alternative LLM (GPT-4) | https://platform.openai.com | ~$20/mo |
| LlamaParse | Advanced resume parsing | https://cloud.llamaindex.ai | Free tier |
| Sentry | Error tracking | https://sentry.io | Free tier |

### ✅ **Cloud Accounts**

- **Railway.app** (Backend hosting) - https://railway.app
- **Vercel** (Frontend hosting) - https://vercel.com
- **GitHub** (Code repository) - https://github.com

All offer **free tiers** sufficient for testing and small-scale deployment.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                         Internet                          │
└───────────────────┬──────────────────┬───────────────────┘
                    │                  │
        ┌───────────▼────────┐  ┌──────▼──────────┐
        │   Vercel (Free)    │  │ Railway ($5/mo) │
        │                    │  │                 │
        │  Next.js Frontend  │──▶ FastAPI Backend │
        │  (s1ngularity.app) │  │ + PostgreSQL    │
        │                    │  │ + Redis         │
        └────────────────────┘  └─────────┬───────┘
                                          │
                    ┌─────────────────────┴─────────────────┐
                    │                                       │
            ┌───────▼────────┐                  ┌──────────▼─────────┐
            │ Anthropic API  │                  │   Tavily API       │
            │ (Claude 3.5)   │                  │ (Web Search)       │
            └────────────────┘                  └────────────────────┘
```

---

## 🔧 Step 1: Prepare Your Code

### 1.1 Ensure Git Repository is Updated

```bash
cd /home/user/arkv2.1

# Check current branch
git branch

# Should see: claude/ai-agent-infrastructure-01TKGjew8uvMcsiEr7svEUoV

# Verify commits
git log --oneline -5
```

### 1.2 Create Production Environment File

```bash
# Create production .env (DO NOT COMMIT THIS)
cp .env.example .env.production

# Edit with your actual keys
nano .env.production
```

**Required variables:**
```bash
# LLM Provider
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic

# Web Search (CRITICAL - Prevents hallucinations)
TAVILY_API_KEY=tvly-your-key-here

# JobDiva ATS
JOBDIVA_CLIENT_ID=your-client-id
JOBDIVA_USERNAME=your-username
JOBDIVA_PASSWORD=your-password
JOBDIVA_BASE_URL=https://api.jobdiva.com

# Database (Railway will provide this)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Redis (Railway will provide this)
REDIS_URL=redis://host:6379/0

# Security
JWT_SECRET_KEY=$(openssl rand -hex 32)
```

---

## 🚂 Step 2: Deploy Backend to Railway

### 2.1 Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your repository

### 2.2 Create New Project

```bash
# From Railway Dashboard:
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose "notr3kt/arkv2.1"
4. Select branch: claude/ai-agent-infrastructure-01TKGjew8uvMcsiEr7svEUoV
```

### 2.3 Add PostgreSQL Database

```bash
# In Railway project:
1. Click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-generates DATABASE_URL
```

### 2.4 Add Redis Cache

```bash
# In Railway project:
1. Click "+ New"
2. Select "Database" → "Redis"
3. Railway auto-generates REDIS_URL
```

### 2.5 Configure Backend Service

```bash
# In Railway project:
1. Click on your service (arkv2.1)
2. Go to "Variables" tab
3. Click "Raw Editor"
4. Paste your .env.production content
5. Click "Add Variables"
```

**Railway will automatically provide:**
- `DATABASE_URL`
- `REDIS_URL`
- `PORT` (default: 8000)

**You need to add:**
```bash
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
JOBDIVA_CLIENT_ID=...
JOBDIVA_USERNAME=...
JOBDIVA_PASSWORD=...
JOBDIVA_BASE_URL=https://api.jobdiva.com
LLM_PROVIDER=anthropic
JWT_SECRET_KEY=<generate with openssl rand -hex 32>
```

### 2.6 Configure Build Settings

```bash
# Railway should auto-detect:
Build Command: docker build -t s1ngularity .
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

# If not, go to "Settings" → "Build" and set manually
```

### 2.7 Deploy

```bash
# Railway automatically deploys on:
1. First setup
2. Every git push to your branch

# Check deployment logs:
Railway Dashboard → Your Service → "Deployments" tab
```

### 2.8 Get Your Backend URL

```bash
# In Railway:
1. Click on your service
2. Go to "Settings" → "Networking"
3. Click "Generate Domain"

# You'll get a URL like:
# https://s1ngularity-production.up.railway.app
```

### 2.9 Verify Backend

```bash
# Test health endpoint
curl https://your-railway-url.railway.app/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": true,
    "jobdiva": true,
    "llm": true,
    "web_search": true
  }
}
```

---

## ▲ Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your repository

### 3.2 Import Project

```bash
# From Vercel Dashboard:
1. Click "Add New..." → "Project"
2. Import "notr3kt/arkv2.1"
3. Select branch: claude/ai-agent-infrastructure-01TKGjew8uvMcsiEr7svEUoV
```

### 3.3 Configure Build Settings

```bash
# Vercel should auto-detect Next.js, but verify:

Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install

# Node.js Version: 18.x (in Settings → General)
```

### 3.4 Add Environment Variables

```bash
# In Vercel:
1. Go to "Settings" → "Environment Variables"
2. Add the following:

Variable Name: NEXT_PUBLIC_API_URL
Value: https://your-railway-url.railway.app
Environment: Production, Preview, Development

# Click "Add"
```

### 3.5 Deploy

```bash
# Vercel automatically deploys

# Check status:
Vercel Dashboard → Your Project → "Deployments"
```

### 3.6 Get Your Frontend URL

```bash
# Vercel provides:
Production: https://s1ngularity.vercel.app
Preview: https://s1ngularity-git-branch-name.vercel.app
```

### 3.7 Verify Frontend

```bash
# Visit your URL in browser
https://your-app.vercel.app

# Should see:
- S1NGULARITY header
- Chat interface
- PDF upload area
- Action buttons
- "Connected" status indicator
```

---

## 🔒 Step 4: Configure CORS

### 4.1 Update Backend CORS Settings

```bash
# In Railway environment variables, add:
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-preview.vercel.app

# Railway will auto-redeploy
```

---

## 🎯 Step 5: Test the Full Stack

### 5.1 Test Health Check

```bash
# Open browser console (F12)
# Go to your Vercel URL

# Check Network tab:
GET https://your-railway-url.railway.app/health
Status: 200
Response: {"status": "healthy", ...}
```

### 5.2 Test Chat

```bash
# In your deployed frontend:
1. Type: "What is the salary for a Senior DevOps Engineer in Austin?"
2. Press Enter
3. Wait for response

# Should show:
- Real salary data (from Tavily API)
- Sources with clickable links
- No hallucinated numbers
```

### 5.3 Test Resume Upload

```bash
1. Drag & drop a PDF resume
2. Wait for upload complete
3. Click "Screen Resume" action button
4. See analysis in right sidebar

# Should show:
- Match score
- Green/yellow/red flags
- Bias detection (if applicable)
```

---

## 💰 Cost Breakdown

### Monthly Costs (Production)

| Service | Plan | Cost |
|---------|------|------|
| **Railway** (Backend + DB + Redis) | Hobby | $5/mo |
| **Vercel** (Frontend) | Free | $0 |
| **Anthropic API** (Claude) | Usage | ~$20/mo |
| **Tavily API** (Web Search) | Free Tier | $0 |
| **Total** | | **~$25/mo** |

### Usage Estimates

- **Claude API**: ~$0.015 per 1K tokens
  - Average conversation: 5K tokens = $0.075
  - 250 conversations/mo = ~$20
- **Tavily API**: Free tier = 1,000 searches/mo
  - Upgrade: $29/mo for 10K searches

---

## 📊 Monitoring & Observability

### Railway Logs

```bash
# View logs:
Railway Dashboard → Your Service → "Logs" tab

# Filter by:
- Info
- Warning
- Error
- Critical
```

### Vercel Analytics

```bash
# Enable free analytics:
Vercel Dashboard → Your Project → "Analytics" tab

# Shows:
- Page views
- Response times
- Error rates
```

### Sentry (Optional)

```bash
# Add to Railway env vars:
SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456
SENTRY_ENVIRONMENT=production

# Add to Vercel env vars:
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456

# Now get:
- Real-time error tracking
- Stack traces
- User context
```

---

## 🔧 Troubleshooting

### Issue: Backend Won't Start

**Symptoms:**
- Railway shows "Crashed" status
- Logs show "Module not found"

**Solution:**
```bash
# Check Railway logs
# Common issues:
1. Missing requirements.txt dependencies
   → Add missing package to requirements.txt
2. Database connection failed
   → Verify DATABASE_URL is set
3. Python version mismatch
   → Railway uses Python 3.11 (check Dockerfile)
```

### Issue: Frontend Shows "Disconnected"

**Symptoms:**
- Red indicator in header
- Chat doesn't work

**Solution:**
```bash
# Check NEXT_PUBLIC_API_URL
Vercel → Settings → Environment Variables

# Should be:
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app

# NOT:
❌ http://localhost:8000
❌ Missing https://
```

### Issue: CORS Errors

**Symptoms:**
- Browser console shows "CORS policy blocked"
- Network requests fail with 403

**Solution:**
```bash
# Add to Railway env vars:
CORS_ORIGINS=https://your-app.vercel.app

# Redeploy backend
```

### Issue: Salary Search Returns "Error"

**Symptoms:**
- Chat shows "Web search failed"
- No salary data

**Solution:**
```bash
# Check Tavily API key
Railway → Variables → TAVILY_API_KEY

# Test manually:
curl -X GET "https://api.tavily.com/search" \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"query": "DevOps salary Austin"}'
```

---

## 🚀 Going to Production

### Custom Domain

#### Backend (Railway)

```bash
# Railway:
1. Settings → Networking → Custom Domain
2. Add: api.yourdomain.com
3. Update DNS CNAME: points to railway.app
4. Wait for SSL certificate (auto-generated)
```

#### Frontend (Vercel)

```bash
# Vercel:
1. Settings → Domains
2. Add: yourdomain.com
3. Update DNS:
   - A record: 76.76.21.21
   - CNAME: cname.vercel-dns.com
4. SSL auto-generated
```

### Environment Variables Update

```bash
# Railway:
CORS_ORIGINS=https://yourdomain.com

# Vercel:
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Scale Up

#### Railway

```bash
# Settings → Resources:
- RAM: 1GB → 2GB ($10/mo → $20/mo)
- CPU: 1vCPU → 2vCPU
- Autoscaling: Enable (scales based on traffic)
```

#### Vercel

```bash
# Pro plan ($20/mo) unlocks:
- Faster builds
- More bandwidth
- Priority support
- Team collaboration
```

---

## 📚 Additional Resources

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Anthropic Docs**: https://docs.anthropic.com
- **Tavily Docs**: https://docs.tavily.com

---

## ✅ Deployment Checklist

- [ ] All API keys obtained
- [ ] Railway account created
- [ ] Backend deployed to Railway
- [ ] PostgreSQL database added
- [ ] Redis cache added
- [ ] Backend health check passes
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] NEXT_PUBLIC_API_URL configured
- [ ] Frontend loads successfully
- [ ] CORS configured
- [ ] End-to-end chat test passes
- [ ] Resume upload test passes
- [ ] Salary search test passes (real data from Tavily)
- [ ] Monitoring enabled (Sentry optional)

---

## 🎉 Success!

Your S1NGULARITY platform is now live! Share it with:

- **Recruiters**: https://your-app.vercel.app
- **Developers**: https://your-api.railway.app/docs (Swagger UI)
- **LinkedIn**: Post about your AI recruiting platform
- **Investors**: Show the demo with real-time salary validation

---

**Questions? Issues? Open a GitHub Issue or contact support.**

**Built with ❤️ and deployed in < 30 minutes.**
