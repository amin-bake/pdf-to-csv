"use client";

import { useState } from "react";
import { Download, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DownloadButtonProps {
  fileId: string;
  fileName?: string;
  variant?: "default" | "outline" | "ghost";
  size?: "default" | "sm" | "lg";
  disabled?: boolean;
}

export function DownloadButton({
  fileId,
  fileName = "download.csv",
  variant = "default",
  size = "default",
  disabled = false,
}: DownloadButtonProps) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      // Simulate download - will connect to API later
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log("Downloading file:", fileId, fileName);
    } catch (error) {
      console.error("Download failed:", error);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Button
      variant={variant}
      size={size}
      onClick={handleDownload}
      disabled={disabled || downloading}
    >
      {downloading ? (
        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
      ) : (
        <Download className="h-4 w-4 mr-2" />
      )}
      {downloading ? "Downloading..." : "Download"}
    </Button>
  );
}
