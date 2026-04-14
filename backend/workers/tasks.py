import json

import structlog

from app.guardrails.content_policy import check_nsfw_output
from app.ml.lora_manager import load_lora, unload_lora
from app.ml.pipeline import generate
from app.utils.storage import save_image
from workers.broker import broker

logger = structlog.get_logger()


@broker.task
async def generate_image(
    job_id: str,
    prompt: str,
    negative_prompt: str = "",
    width: int = 512,
    height: int = 512,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: int | None = None,
    scheduler: str = "DPMSolverMultistep",
    lora_model_id: str | None = None,
    lora_scale: float = 0.8,
) -> dict[str, str]:
    try:
        await broker.redis.set(
            f"job:{job_id}",
            json.dumps({"status": "processing", "progress": 10}),
            ex=3600,
        )

        if lora_model_id:
            load_lora(lora_model_id, scale=lora_scale)
        else:
            unload_lora()

        await broker.redis.set(
            f"job:{job_id}",
            json.dumps({"status": "processing", "progress": 30}),
            ex=3600,
        )

        image_data = generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            seed=seed,
            scheduler=scheduler,
        )

        is_safe = check_nsfw_output(image_data)
        if not is_safe:
            await broker.redis.set(
                f"job:{job_id}",
                json.dumps({"status": "failed", "error": "Content filtered by safety check"}),
                ex=3600,
            )
            return {"status": "failed", "job_id": job_id}

        save_image(job_id, image_data)

        await broker.redis.set(
            f"job:{job_id}",
            json.dumps({"status": "completed", "progress": 100}),
            ex=3600,
        )

        logger.info("Generation completed", job_id=job_id)
        return {"status": "completed", "job_id": job_id}

    except Exception:
        logger.exception("Generation failed", job_id=job_id)
        await broker.redis.set(
            f"job:{job_id}",
            json.dumps({"status": "failed", "error": "Internal generation error"}),
            ex=3600,
        )
        return {"status": "failed", "job_id": job_id}
