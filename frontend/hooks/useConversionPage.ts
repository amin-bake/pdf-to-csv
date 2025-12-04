/**
 * Custom hook for managing conversion page logic
 * Consolidates all the repeated logic from conversion pages
 */

import { useState, useEffect, useCallback } from "react";
import { useUploadStore } from "@/store/uploadStore";
import { useUpload } from "@/hooks/useUpload";
import { useConversion, useConversionStatus } from "@/hooks/useConversion";
import { api } from "@/lib/api";
import { OutputFormat } from "@/lib/conversionConfig";

interface UseConversionPageProps {
  outputFormat: OutputFormat;
  fileExtension: string;
}

export function useConversionPage({
  outputFormat,
  fileExtension,
}: UseConversionPageProps) {
  const {
    files,
    parser,
    merge,
    currentJobId,
    addFiles,
    updateFile,
    removeFile,
    clearFiles,
    setParser,
    setMerge,
    setCurrentJobId,
    markAllAsConverting,
    markAllAsCompleted,
  } = useUploadStore();

  const {
    upload,
    uploading,
    progress,
    error: uploadError,
  } = useUpload({
    onSuccess: (tempFileId, serverResponse) => {
      updateFile(tempFileId, {
        fileId: serverResponse.fileId,
        status: "uploaded",
        progress: 100,
      });
    },
    onError: (fileId, error) => {
      updateFile(fileId, {
        status: "error",
        error: error.message,
      });
    },
    onProgress: (fileId, progress) => {
      updateFile(fileId, { progress });
    },
  });

  const { startConversion, converting } = useConversion();
  const { data: conversionStatus } = useConversionStatus(currentJobId, {
    enabled: !!currentJobId,
    onComplete: () => {
      markAllAsCompleted();
    },
  });

  const [error, setError] = useState<string | null>(null);

  // Handle conversion status updates
  useEffect(() => {
    if (conversionStatus) {
      const { status } = conversionStatus;
      const statusMessage = conversionStatus.message || conversionStatus.error;

      if (status === "completed") {
        markAllAsCompleted();
        setCurrentJobId(null);
      } else if (status === "error") {
        files.forEach((file) => {
          if (file.status === "converting") {
            updateFile(file.fileId, {
              status: "error",
              error: statusMessage || "Conversion failed",
            });
          }
        });
        setCurrentJobId(null);
      }
    }
  }, [
    conversionStatus,
    files,
    markAllAsCompleted,
    updateFile,
    setCurrentJobId,
  ]);

  // Handle file selection and upload
  const onFilesSelected = useCallback(
    async (selectedFiles: File[]) => {
      setError(null);

      const newFiles = selectedFiles.map((file) => ({
        fileId: `${Date.now()}-${file.name}`,
        fileName: file.name,
        fileSize: file.size,
        status: "uploading" as const,
        progress: 0,
      }));

      addFiles(newFiles);

      for (const [index, file] of selectedFiles.entries()) {
        try {
          await upload(file, newFiles[index].fileId);
        } catch (err) {
          console.error("Upload error:", err);
        }
      }
    },
    [addFiles, upload]
  );

  // Handle conversion
  const onConvert = useCallback(async () => {
    setError(null);

    const uploadedFiles = files.filter((f) => f.status === "uploaded");

    if (uploadedFiles.length === 0) {
      setError("Please upload files before converting");
      return;
    }

    try {
      markAllAsConverting();

      const conversionParams: any = {
        fileIds: uploadedFiles.map((f) => f.fileId),
        parser,
        merge,
      };

      // Only add outputFormat if it's not CSV (default)
      if (outputFormat !== "csv") {
        conversionParams.outputFormat = outputFormat;
      }

      const result = await startConversion(conversionParams);

      if (result?.jobId) {
        setCurrentJobId(result.jobId);
      } else {
        throw new Error("Failed to start conversion");
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to start conversion"
      );
      files.forEach((file) => {
        if (file.status === "converting") {
          updateFile(file.fileId, {
            status: "uploaded",
            progress: 100,
          });
        }
      });
    }
  }, [
    files,
    parser,
    merge,
    outputFormat,
    markAllAsConverting,
    startConversion,
    setCurrentJobId,
    updateFile,
  ]);

  // Handle file removal
  const onRemoveFile = useCallback(
    (fileId: string) => {
      removeFile(fileId);
    },
    [removeFile]
  );

  // Handle clear all files
  const onClearAll = useCallback(() => {
    clearFiles();
    setError(null);
  }, [clearFiles]);

  // Handle single file download
  const onDownloadFile = useCallback(
    async (fileId: string) => {
      const file = files.find((f) => f.fileId === fileId);
      if (!file) return;

      try {
        await api.download(
          file.fileId,
          file.fileName.replace(".pdf", fileExtension)
        );
      } catch (err) {
        console.error("Download error:", err);
        setError("Failed to download file");
      }
    },
    [files, fileExtension]
  );

  // Handle download all files
  const onDownloadAll = useCallback(async () => {
    const completedFiles = files.filter((f) => f.status === "completed");

    if (completedFiles.length === 0) {
      setError("No files available to download");
      return;
    }

    try {
      if (completedFiles.length === 1) {
        // Single file: download directly
        const file = completedFiles[0];
        await api.download(
          file.fileId,
          file.fileName.replace(".pdf", fileExtension)
        );
      } else {
        // Multiple files: download as ZIP with original names
        const fileIds = completedFiles.map((f) => f.fileId);
        const fileNames = completedFiles.reduce((acc, f) => {
          acc[f.fileId] = f.fileName.replace(".pdf", fileExtension);
          return acc;
        }, {} as Record<string, string>);
        await api.downloadBatch(fileIds, fileNames);
      }
    } catch (err) {
      console.error("Download error:", err);
      setError("Failed to download files");
    }
  }, [files, fileExtension]);

  // Computed values
  const completedFiles = files.filter((f) => f.status === "completed");
  const uploadedFiles = files.filter((f) => f.status === "uploaded");
  const hasFiles = files.length > 0;

  return {
    // State
    files,
    parser,
    merge,
    currentJobId,
    conversionStatus,
    error,
    uploading,
    converting,
    completedFiles,
    uploadedFiles,
    hasFiles,
    progress,

    // Actions
    onFilesSelected,
    onConvert,
    onRemoveFile,
    onClearAll,
    onDownloadFile,
    onDownloadAll,
    setParser,
    setMerge,
  };
}
