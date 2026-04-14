"use client";

import { useModels } from "@/hooks/use-models";

interface ModelSelectorProps {
  selectedModel: string | null;
  onModelChange: (modelId: string | null) => void;
}

export function ModelSelector({ selectedModel, onModelChange }: ModelSelectorProps) {
  const { data, isLoading } = useModels();

  const loraModels = data?.models.filter((m) => m.model_type === "lora") ?? [];

  if (isLoading) {
    return (
      <div className="flex flex-col gap-1.5">
        <label className="text-sm font-medium">LoRA Model</label>
        <div className="h-10 animate-pulse rounded-lg bg-[var(--border)]" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor="model-select" className="text-sm font-medium">
        LoRA Model (optional)
      </label>
      <select
        id="model-select"
        value={selectedModel ?? ""}
        onChange={(e) => onModelChange(e.target.value || null)}
        className="h-10 rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 text-sm text-[var(--foreground)] focus:border-[var(--primary)] focus:outline-none focus:ring-1 focus:ring-[var(--primary)]"
      >
        <option value="">None (base model)</option>
        {loraModels.map((model) => (
          <option key={model.model_id} value={model.model_id}>
            {model.name}
          </option>
        ))}
      </select>
    </div>
  );
}
