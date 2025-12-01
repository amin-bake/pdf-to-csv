import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

export interface UploadedFile {
  fileId: string;
  fileName: string;
  fileSize: number;
  status: "uploading" | "uploaded" | "converting" | "completed" | "error";
  progress: number;
  error?: string;
}

interface UploadState {
  files: UploadedFile[];
  parser: "pdfplumber" | "tabula";
  merge: boolean;
  currentJobId: string | null;

  addFiles: (files: UploadedFile[]) => void;
  updateFile: (fileId: string, updates: Partial<UploadedFile>) => void;
  removeFile: (fileId: string) => void;
  clearFiles: () => void;
  setParser: (parser: "pdfplumber" | "tabula") => void;
  setMerge: (merge: boolean) => void;
  setCurrentJobId: (jobId: string | null) => void;
  markAllAsConverting: () => void;
  markAllAsCompleted: () => void;
}

export const useUploadStore = create<UploadState>()(
  devtools(
    persist(
      (set) => ({
        files: [],
        parser: "pdfplumber",
        merge: true,
        currentJobId: null,

        addFiles: (files) =>
          set((state) => ({
            files: [...state.files, ...files],
          })),

        updateFile: (fileId, updates) =>
          set((state) => ({
            files: state.files.map((f) =>
              f.fileId === fileId ? { ...f, ...updates } : f
            ),
          })),

        removeFile: (fileId) =>
          set((state) => ({
            files: state.files.filter((f) => f.fileId !== fileId),
          })),

        clearFiles: () => set({ files: [], currentJobId: null }),

        setParser: (parser) => set({ parser }),

        setMerge: (merge) => set({ merge }),

        setCurrentJobId: (jobId) => set({ currentJobId: jobId }),

        markAllAsConverting: () =>
          set((state) => ({
            files: state.files.map((f) => ({
              ...f,
              status: "converting" as const,
              progress: 0,
            })),
          })),

        markAllAsCompleted: () =>
          set((state) => ({
            files: state.files.map((f) => ({
              ...f,
              status: "completed" as const,
              progress: 100,
            })),
          })),
      }),
      { name: "upload-store" }
    )
  )
);
