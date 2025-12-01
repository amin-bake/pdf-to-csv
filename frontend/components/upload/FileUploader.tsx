"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload } from "lucide-react";
import { cn } from "@/lib/utils";

export interface UploadedFile {
  fileId: string;
  fileName: string;
  fileSize: number;
  status: "uploading" | "uploaded" | "converting" | "completed" | "error";
  progress: number;
  error?: string;
}

interface FileUploaderProps {
  onFilesSelected?: (files: File[]) => void;
  onUploadError?: (error: Error) => void;
  maxFiles?: number;
  maxFileSize?: number;
  acceptedTypes?: string[];
  disabled?: boolean;
}

export function FileUploader({
  onFilesSelected,
  onUploadError,
  maxFiles = 10,
  maxFileSize = 50 * 1024 * 1024, // 50MB
  disabled = false,
}: FileUploaderProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      setFiles(acceptedFiles);
      setUploading(true);

      try {
        onFilesSelected?.(acceptedFiles);
        setUploading(false);
      } catch (error) {
        onUploadError?.(error as Error);
        setUploading(false);
      }
    },
    [onFilesSelected, onUploadError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    maxFiles,
    maxSize: maxFileSize,
    disabled: disabled || uploading,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors",
        "hover:border-primary/50 hover:bg-primary/5",
        isDragActive && "border-primary bg-primary/10",
        (disabled || uploading) &&
          "opacity-50 cursor-not-allowed pointer-events-none"
      )}
    >
      <input {...getInputProps()} />
      <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
      <p className="text-lg font-medium mb-2">
        {isDragActive ? "Drop files here" : "Drag & drop PDF files here"}
      </p>
      <p className="text-sm text-muted-foreground">
        or click to browse (max {maxFiles} files, {maxFileSize / 1024 / 1024}MB
        each)
      </p>
      {uploading && (
        <p className="text-sm text-primary mt-4 animate-pulse">Uploading...</p>
      )}
    </div>
  );
}
