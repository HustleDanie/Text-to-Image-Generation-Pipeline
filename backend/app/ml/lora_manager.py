import structlog

from app.ml.pipeline import get_pipeline

logger = structlog.get_logger()

_loaded_lora: str | None = None


def load_lora(model_id: str, scale: float = 0.8) -> None:
    global _loaded_lora  # noqa: PLW0603
    pipe = get_pipeline()

    if _loaded_lora == model_id:
        logger.debug("LoRA already loaded", model_id=model_id)
        return

    if _loaded_lora is not None:
        unload_lora()

    logger.info("Loading LoRA adapter", model_id=model_id, scale=scale)
    pipe.load_lora_weights(model_id)
    pipe.fuse_lora(lora_scale=scale)
    _loaded_lora = model_id
    logger.info("LoRA adapter loaded", model_id=model_id)


def unload_lora() -> None:
    global _loaded_lora  # noqa: PLW0603
    if _loaded_lora is None:
        return

    pipe = get_pipeline()
    pipe.unfuse_lora()
    pipe.unload_lora_weights()

    logger.info("LoRA adapter unloaded", model_id=_loaded_lora)
    _loaded_lora = None


def get_loaded_lora() -> str | None:
    return _loaded_lora
