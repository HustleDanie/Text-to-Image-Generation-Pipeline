"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { StatusResponse } from "@/lib/types";

export function useJobStatus(jobId: string | null) {
  return useQuery<StatusResponse>({
    queryKey: ["jobStatus", jobId],
    queryFn: () => apiClient.getStatus(jobId!),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === "completed" || data?.status === "failed") {
        return false;
      }
      return 2000;
    },
  });
}
