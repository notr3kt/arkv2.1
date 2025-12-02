# Deploy Frontend to Vercel

**Quick guide to deploy S1NGULARITY frontend to Vercel**

---

## Step 1: Push to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare frontend for Vercel deployment"
git push origin main
```

---

## Step 2: Deploy to Vercel

### Option A: Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Click **"Import Project"**
3. Select your GitHub repository: `notr3kt/arkv2.1`
4. **Root Directory**: Set to `frontend`
5. **Framework Preset**: Next.js (auto-detected)
6. Click **"Deploy"**

### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel
```

---

## Step 3: Set Environment Variables

After deployment, add environment variables in Vercel:

1. Go to your project in Vercel dashboard
2. Click **Settings** → **Environment Variables**
3. Add these variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://arkv21-production.up.railway.app` | Production |
| `NEXT_PUBLIC_ENABLE_PDF_UPLOAD` | `true` | Production |
| `NEXT_PUBLIC_ENABLE_WEB_SEARCH` | `true` | Production |
| `NEXT_PUBLIC_ENABLE_BIAS_DETECTION` | `true` | Production |

4. Click **"Redeploy"** to apply changes

---

## Step 4: Update Backend CORS

Add your Vercel URL to Railway backend:

1. Go to Railway dashboard
2. Open your backend service
3. Go to **Settings** → **Variables**
4. Update `CORS_ORIGINS` to include your Vercel URL:

```
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

**Note:** Replace `your-app.vercel.app` with your actual Vercel domain.

5. Railway will auto-redeploy

---

## Step 5: Test Deployment

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Check if health indicator shows "Connected"
3. Try sending a chat message
4. Verify it connects to Railway backend

---

## Troubleshooting

### Issue: "Failed to connect to backend"

**Solution:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check Railway backend is running: `https://arkv21-production.up.railway.app/health`
- Verify CORS_ORIGINS includes your Vercel URL

### Issue: "CORS error in console"

**Solution:**
- Add your Vercel domain to `CORS_ORIGINS` in Railway
- Make sure to redeploy Railway after changing environment variables

### Issue: "Build fails in Vercel"

**Solution:**
```bash
# Test build locally first
cd frontend
npm install
npm run build
```

---

## Custom Domain (Optional)

1. Go to Vercel project → **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update `CORS_ORIGINS` in Railway to include custom domain

---

## Automatic Deployments

Once connected to GitHub:
- **Push to main** → Auto-deploy to production
- **Pull requests** → Auto-generate preview URLs
- **Rollback** → One-click rollback in Vercel dashboard

---

**Your Frontend URL:** Will be `https://[project-name]-[hash].vercel.app`

**Backend URL:** `https://arkv21-production.up.railway.app`
