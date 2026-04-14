---
description: "React 19 component patterns and best practices"
paths:
  - "frontend/**/*.tsx"
---

# React Best Practices

## Component Patterns
- Functional components only — no class components
- One component per file; filename matches component name
- Props interface named `{ComponentName}Props`
- Destructure props in function signature
- Use `React.memo()` only for expensive renders with profiler evidence

## Hooks
- Follow Rules of Hooks: top-level only, React functions only
- Custom hooks must start with `use` prefix
- Extract complex state logic into custom hooks
- Use `useCallback` for functions passed to memoized children
- Use `useMemo` for expensive computations, not as premature optimization

## State Management
- Local state: `useState` for simple, `useReducer` for complex
- Server state: TanStack Query (fetching, caching, polling)
- Client state: Zustand (UI state, preferences)
- Avoid prop drilling beyond 2 levels — use context or Zustand

## Error Handling
- Wrap route segments with `error.tsx` boundaries
- Use `ErrorBoundary` for component-level error isolation
- Always handle loading and error states in data-fetching components

## Accessibility
- Semantic HTML: `<button>` not `<div onClick>`, `<nav>`, `<main>`, `<article>`
- `alt` text on all images
- Keyboard navigation support on interactive elements
- ARIA attributes when semantic HTML is insufficient
