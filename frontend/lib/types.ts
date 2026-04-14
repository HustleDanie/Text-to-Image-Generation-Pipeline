export interface GenerateRequest {
  prompt: string;
  negative_prompt?: string;
  width?: number;
  height?: number;
  guidance_scale?: number;
  num_inference_steps?: number;
  seed?: number | null;
  scheduler?: string;
  lora_model_id?: string | null;
  lora_scale?: number;
}

export interface JobResponse {
  job_id: string;
  status: string;
}

export interface StatusResponse {
  job_id: string;
  status: "queued" | "processing" | "completed" | "failed";
  progress: number | null;
  image_url: string | null;
  error: string | null;
}

export interface ModelInfo {
  model_id: string;
  name: string;
  model_type: "base" | "lora";
  description: string;
}

export interface ModelsResponse {
  models: ModelInfo[];
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  device: string;
  version: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: Array<{ field?: string; issue: string }>;
  };
}

export interface GalleryImage {
  id: string;
  jobId: string;
  prompt: string;
  imageUrl: string;
  createdAt: Date;
  settings: {
    width: number;
    height: number;
    guidanceScale: number;
    steps: number;
    seed: number | null;
    scheduler: string;
  };
}
