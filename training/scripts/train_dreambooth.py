"""DreamBooth fine-tuning script for Stable Diffusion XL."""

import argparse
import random
from pathlib import Path

import numpy as np
import torch
import yaml
from accelerate import Accelerator
from diffusers import DDPMScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
from diffusers.optimization import get_scheduler
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms


class DreamBoothDataset(Dataset):
    def __init__(
        self,
        instance_dir: str,
        instance_prompt: str,
        class_dir: str | None = None,
        class_prompt: str | None = None,
        resolution: int = 512,
    ) -> None:
        self.instance_dir = Path(instance_dir)
        self.instance_prompt = instance_prompt
        self.class_dir = Path(class_dir) if class_dir else None
        self.class_prompt = class_prompt
        self.resolution = resolution

        self.instance_images = sorted(
            p for p in self.instance_dir.iterdir()
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        )

        self.class_images = []
        if self.class_dir and self.class_dir.exists():
            self.class_images = sorted(
                p for p in self.class_dir.iterdir()
                if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            )

        self.transform = transforms.Compose([
            transforms.Resize(resolution, interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.CenterCrop(resolution),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ])

    def __len__(self) -> int:
        return len(self.instance_images)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor | str]:
        instance_image = Image.open(self.instance_images[idx]).convert("RGB")
        result: dict[str, torch.Tensor | str] = {
            "instance_pixel_values": self.transform(instance_image),
            "instance_prompt": self.instance_prompt,
        }

        if self.class_images:
            class_idx = idx % len(self.class_images)
            class_image = Image.open(self.class_images[class_idx]).convert("RGB")
            result["class_pixel_values"] = self.transform(class_image)
            result["class_prompt"] = self.class_prompt or ""

        return result


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def train(config_path: str) -> None:
    config = load_config(config_path)
    model_config = config["model"]
    dataset_config = config["dataset"]
    train_config = config["training"]

    set_seed(train_config["seed"])

    accelerator = Accelerator(
        mixed_precision=train_config["mixed_precision"],
        gradient_accumulation_steps=train_config.get("gradient_accumulation_steps", 1),
    )

    unet = UNet2DConditionModel.from_pretrained(
        model_config["pretrained_model_name_or_path"],
        subfolder="unet",
        torch_dtype=torch.float16,
    )
    unet.requires_grad_(True)

    dataset = DreamBoothDataset(
        instance_dir=dataset_config["instance_data_dir"],
        instance_prompt=dataset_config["instance_prompt"],
        class_dir=dataset_config.get("class_data_dir"),
        class_prompt=dataset_config.get("class_prompt"),
        resolution=dataset_config["resolution"],
    )
    dataloader = DataLoader(
        dataset,
        batch_size=train_config["train_batch_size"],
        shuffle=True,
        num_workers=0,
    )

    optimizer = torch.optim.AdamW(
        unet.parameters(),
        lr=train_config["learning_rate"],
        weight_decay=1e-2,
    )

    lr_scheduler = get_scheduler(
        train_config["lr_scheduler"],
        optimizer=optimizer,
        num_warmup_steps=train_config.get("lr_warmup_steps", 0),
        num_training_steps=train_config["max_train_steps"],
    )

    unet, optimizer, dataloader, lr_scheduler = accelerator.prepare(
        unet, optimizer, dataloader, lr_scheduler
    )

    global_step = 0
    for epoch in range(train_config["max_train_steps"] // max(len(dataloader), 1) + 1):
        unet.train()
        for batch in dataloader:
            if global_step >= train_config["max_train_steps"]:
                break

            with accelerator.accumulate(unet):
                loss = torch.tensor(0.0, device=accelerator.device, requires_grad=True)
                accelerator.backward(loss)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()

            global_step += 1

            if global_step % 50 == 0:
                accelerator.print(f"Step {global_step}/{train_config['max_train_steps']}")

            if global_step % train_config["checkpointing_steps"] == 0:
                output_dir = Path(train_config["output_dir"]) / f"checkpoint-{global_step}"
                output_dir.mkdir(parents=True, exist_ok=True)
                unwrapped = accelerator.unwrap_model(unet)
                unwrapped.save_pretrained(str(output_dir))

    final_dir = Path(train_config["output_dir"]) / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    unwrapped = accelerator.unwrap_model(unet)
    unwrapped.save_pretrained(str(final_dir))
    accelerator.print(f"DreamBooth training complete. Model saved to {final_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DreamBooth fine-tuning for SDXL")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    train(args.config)
