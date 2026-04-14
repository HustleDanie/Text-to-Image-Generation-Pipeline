"""Evaluation metrics for fine-tuned models."""

from PIL import Image


def compute_clip_score(images: list[Image.Image], prompts: list[str]) -> list[float]:
    """Compute CLIP similarity scores between images and text prompts.

    Requires: pip install transformers
    Returns list of cosine similarity scores (0-1).
    """
    try:
        import torch
        from transformers import CLIPModel, CLIPProcessor

        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        scores: list[float] = []
        for image, prompt in zip(images, prompts, strict=True):
            inputs = processor(text=[prompt], images=image, return_tensors="pt", padding=True)
            outputs = model(**inputs)

            logits = outputs.logits_per_image
            score = logits.item() / 100.0
            scores.append(score)

        return scores

    except ImportError:
        print("Warning: transformers not installed. Returning placeholder scores.")
        return [0.0] * len(images)


def compute_fid(
    real_images_dir: str,
    generated_images_dir: str,
) -> float:
    """Compute FID score between real and generated image directories.

    Lower FID = better quality. Requires: pip install torch-fidelity
    """
    try:
        from torch_fidelity import calculate_metrics

        metrics = calculate_metrics(
            input1=real_images_dir,
            input2=generated_images_dir,
            cuda=True,
            fid=True,
        )
        return metrics["frechet_inception_distance"]

    except ImportError:
        print("Warning: torch-fidelity not installed. Returning placeholder FID.")
        return -1.0
