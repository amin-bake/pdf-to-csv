"use client";

import { useState, useEffect } from "react";
import { FileUploader } from "@/components/upload/FileUploader";
import { FileCard } from "@/components/upload/FileCard";
import { ConversionStatus } from "@/components/conversion/ConversionStatus";
import { DownloadButton } from "@/components/download/DownloadButton";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useUploadStore } from "@/store/uploadStore";
import { useUpload } from "@/hooks/useUpload";
import { useConversion, useConversionStatus } from "@/hooks/useConversion";
import { Download, FileDown, Trash2, AlertCircle } from "lucide-react";

export default function Home() {
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
    onSuccess: (file) => {
      updateFile(file.fileId, {
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

  // Update file statuses based on conversion status
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

  const handleFilesSelected = async (selectedFiles: File[]) => {
    setError(null);

    // Create file objects
    const newFiles = selectedFiles.map((file) => ({
      fileId: `${Date.now()}-${file.name}`,
      fileName: file.name,
      fileSize: file.size,
      status: "uploading" as const,
      progress: 0,
    }));

    addFiles(newFiles);

    // Upload each file
    for (const [index, file] of selectedFiles.entries()) {
      try {
        await upload(file, newFiles[index].fileId);
      } catch (err) {
        // Error handled in hook callback
        console.error("Upload error:", err);
      }
    }
  };

  const handleConvert = async () => {
    setError(null);

    const uploadedFiles = files.filter((f) => f.status === "uploaded");

    if (uploadedFiles.length === 0) {
      setError("Please upload files before converting");
      return;
    }

    try {
      markAllAsConverting();

      const result = await startConversion({
        fileIds: uploadedFiles.map((f) => f.fileId),
        parser,
        merge,
      });

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
  };

  const handleRemoveFile = (fileId: string) => {
    removeFile(fileId);
  };

  const handleClearAll = () => {
    clearFiles();
    setError(null);
  };

  const handleDownloadAll = async () => {
    const completedFiles = files.filter((f) => f.status === "completed");

    if (completedFiles.length === 0) {
      setError("No files available to download");
      return;
    }

    // Download each file individually
    for (const file of completedFiles) {
      try {
        const blob = await fetch(`/api/download/${file.fileId}`).then((r) =>
          r.blob()
        );
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = file.fileName.replace(".pdf", ".csv");
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (err) {
        console.error("Download error:", err);
      }
    }
  };

  const completedFiles = files.filter((f) => f.status === "completed");
  const uploadedFiles = files.filter((f) => f.status === "uploaded");
  const hasFiles = files.length > 0;

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-2">PDF to CSV Converter</h1>
        <p className="text-muted-foreground">
          Upload PDF files and convert them to CSV with advanced extraction
        </p>
      </div>

      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Left Column: Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle>Upload Files</CardTitle>
            <CardDescription>
              Select or drag PDF files to upload (max 50MB per file)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <FileUploader
              onFilesSelected={handleFilesSelected}
              maxFiles={10}
              maxFileSize={50 * 1024 * 1024}
              disabled={uploading || converting}
            />

            {/* Parser Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Parser Type</label>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant={parser === "pdfplumber" ? "default" : "outline"}
                  onClick={() => setParser("pdfplumber")}
                  disabled={converting}
                  className="flex-1"
                >
                  PDFPlumber
                </Button>
                <Button
                  type="button"
                  variant={parser === "tabula" ? "default" : "outline"}
                  onClick={() => setParser("tabula")}
                  disabled={converting}
                  className="flex-1"
                >
                  Tabula
                </Button>
              </div>
            </div>

            {/* Merge Option */}
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="merge"
                checked={merge}
                onChange={(e) => setMerge(e.target.checked)}
                disabled={converting}
                className="h-4 w-4 rounded border-gray-300"
              />
              <label htmlFor="merge" className="text-sm font-medium">
                Merge all PDFs into single CSV
              </label>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 pt-2">
              <Button
                onClick={handleConvert}
                disabled={uploadedFiles.length === 0 || converting || uploading}
                className="flex-1"
              >
                <FileDown className="mr-2 h-4 w-4" />
                Convert to CSV
              </Button>
              {hasFiles && (
                <Button
                  variant="outline"
                  onClick={handleClearAll}
                  disabled={converting || uploading}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Right Column: Status Section */}
        <Card>
          <CardHeader>
            <CardTitle>Conversion Status</CardTitle>
            <CardDescription>
              Track the progress of your conversions
            </CardDescription>
          </CardHeader>
          <CardContent>
            {currentJobId && conversionStatus ? (
              <ConversionStatus
                status={conversionStatus.status}
                message={conversionStatus.message}
                progress={conversionStatus.progress}
              />
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                {hasFiles
                  ? 'Click "Convert to CSV" to start processing'
                  : "Upload files to get started"}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Files List */}
      {hasFiles && (
        <Card className="mt-6">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Files ({files.length})</CardTitle>
              <CardDescription>Uploaded and converted files</CardDescription>
            </div>
            {completedFiles.length > 0 && (
              <Button onClick={handleDownloadAll} variant="outline" size="sm">
                <Download className="mr-2 h-4 w-4" />
                Download All ({completedFiles.length})
              </Button>
            )}
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {files.map((file) => (
                <FileCard
                  key={file.fileId}
                  file={file}
                  onRemove={() => handleRemoveFile(file.fileId)}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
