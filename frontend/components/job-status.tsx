"use client";

import type { StatusResponse } from "@/lib/types";
import { cn } from "@/lib/utils";

interface JobStatusProps {
  status: StatusResponse;
}

export function JobStatus({ status }: JobStatusProps) {
  const statusColors: Record<string, string> = {
    queued: "text-yellow-600 dark:text-yellow-400",
    processing: "text-blue-600 dark:text-blue-400",
    completed: "text-green-600 dark:text-green-400",
    failed: "text-red-600 dark:text-red-400",
  };

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--background)] p-3">
      <div className="flex items-center gap-2">
        <span
          className={cn(
            "text-sm font-medium capitalize",
            statusColors[status.status] ?? "text-[var(--muted)]",
          )}
        >
          {status.status}
        </span>

        {status.progress !== null && status.progress !== undefined && (
          <div className="flex-1">
            <div className="h-2 overflow-hidden rounded-full bg-[var(--border)]">
              <div
                className="h-full rounded-full bg-[var(--primary)] transition-all duration-300"
                style={{ width: `${status.progress}%` }}
              />
            </div>
          </div>
        )}

        {status.progress !== null && (
          <span className="text-xs text-[var(--muted)]">
            {status.progress}%
          </span>
        )}
      </div>

      {status.error && (
        <p className="mt-2 text-sm text-[var(--destructive)]">
          {status.error}
        </p>
      )}
    </div>
  );
}
