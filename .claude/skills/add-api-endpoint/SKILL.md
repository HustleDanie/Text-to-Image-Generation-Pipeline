---
name: add-api-endpoint
description: "Step-by-step guide to add a new FastAPI endpoint with schema, route, tests, and docs"
---

# Add API Endpoint

## Steps

1. **Define schemas** in `backend/app/schemas/`
   - Request model (Pydantic v2 with Field descriptions)
   - Response model (with example values)
   - Use `Annotated[type, Field(...)]` for complex validations

2. **Create route** in `backend/app/routes/`
   - `async def` handler
   - Type the response: `response_model=YourResponse`
   - Set `status_code` (201 for creation, 202 for async jobs)
   - Add dependency injection for shared services

3. **Register route** in `backend/app/main.py`
   - `app.include_router(router, prefix="/api", tags=["tag"])`

4. **Write tests** in `backend/tests/`
   - Happy path test
   - Validation error test (missing fields, invalid values)
   - Edge case tests (empty strings, boundary values)
   - Use `httpx.AsyncClient` with `ASGITransport`

5. **Verify**
   - `uv run ruff check backend/`
   - `uv run pytest backend/tests/ -x -q`
   - Check `/docs` for OpenAPI documentation
