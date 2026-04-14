import type {
  GenerateRequest,
  JobResponse,
  StatusResponse,
  ModelsResponse,
  HealthResponse,
  ApiError,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClientError extends Error {
  constructor(
    public status: number,
    public body: ApiError,
  ) {
    super(body.error.message);
    this.name = "ApiClientError";
  }
}

async function request<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const body = (await response.json()) as ApiError;
    throw new ApiClientError(response.status, body);
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  generate(params: GenerateRequest): Promise<JobResponse> {
    return request<JobResponse>("/api/generate", {
      method: "POST",
      body: JSON.stringify(params),
    });
  },

  getStatus(jobId: string): Promise<StatusResponse> {
    return request<StatusResponse>(`/api/status/${encodeURIComponent(jobId)}`);
  },

  getImageUrl(jobId: string): string {
    return `${API_BASE_URL}/api/images/${encodeURIComponent(jobId)}`;
  },

  getModels(): Promise<ModelsResponse> {
    return request<ModelsResponse>("/api/models");
  },

  getHealth(): Promise<HealthResponse> {
    return request<HealthResponse>("/health");
  },
};
