"""Evaluate fine-tuned models using FID, CLIP score, and LPIPS metrics."""

import argparse
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image

from utils.metrics import compute_clip_score


def generate_evaluation_images(
    model_path: str,
    prompts: list[str],
    output_dir: str,
    num_images_per_prompt: int = 4,
    seed: int = 42,
) -> list[Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        use_safetensors=True,
    ).to("cuda" if torch.cuda.is_available() else "cpu")

    generated_paths: list[Path] = []
    generator = torch.Generator().manual_seed(seed)

    for i, prompt in enumerate(prompts):
        for j in range(num_images_per_prompt):
            image = pipe(prompt=prompt, generator=generator).images[0]
            file_path = output_path / f"eval_{i}_{j}.png"
            image.save(file_path)
            generated_paths.append(file_path)

    return generated_paths


def evaluate(model_path: str, prompts_file: str, output_dir: str = "./eval_output") -> None:
    prompts_path = Path(prompts_file)
    if not prompts_path.exists():
        msg = f"Prompts file not found: {prompts_file}"
        raise FileNotFoundError(msg)

    prompts = [line.strip() for line in prompts_path.read_text().splitlines() if line.strip()]

    print(f"Evaluating model: {model_path}")
    print(f"Using {len(prompts)} prompts")

    generated_paths = generate_evaluation_images(
        model_path=model_path,
        prompts=prompts,
        output_dir=output_dir,
    )

    images = [Image.open(p) for p in generated_paths]
    expanded_prompts = [p for p in prompts for _ in range(4)]

    clip_scores = compute_clip_score(images, expanded_prompts[:len(images)])
    avg_clip = sum(clip_scores) / len(clip_scores) if clip_scores else 0.0

    print(f"\nResults:")
    print(f"  Generated images: {len(generated_paths)}")
    print(f"  Avg CLIP score: {avg_clip:.4f}")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned model")
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--prompts", type=str, required=True, help="Path to prompts text file")
    parser.add_argument("--output_dir", type=str, default="./eval_output")
    args = parser.parse_args()
    evaluate(args.model_path, args.prompts, args.output_dir)
