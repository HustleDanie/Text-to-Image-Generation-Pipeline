---
name: add-react-component
description: "Guide to create a React 19 component following Next.js 16 patterns with tests"
---

# Add React Component

## Steps

1. **Decide Server vs Client Component**
   - Default: Server Component (no directive needed)
   - Add `'use client'` only if using: `useState`, `useEffect`, `onClick`, browser APIs

2. **Create component file** in `frontend/components/`
   - Define `{ComponentName}Props` interface
   - Destructure props in function signature
   - Use `cn()` utility for conditional Tailwind classes
   - Export as named export

3. **Add to parent page/component**
   - Import using `@/components/` path alias
   - Pass typed props

4. **Write test** in `frontend/__tests__/components/`
   - Use React Testing Library
   - Test rendering, interactions, edge cases
   - Query by role/text, not test-ids

5. **Verify**
   - `npx tsc --noEmit` (type check)
   - `npx vitest run` (tests)
   - `npx eslint frontend/` (lint)
   - Visual check in browser
