"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { JobStatus } from "@/components/job-status";
import { ModelSelector } from "@/components/model-selector";
import { useGenerate } from "@/hooks/use-generate";
import type { GenerateRequest } from "@/lib/types";

export function ImageGenerator() {
  const { generate, isGenerating, status, error, reset } = useGenerate();

  const [prompt, setPrompt] = useState("");
  const [negativePrompt, setNegativePrompt] = useState("");
  const [width, setWidth] = useState(512);
  const [height, setHeight] = useState(512);
  const [guidanceScale, setGuidanceScale] = useState(7.5);
  const [steps, setSteps] = useState(30);
  const [seed, setSeed] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const params: GenerateRequest = {
      prompt,
      negative_prompt: negativePrompt || undefined,
      width,
      height,
      guidance_scale: guidanceScale,
      num_inference_steps: steps,
      seed: seed ? parseInt(seed, 10) : null,
      lora_model_id: selectedModel,
    };

    generate(params);
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Image</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="prompt" className="mb-1.5 block text-sm font-medium">
              Prompt
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="A serene mountain landscape at sunset, oil painting style..."
              rows={3}
              maxLength={500}
              required
              className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-sm placeholder:text-[var(--muted)] focus:border-[var(--primary)] focus:outline-none focus:ring-1 focus:ring-[var(--primary)]"
            />
            <p className="mt-1 text-xs text-[var(--muted)]">
              {prompt.length}/500 characters
            </p>
          </div>

          <Input
            id="negative-prompt"
            label="Negative Prompt"
            value={negativePrompt}
            onChange={(e) => setNegativePrompt(e.target.value)}
            placeholder="blurry, low quality, distorted..."
            maxLength={500}
          />

          <ModelSelector
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
          />

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <Input
              id="width"
              label="Width"
              type="number"
              value={width}
              onChange={(e) => setWidth(parseInt(e.target.value, 10))}
              min={256}
              max={1024}
              step={64}
            />
            <Input
              id="height"
              label="Height"
              type="number"
              value={height}
              onChange={(e) => setHeight(parseInt(e.target.value, 10))}
              min={256}
              max={1024}
              step={64}
            />
            <Input
              id="guidance"
              label="Guidance Scale"
              type="number"
              value={guidanceScale}
              onChange={(e) => setGuidanceScale(parseFloat(e.target.value))}
              min={1}
              max={30}
              step={0.5}
            />
            <Input
              id="steps"
              label="Steps"
              type="number"
              value={steps}
              onChange={(e) => setSteps(parseInt(e.target.value, 10))}
              min={1}
              max={100}
            />
          </div>

          <Input
            id="seed"
            label="Seed (optional)"
            type="number"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            placeholder="Random"
            min={0}
            max={2147483647}
          />

          {status && <JobStatus status={status} />}

          {error && (
            <p className="text-sm text-[var(--destructive)]">
              {error instanceof Error ? error.message : "Generation failed"}
            </p>
          )}

          <div className="flex gap-3">
            <Button type="submit" disabled={isGenerating || !prompt.trim()}>
              {isGenerating ? "Generating..." : "Generate"}
            </Button>
            {(status || error) && (
              <Button type="button" variant="secondary" onClick={reset}>
                Reset
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
