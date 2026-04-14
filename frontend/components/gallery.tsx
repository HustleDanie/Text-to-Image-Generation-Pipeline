"use client";

import Image from "next/image";
import { useImageStore } from "@/stores/image-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { formatDate } from "@/lib/utils";

export function Gallery() {
  const images = useImageStore((s) => s.images);
  const removeImage = useImageStore((s) => s.removeImage);
  const clearImages = useImageStore((s) => s.clearImages);

  if (images.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-[var(--border)] p-12 text-center">
        <p className="text-[var(--muted)]">
          No images generated yet. Create your first image above!
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm text-[var(--muted)]">
          {images.length} image{images.length !== 1 ? "s" : ""}
        </p>
        <Button variant="secondary" size="sm" onClick={clearImages}>
          Clear All
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {images.map((image) => (
          <Card key={image.id} className="overflow-hidden p-0">
            <div className="relative aspect-square">
              <Image
                src={image.imageUrl}
                alt={image.prompt}
                fill
                className="object-cover"
                sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
              />
            </div>
            <div className="p-4">
              <p className="line-clamp-2 text-sm">{image.prompt}</p>
              <div className="mt-2 flex items-center justify-between">
                <p className="text-xs text-[var(--muted)]">
                  {formatDate(image.createdAt)}
                </p>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => removeImage(image.id)}
                >
                  Remove
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
