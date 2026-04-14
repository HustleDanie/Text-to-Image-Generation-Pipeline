# API Documentation

Interactive docs available at: `http://localhost:8000/docs` (Swagger UI)

## Endpoints

### POST /api/generate
Submit an image generation job.

**Request:**
```json
{
  "prompt": "A serene mountain landscape at sunset, oil painting style",
  "negative_prompt": "blurry, low quality",
  "width": 512,
  "height": 512,
  "guidance_scale": 7.5,
  "num_inference_steps": 30,
  "seed": 42,
  "scheduler": "DPMSolverMultistep",
  "lora_model_id": null,
  "lora_scale": 0.8
}
```

**Response (202 Accepted):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}
```

### GET /api/status/{job_id}
Poll the status of a generation job.

**Response (200):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "image_url": null,
  "error": null
}
```

Status values: `queued`, `processing`, `completed`, `failed`

When completed:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "image_url": "/api/images/550e8400-e29b-41d4-a716-446655440000",
  "error": null
}
```

### GET /api/images/{job_id}
Retrieve the generated image (PNG binary).

**Response:** `image/png` binary data

### GET /api/models
List available base models and LoRA adapters.

**Response:**
```json
{
  "models": [
    {
      "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
      "name": "Stable Diffusion XL Base",
      "model_type": "base",
      "description": "SDXL 1.0 base model"
    }
  ]
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "version": "0.1.0"
}
```

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Width must be between 256 and 1024",
    "details": [
      {"field": "width", "issue": "Value 2048 exceeds maximum of 1024"}
    ]
  }
}
```

Error codes: `VALIDATION_ERROR`, `PROMPT_BLOCKED`, `JOB_NOT_FOUND`, `GENERATION_FAILED`, `RATE_LIMITED`
