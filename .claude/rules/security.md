---
description: "Security rules following OWASP guidelines"
---

# Security Rules

## Input Validation
- Validate ALL user inputs with Pydantic models — no raw access to request body
- Constrain numeric inputs: `width/height` (256-1024), `guidance_scale` (1-30), `steps` (1-100)
- Sanitize text inputs: strip control characters, enforce max length on prompts (500 chars)
- Reject requests with unexpected fields (`model_config = ConfigDict(extra="forbid")`)

## Prompt Injection Prevention
- Filter prompts through blocklist (hate speech, violence, CSAM terms)
- Use regex + keyword matching — not LLM-based filtering (too slow per request)
- Log blocked prompts for audit (without storing full user details)

## NSFW Output Filtering
- Enable Stable Diffusion safety checker in pipeline
- Post-generation NSFW check as secondary filter
- Return 422 with generic error if content filtered — don't reveal filter details

## Rate Limiting
- IP-based rate limiting on generation endpoints (10 req/min default)
- Use sliding window algorithm with Redis
- Return 429 with `Retry-After` header

## API Security
- CORS restricted to specific origins (`ALLOWED_ORIGINS` env var)
- No secrets in code or logs — use environment variables
- Validate `Content-Type` header on POST requests
- Set security headers: `X-Content-Type-Options`, `X-Frame-Options`

## Dependencies
- Pin exact versions in lockfiles (`uv.lock`, `package-lock.json`)
- Run `uv audit` / `npm audit` in CI
