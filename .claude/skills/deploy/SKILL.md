---
name: deploy
description: "Deployment checklist for HuggingFace Spaces (backend) and Vercel (frontend)"
---

# Deploy

## Backend → HuggingFace Spaces

1. **Prepare Dockerfile** — ensure `backend/Dockerfile` is correct
2. **Create HF Space** — type: Docker, hardware: ZeroGPU (free, 5 GPU hrs/mo)
3. **Set environment variables** in Space settings:
   - `MODEL_ID`, `REDIS_URL`, `DEVICE=cuda`, `STORAGE_PATH=/tmp/generated`
4. **Push to Space**:
   ```bash
   cd backend
   git remote add hf https://huggingface.co/spaces/username/text-to-image-backend
   git subtree push --prefix backend hf main
   ```
5. **Verify** — check Space logs, hit `/health` endpoint

## Frontend → Vercel

1. **Connect GitHub repo** to Vercel
2. **Set root directory** to `frontend/`
3. **Set environment variables**:
   - `NEXT_PUBLIC_API_URL` → HF Spaces backend URL
4. **Deploy** — auto on push to `main`
5. **Verify** — check deployment logs, test image generation flow

## Post-Deploy Checklist
- [ ] CORS configured for Vercel domain
- [ ] Health check returns 200
- [ ] Image generation end-to-end works
- [ ] Error states display correctly
- [ ] Rate limiting functional
- [ ] NSFW filter active
