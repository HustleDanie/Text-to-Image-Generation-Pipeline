import { describe, it, expect } from "vitest";

describe("ImageGenerator", () => {
  it("should be importable", async () => {
    // Basic smoke test to verify the component can be imported
    const module = await import("@/components/image-generator");
    expect(module.ImageGenerator).toBeDefined();
  });
});
