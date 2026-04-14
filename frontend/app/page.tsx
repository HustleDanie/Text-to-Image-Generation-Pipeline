import { ImageGenerator } from "@/components/image-generator";
import { Gallery } from "@/components/gallery";

export default function Home() {
  return (
    <main className="mx-auto max-w-screen-xl px-4 py-8">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          AI Image Studio
        </h1>
        <p className="mt-3 text-lg text-[var(--muted)]">
          Generate images from text prompts using fine-tuned Stable Diffusion
          with LoRA adapters
        </p>
      </header>

      <section className="mb-16">
        <ImageGenerator />
      </section>

      <section>
        <h2 className="mb-6 text-2xl font-semibold">Generated Images</h2>
        <Gallery />
      </section>
    </main>
  );
}
