"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { GenerateRequest, StatusResponse } from "@/lib/types";
import { useImageStore } from "@/stores/image-store";

export function useGenerate() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const addImage = useImageStore((s) => s.addImage);

  const mutation = useMutation({
    mutationFn: async (params: GenerateRequest) => {
      const job = await apiClient.generate(params);
      setJobId(job.job_id);

      // Poll for completion
      const result = await pollForCompletion(job.job_id);

      if (result.status === "completed" && result.image_url) {
        addImage({
          id: crypto.randomUUID(),
          jobId: job.job_id,
          prompt: params.prompt,
          imageUrl: apiClient.getImageUrl(job.job_id),
          createdAt: new Date(),
          settings: {
            width: params.width ?? 512,
            height: params.height ?? 512,
            guidanceScale: params.guidance_scale ?? 7.5,
            steps: params.num_inference_steps ?? 30,
            seed: params.seed ?? null,
            scheduler: params.scheduler ?? "DPMSolverMultistep",
          },
        });
      }

      return result;
    },
  });

  async function pollForCompletion(id: string): Promise<StatusResponse> {
    const maxAttempts = 120;
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const statusResult = await apiClient.getStatus(id);
      setStatus(statusResult);

      if (statusResult.status === "completed" || statusResult.status === "failed") {
        return statusResult;
      }
    }

    return {
      job_id: id,
      status: "failed",
      progress: null,
      image_url: null,
      error: "Generation timed out",
    };
  }

  return {
    generate: mutation.mutate,
    isGenerating: mutation.isPending,
    jobId,
    status,
    error: mutation.error,
    reset: () => {
      mutation.reset();
      setJobId(null);
      setStatus(null);
    },
  };
}
