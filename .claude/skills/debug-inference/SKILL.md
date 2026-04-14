---
name: debug-inference
description: "Diagnose and fix common ML inference issues: OOM, model loading, dtype mismatches"
---

# Debug Inference

## Common Issues

### CUDA Out of Memory (OOM)
1. Check GPU memory: `nvidia-smi`
2. Fixes (try in order):
   - Enable `torch.float16` dtype
   - Enable attention slicing: `pipe.enable_attention_slicing()`
   - Enable VAE tiling: `pipe.enable_vae_tiling()`
   - Reduce resolution (512→384→256)
   - Enable CPU offloading: `pipe.enable_model_cpu_offload()`
   - Clear cache: `torch.cuda.empty_cache()`

### Model Loading Failures
1. Verify model path/ID: `huggingface_hub.model_info("model-id")`
2. Check disk space: model weights can be 2-7 GB
3. Ensure correct `torch_dtype` matches model training dtype
4. Check internet connection for first-time downloads
5. Use `local_files_only=True` after initial download

### LoRA Loading Issues
1. Verify adapter path: `ls outputs/my_model/`
2. Check adapter config: `adapter_config.json` must exist
3. Ensure base model matches adapter training model
4. Load correctly:
   ```python
   pipe.load_lora_weights("path/to/adapter", weight_name="pytorch_lora_weights.safetensors")
   pipe.fuse_lora(lora_scale=0.8)
   ```

### Dtype Mismatches
- Symptom: `RuntimeError: expected scalar type Float but found Half`
- Fix: Ensure pipeline and inputs use same dtype
- Use `pipe.to(torch.float16)` consistently

### Slow Generation
1. Use `torch.compile(pipe.unet)` for 20-30% speedup
2. Enable `pipe.enable_xformers_memory_efficient_attention()` if available
3. Reduce `num_inference_steps` (50→30→20)
4. Use faster schedulers: `DPMSolverMultistepScheduler`, `EulerAncestralDiscreteScheduler`
