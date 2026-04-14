---
description: "Next.js 16 + TypeScript frontend conventions"
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.tsx"
---

# TypeScript Frontend Rules

## Next.js 16.2
- Use App Router exclusively (no Pages Router)
- Default to Server Components; add `'use client'` only when state/effects/browser APIs needed
- Use `use cache` for data caching (replaces `getStaticProps`/`getServerSideProps`)
- Use `loading.tsx` and `error.tsx` for route-level loading/error states
- Image optimization via `next/image` with explicit `width` and `height`
- Use `next/link` for client-side navigation

## TypeScript
- Strict mode enabled (`"strict": true` in tsconfig)
- No `any` — use `unknown` + type guards
- Define explicit interfaces for component props (not inline types)
- Use `as const` for literal types
- Prefer `interface` for object shapes, `type` for unions/intersections

## Imports
- Group: React → Next.js → third-party → local components → local lib → types
- Use path aliases: `@/components/`, `@/lib/`, `@/hooks/`, `@/stores/`
- No default exports except for pages/layouts (Next.js convention)
