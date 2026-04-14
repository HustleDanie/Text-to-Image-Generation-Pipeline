---
description: "REST API design conventions for the backend"
paths:
  - "backend/app/routes/**"
---

# API Design Rules

## Async Job Pattern
Generation takes 5-30 seconds — never handle synchronously.

```
1. POST /api/generate       → 202 Accepted {"job_id": "abc-123"}
2. GET  /api/status/{id}    → 200 {"status": "processing", "progress": 45}
                             → 200 {"status": "completed", "image_url": "/api/images/abc-123"}
                             → 200 {"status": "failed", "error": "Content filtered"}
3. GET  /api/images/{id}    → 200 (image/png binary)
```

## Endpoints
- Use plural nouns: `/api/models`, `/api/images`
- Use HTTP methods correctly: GET (read), POST (create), DELETE (remove)
- Return appropriate status codes: 200, 201, 202, 400, 404, 422, 429, 500

## Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Width must be between 256 and 1024",
    "details": [{"field": "width", "issue": "Value 2048 exceeds maximum of 1024"}]
  }
}
```

## Pagination (for gallery/models endpoints)
Use cursor-based pagination: `?cursor=xxx&limit=20`
Response: `{"items": [...], "next_cursor": "yyy", "has_more": true}`

## Content Types
- JSON for API requests/responses: `application/json`
- Binary for images: `image/png`
- Validate `Content-Type` header on incoming requests
