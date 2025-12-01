"use client";

import { Download, X, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { formatFileSize } from "@/lib/utils";
import type { UploadedFile } from "./FileUploader";

interface FileCardProps {
  file: UploadedFile;
  onDownload?: (fileId: string) => void;
  onRemove?: (fileId: string) => void;
  disabled?: boolean;
}

export function FileCard({
  file,
  onDownload,
  onRemove,
  disabled = false,
}: FileCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-500 text-white";
      case "error":
        return "bg-red-500 text-white";
      case "converting":
        return "bg-blue-500 text-white";
      case "uploading":
        return "bg-yellow-500 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-4">
          {/* File Info */}
          <div className="flex items-start gap-3 flex-1 min-w-0">
            <FileText className="h-5 w-5 text-muted-foreground mt-1 shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{file.fileName}</p>
              <p className="text-sm text-muted-foreground">
                {formatFileSize(file.fileSize)}
              </p>
            </div>
          </div>

          {/* Status Badge */}
          <Badge className={getStatusColor(file.status)}>{file.status}</Badge>

          {/* Actions */}
          <div className="flex gap-2 shrink-0">
            {file.status === "completed" && (
              <Button
                size="sm"
                onClick={() => onDownload?.(file.fileId)}
                disabled={disabled}
              >
                <Download className="h-4 w-4 mr-1" />
                Download
              </Button>
            )}
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onRemove?.(file.fileId)}
              disabled={disabled}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Progress Bar */}
        {(file.status === "uploading" || file.status === "converting") && (
          <div className="mt-3">
            <Progress value={file.progress} className="h-2" />
            <p className="text-xs text-muted-foreground mt-1">
              {file.progress}%
            </p>
          </div>
        )}

        {/* Error Message */}
        {file.status === "error" && file.error && (
          <p className="text-sm text-red-500 mt-2">{file.error}</p>
        )}
      </CardContent>
    </Card>
  );
}
