"""Upload fine-tuned model adapters to HuggingFace Hub."""

import argparse
from pathlib import Path

from huggingface_hub import HfApi, create_repo


def upload_model(model_path: str, repo_id: str, private: bool = False) -> None:
    model_dir = Path(model_path)
    if not model_dir.exists():
        msg = f"Model path not found: {model_path}"
        raise FileNotFoundError(msg)

    api = HfApi()

    create_repo(repo_id, exist_ok=True, private=private)

    api.upload_folder(
        folder_path=str(model_dir),
        repo_id=repo_id,
        commit_message="Upload fine-tuned model adapters",
    )

    print(f"Model uploaded to: https://huggingface.co/{repo_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload model to HuggingFace Hub")
    parser.add_argument("--model_path", type=str, required=True, help="Path to model directory")
    parser.add_argument("--repo_id", type=str, required=True, help="HuggingFace repo ID (user/model)")
    parser.add_argument("--private", action="store_true", help="Make repo private")
    args = parser.parse_args()
    upload_model(args.model_path, args.repo_id, args.private)
