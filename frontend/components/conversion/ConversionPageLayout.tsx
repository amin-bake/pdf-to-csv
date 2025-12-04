/**
 * Reusable layout component for PDF conversion pages
 * Provides consistent UI structure across all conversion types
 */

"use client";

import { FileUploader } from "@/components/upload/FileUploader";
import { FileCard } from "@/components/upload/FileCard";
import { ConversionStatus } from "@/components/conversion/ConversionStatus";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Download,
  FileDown,
  Trash2,
  AlertCircle,
  ArrowLeft,
} from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import { ColorThemeSelector } from "@/components/color-theme-selector";
import { ConversionConfig } from "@/lib/conversionConfig";

export type ParserType = "pdfplumber" | "tabula";

interface ConversionPageLayoutProps {
  config: ConversionConfig;
  files: any[];
  parser: ParserType;
  merge: boolean;
  currentJobId: string | null;
  conversionStatus: any;
  error: string | null;
  uploading: boolean;
  converting: boolean;
  completedFiles: any[];
  uploadedFiles: any[];
  hasFiles: boolean;
  onFilesSelected: (files: File[]) => void;
  onConvert: () => void;
  onRemoveFile: (fileId: string) => void;
  onClearAll: () => void;
  onDownloadFile: (fileId: string) => void;
  onDownloadAll: () => void;
  onParserChange: (parser: ParserType) => void;
  onMergeChange: (merge: boolean) => void;
}

export function ConversionPageLayout({
  config,
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
  onFilesSelected,
  onConvert,
  onRemoveFile,
  onClearAll,
  onDownloadFile,
  onDownloadAll,
  onParserChange,
  onMergeChange,
}: ConversionPageLayoutProps) {
  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header with Theme Toggle */}
      <div className="flex justify-end gap-2 mb-4">
        <ColorThemeSelector />
        <ThemeToggle />
      </div>

      <div className="mb-8">
        <Link
          href="/"
          className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-4"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Home
        </Link>
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2">{config.title}</h1>
          <p className="text-muted-foreground">{config.description}</p>
        </div>
      </div>

      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Upload Files</CardTitle>
            <CardDescription>
              Select or drag PDF files to upload (max 50MB per file)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <FileUploader
              onFilesSelected={onFilesSelected}
              maxFiles={10}
              maxFileSize={50 * 1024 * 1024}
              disabled={uploading || converting}
            />

            <div className="space-y-2">
              <label className="text-sm font-medium">Parser Type</label>
              <div className="flex gap-2">
                <Button
                  type="button"
                  variant={parser === "pdfplumber" ? "default" : "outline"}
                  onClick={() => onParserChange("pdfplumber")}
                  disabled={converting}
                  className="flex-1"
                >
                  PDFPlumber
                </Button>
                <Button
                  type="button"
                  variant={parser === "tabula" ? "default" : "outline"}
                  onClick={() => onParserChange("tabula")}
                  disabled={converting}
                  className="flex-1"
                >
                  Tabula
                </Button>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="merge"
                checked={merge}
                onChange={(e) => onMergeChange(e.target.checked)}
                disabled={converting}
                className="h-4 w-4 rounded border-gray-300 accent-accent"
              />
              <label htmlFor="merge" className="text-sm font-medium">
                Merge all PDFs into single {config.format.toUpperCase()}
              </label>
            </div>

            <div className="flex gap-2 pt-2">
              <Button
                onClick={onConvert}
                disabled={uploadedFiles.length === 0 || converting || uploading}
                className="flex-1"
              >
                <FileDown className="mr-2 h-4 w-4" />
                {config.buttonText}
              </Button>
              {hasFiles && (
                <Button
                  variant="outline"
                  onClick={onClearAll}
                  disabled={converting || uploading}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

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
                  ? `Click "${config.buttonText}" to start processing`
                  : "Upload files to get started"}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {hasFiles && (
        <Card className="mt-6">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Files ({files.length})</CardTitle>
              <CardDescription>Uploaded and converted files</CardDescription>
            </div>
            {completedFiles.length > 0 && (
              <Button onClick={onDownloadAll} variant="outline" size="sm">
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
                  onDownload={onDownloadFile}
                  onRemove={() => onRemoveFile(file.fileId)}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
