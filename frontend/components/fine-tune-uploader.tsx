"use client";

import { useCallback, useState, type ChangeEvent, type DragEvent } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface FineTuneUploaderProps {
  onUpload?: (files: File[]) => void;
}

export function FineTuneUploader({ onUpload }: FineTuneUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  const handleDragOver = useCallback((e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const droppedFiles = Array.from(e.dataTransfer.files).filter((f) =>
        f.type.startsWith("image/"),
      );
      setFiles((prev) => [...prev, ...droppedFiles]);
      onUpload?.(droppedFiles);
    },
    [onUpload],
  );

  const handleFileInput = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      const selectedFiles = Array.from(e.target.files ?? []);
      setFiles((prev) => [...prev, ...selectedFiles]);
      onUpload?.(selectedFiles);
    },
    [onUpload],
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Training Images</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            "rounded-lg border-2 border-dashed p-8 text-center transition-colors",
            isDragging
              ? "border-[var(--primary)] bg-[var(--primary)]/5"
              : "border-[var(--border)]",
          )}
        >
          <p className="mb-2 text-sm text-[var(--muted)]">
            Drag & drop training images here, or
          </p>
          <label>
            <Button type="button" variant="secondary" size="sm" asChild>
              <span>Browse Files</span>
            </Button>
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileInput}
              className="hidden"
            />
          </label>
          <p className="mt-2 text-xs text-[var(--muted)]">
            PNG, JPG, WebP. 10-30 images recommended for LoRA.
          </p>
        </div>

        {files.length > 0 && (
          <div className="mt-4">
            <p className="text-sm font-medium">
              {files.length} image{files.length !== 1 ? "s" : ""} selected
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              {files.map((file, i) => (
                <span
                  key={`${file.name}-${i}`}
                  className="rounded-md bg-[var(--border)] px-2 py-1 text-xs"
                >
                  {file.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
