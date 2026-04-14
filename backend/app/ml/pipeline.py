import threading

import structlog
import torch
from diffusers import (
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    StableDiffusionXLPipeline,
)

from app.config import settings

logger = structlog.get_logger()

_pipeline: StableDiffusionXLPipeline | None = None
_lock = threading.Lock()

SCHEDULERS: dict[str, type] = {
    "DPMSolverMultistep": DPMSolverMultistepScheduler,
    "EulerAncestral": EulerAncestralDiscreteScheduler,
    "Euler": EulerDiscreteScheduler,
}


def get_pipeline() -> StableDiffusionXLPipeline:
    global _pipeline  # noqa: PLW0603
    if _pipeline is not None:
        return _pipeline

    with _lock:
        if _pipeline is not None:
            return _pipeline

        logger.info("Loading pipeline", model_id=settings.model_id)

        dtype = torch.float16 if settings.torch_dtype == "float16" else torch.float32

        pipe = StableDiffusionXLPipeline.from_pretrained(
            settings.model_id,
            torch_dtype=dtype,
            use_safetensors=True,
            variant="fp16" if dtype == torch.float16 else None,
        )
        pipe = pipe.to(settings.device)

        pipe.enable_attention_slicing()

        if settings.device == "cuda":
            pipe.enable_vae_tiling()

        _pipeline = pipe
        logger.info("Pipeline loaded successfully", device=settings.device)
        return _pipeline


def set_scheduler(pipeline: StableDiffusionXLPipeline, scheduler_name: str) -> None:
    scheduler_cls = SCHEDULERS.get(scheduler_name)
    if scheduler_cls is not None:
        pipeline.scheduler = scheduler_cls.from_config(pipeline.scheduler.config)


def generate(
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: int | None = None,
    scheduler: str = "DPMSolverMultistep",
) -> bytes:
    import io

    pipe = get_pipeline()
    set_scheduler(pipe, scheduler)

    generator = None
    if seed is not None:
        generator = torch.Generator(device=settings.device).manual_seed(seed)

    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt or None,
        width=width,
        height=height,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        generator=generator,
    )

    image = result.images[0]
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
