from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: Annotated[
        str,
        Field(
            min_length=1,
            max_length=500,
            description="Text prompt describing the image to generate",
            examples=["A serene mountain landscape at sunset, oil painting style"],
        ),
    ]
    negative_prompt: Annotated[
        str,
        Field(
            default="",
            max_length=500,
            description="Text describing what to exclude from the image",
        ),
    ]
    width: Annotated[
        int,
        Field(
            default=512,
            ge=256,
            le=1024,
            multiple_of=64,
            description="Image width in pixels (must be multiple of 64)",
        ),
    ]
    height: Annotated[
        int,
        Field(
            default=512,
            ge=256,
            le=1024,
            multiple_of=64,
            description="Image height in pixels (must be multiple of 64)",
        ),
    ]
    guidance_scale: Annotated[
        float,
        Field(
            default=7.5,
            ge=1.0,
            le=30.0,
            description="How strongly the image follows the prompt",
        ),
    ]
    num_inference_steps: Annotated[
        int,
        Field(
            default=30,
            ge=1,
            le=100,
            description="Number of denoising steps",
        ),
    ]
    seed: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            le=2147483647,
            description="Random seed for reproducibility",
        ),
    ]
    scheduler: Annotated[
        str,
        Field(
            default="DPMSolverMultistep",
            description="Scheduler algorithm",
        ),
    ]
    lora_model_id: Annotated[
        str | None,
        Field(
            default=None,
            description="LoRA adapter model ID to apply",
        ),
    ]
    lora_scale: Annotated[
        float,
        Field(
            default=0.8,
            ge=0.0,
            le=1.5,
            description="LoRA adapter scale weight",
        ),
    ]
