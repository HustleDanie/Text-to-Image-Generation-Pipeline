import { create } from "zustand";
import type { GalleryImage } from "@/lib/types";

interface ImageStore {
  images: GalleryImage[];
  addImage: (image: GalleryImage) => void;
  removeImage: (id: string) => void;
  clearImages: () => void;
}

export const useImageStore = create<ImageStore>((set) => ({
  images: [],

  addImage: (image) =>
    set((state) => ({
      images: [image, ...state.images],
    })),

  removeImage: (id) =>
    set((state) => ({
      images: state.images.filter((img) => img.id !== id),
    })),

  clearImages: () => set({ images: [] }),
}));
