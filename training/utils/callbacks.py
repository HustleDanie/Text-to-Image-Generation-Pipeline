"""Training callbacks for logging and checkpointing."""

from pathlib import Path


class LoggingCallback:
    def __init__(self, log_every: int = 100) -> None:
        self.log_every = log_every
        self.losses: list[float] = []

    def on_step_end(self, step: int, loss: float) -> None:
        self.losses.append(loss)
        if step % self.log_every == 0:
            avg_loss = sum(self.losses[-self.log_every:]) / min(len(self.losses), self.log_every)
            print(f"Step {step} | Avg Loss: {avg_loss:.6f} | Current Loss: {loss:.6f}")


class CheckpointCallback:
    def __init__(self, save_every: int = 500, output_dir: str = "./checkpoints") -> None:
        self.save_every = save_every
        self.output_dir = Path(output_dir)

    def on_step_end(self, step: int, model: object) -> None:
        if step % self.save_every == 0 and step > 0:
            checkpoint_dir = self.output_dir / f"checkpoint-{step}"
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            if hasattr(model, "save_pretrained"):
                model.save_pretrained(str(checkpoint_dir))  # type: ignore[union-attr]
                print(f"Checkpoint saved: {checkpoint_dir}")


class ValidationCallback:
    def __init__(self, validate_every: int = 500) -> None:
        self.validate_every = validate_every

    def on_step_end(self, step: int) -> bool:
        return step % self.validate_every == 0 and step > 0
