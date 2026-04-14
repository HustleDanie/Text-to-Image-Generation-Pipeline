from pydantic import BaseModel, Field


class JobResponse(BaseModel):
    job_id: str = Field(description="Unique identifier for the generation job")
    status: str = Field(default="queued", description="Job status: queued, processing, completed, failed")


class StatusResponse(BaseModel):
    job_id: str
    status: str = Field(description="Job status: queued, processing, completed, failed")
    progress: int | None = Field(default=None, description="Progress percentage (0-100)")
    image_url: str | None = Field(default=None, description="URL to retrieve the generated image")
    error: str | None = Field(default=None, description="Error message if generation failed")


class ModelInfo(BaseModel):
    model_id: str
    name: str
    model_type: str = Field(description="Type: base, lora")
    description: str = ""


class ModelsResponse(BaseModel):
    models: list[ModelInfo]


class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool = False
    device: str = ""
    version: str = "0.1.0"


class ErrorDetail(BaseModel):
    field: str | None = None
    issue: str


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []


class ErrorResponse(BaseModel):
    error: ErrorBody
