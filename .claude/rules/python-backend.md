---
description: "FastAPI + Pydantic v2 backend conventions"
paths:
  - "backend/**/*.py"
---

# Python Backend Rules

## FastAPI
- All route handlers must be `async def`
- Use dependency injection (`Depends()`) for shared logic (auth, DB, config)
- Use `lifespan` context manager for startup/shutdown (model loading, connections)
- Return Pydantic models from endpoints, not dicts
- Use `status_code` parameter on route decorators

## Pydantic v2
- Use `model_validate()` not `parse_obj()`
- Use `model_dump()` not `.dict()`
- Use `ConfigDict` class attribute, not inner `Config` class
- Define explicit `Field()` with descriptions for OpenAPI doc generation
- Use `Annotated[type, Field(...)]` pattern for complex validations

## Type Hints
- Type hints on ALL function signatures (params + return)
- Use `collections.abc` types: `Sequence`, `Mapping` (not `List`, `Dict`)
- Use `X | None` syntax (not `Optional[X]`)

## Error Handling
- Define custom exception classes in `app/utils/errors.py`
- Register exception handlers in `app/main.py`
- Never expose stack traces or internal details in API responses
- Use structured error format: `{"error": {"code": "...", "message": "...", "details": [...]}}`

## Logging
- Use `structlog` or `logging` with JSON formatter — never `print()`
- Log at appropriate levels: DEBUG for dev, INFO for operations, ERROR for failures
- Include context: `request_id`, `job_id`, `user_ip` in log entries
