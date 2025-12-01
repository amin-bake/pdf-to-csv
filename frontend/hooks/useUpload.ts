import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { api, type UploadResponse } from "@/lib/api";

interface UploadOptions {
  onSuccess?: (file: UploadResponse) => void;
  onError?: (fileId: string, error: Error) => void;
  onProgress?: (fileId: string, progress: number) => void;
}

export function useUpload(options?: UploadOptions) {
  const [progress, setProgress] = useState<Record<string, number>>({});

  const uploadFile = async (file: File, fileId: string) => {
    try {
      // Simulate progress
      setProgress((prev) => ({ ...prev, [fileId]: 50 }));
      options?.onProgress?.(fileId, 50);

      const result = await api.upload(file);

      setProgress((prev) => ({ ...prev, [fileId]: 100 }));
      options?.onProgress?.(fileId, 100);
      options?.onSuccess?.(result);

      return result;
    } catch (error) {
      setProgress((prev) => ({ ...prev, [fileId]: 0 }));
      options?.onError?.(fileId, error as Error);
      throw error;
    }
  };

  const mutation = useMutation({
    mutationFn: async ({ file, fileId }: { file: File; fileId: string }) => {
      return uploadFile(file, fileId);
    },
  });

  return {
    upload: (file: File, fileId: string) => uploadFile(file, fileId),
    uploading: mutation.isPending,
    progress,
    error: mutation.error,
  };
}
