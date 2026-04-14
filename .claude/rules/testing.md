---
description: "Testing conventions and patterns"
paths:
  - "**/*.test.*"
  - "**/*_test.*"
  - "**/tests/**"
  - "**/__tests__/**"
---

# Testing Rules

## Pattern: AAA (Arrange-Act-Assert)
```python
def test_generate_returns_job_id(client, mock_broker):
    # Arrange
    payload = {"prompt": "a sunset over mountains", "width": 512, "height": 512}

    # Act
    response = client.post("/api/generate", json=payload)

    # Assert
    assert response.status_code == 202
    assert "job_id" in response.json()
```

## Python (pytest)
- Use fixtures for setup/teardown — no inline setup
- Use `conftest.py` for shared fixtures
- Mock at boundaries (external APIs, ML models, Redis) — never mock internals
- Use `httpx.AsyncClient` with `ASGITransport` for FastAPI async tests
- Name tests: `test_{function}_{scenario}_{expected_result}`

## TypeScript (vitest)
- Use React Testing Library for component tests
- Test behavior, not implementation: query by role/text, not test-ids
- Use `userEvent` over `fireEvent` for realistic interactions
- Mock API calls with MSW (Mock Service Worker) or vitest mocks
- Name tests: `it("should {behavior} when {condition}")`

## Coverage
- Aim for 80%+ on critical paths (routes, guardrails, hooks)
- Don't chase 100% — focus on logic, edge cases, error paths
