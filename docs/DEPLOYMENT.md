# Deployment Guide

## Backend → HuggingFace Spaces (ZeroGPU)

### 1. Create a HuggingFace Space

1. Go to https://huggingface.co/new-space
2. Choose **Docker** as the SDK
3. Select **ZeroGPU** hardware (free, 5 GPU hours/month)
4. Name your space (e.g., `text-to-image-backend`)

### 2. Configure Environment Variables

In your Space Settings → Variables:
- `MODEL_ID`: `stabilityai/stable-diffusion-xl-base-1.0`
- `REDIS_URL`: Use a free Redis provider (Upstash, Redis Cloud) or run Redis as a sidecar
- `DEVICE`: `cuda`
- `STORAGE_PATH`: `/tmp/generated`
- `ALLOWED_ORIGINS`: Your Vercel frontend URL

### 3. Deploy

**Option A: GitHub Actions (automated)**
Set these secrets in your GitHub repo:
- `HF_TOKEN`: Your HuggingFace API token
- `HF_SPACE_ID`: `username/text-to-image-backend`

Push to `main` — the `.github/workflows/deploy-backend.yml` handles deployment.

**Option B: Manual**
```bash
cd backend
git init
git add .
git commit -m "Deploy"
git remote add hf https://huggingface.co/spaces/username/text-to-image-backend
git push hf main --force
```

## Frontend → Vercel

### 1. Connect Repository

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Set **Root Directory** to `frontend`
4. Framework will auto-detect as Next.js

### 2. Configure Environment Variables

In Vercel Project Settings → Environment Variables:
- `NEXT_PUBLIC_API_URL`: Your HuggingFace Spaces backend URL (e.g., `https://username-text-to-image-backend.hf.space`)

### 3. Deploy

**Option A: Auto-deploy**
Vercel auto-deploys on push to `main`. The `.github/workflows/deploy-frontend.yml` provides additional control.

Set Vercel secrets in GitHub:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

**Option B: Manual**
```bash
cd frontend
npx vercel --prod
```

## Post-Deployment Checklist

- [ ] Backend `/health` returns 200
- [ ] Frontend loads and displays UI
- [ ] CORS allows frontend domain
- [ ] Image generation works end-to-end
- [ ] Rate limiting is functional
- [ ] NSFW filter blocks inappropriate prompts
- [ ] Error states display correctly in UI
- [ ] Generated images load in gallery

## Free Tier Limits

| Service | Limit |
|---------|-------|
| HuggingFace ZeroGPU | 5 GPU hours/month |
| Vercel | 100GB bandwidth, 1000 builds/month |
| Redis (Upstash free) | 10,000 commands/day |

## Monitoring

- **Backend**: HuggingFace Spaces logs (Settings → Logs)
- **Frontend**: Vercel deployment logs + Analytics
- **Errors**: Structured JSON logs in backend, browser console in frontend
