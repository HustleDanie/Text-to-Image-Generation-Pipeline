---
description: "Tailwind CSS 4 patterns and conventions"
paths:
  - "frontend/**/*.tsx"
---

# Tailwind CSS Patterns

## Approach
- Utility-first: compose utilities in JSX, extract component classes sparingly
- Mobile-first responsive: `base → sm → md → lg → xl → 2xl`
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes

## cn() Pattern
```tsx
import { cn } from "@/lib/utils";

function Button({ className, variant, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "rounded-lg px-4 py-2 font-medium transition-colors",
        variant === "primary" && "bg-blue-600 text-white hover:bg-blue-700",
        variant === "secondary" && "bg-gray-200 text-gray-900 hover:bg-gray-300",
        className
      )}
      {...props}
    />
  );
}
```

## Dark Mode
- Use `dark:` variant for dark mode styles
- Define color tokens in CSS custom properties for theming

## Spacing & Layout
- Use consistent spacing scale (multiples of 4: 1, 2, 3, 4, 6, 8, 12, 16)
- Prefer `gap` over margins for flex/grid children
- Use `max-w-screen-xl mx-auto` for page-level containers
