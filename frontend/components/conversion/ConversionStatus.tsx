"use client";

import { Loader2, CheckCircle2, XCircle } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";

interface ConversionStatusProps {
  status:
    | "idle"
    | "pending"
    | "processing"
    | "converting"
    | "completed"
    | "error";
  message?: string;
  progress?: number;
}

export function ConversionStatus({
  status,
  message,
  progress,
}: ConversionStatusProps) {
  if (status === "idle") {
    return null;
  }

  if (status === "error") {
    return (
      <Alert variant="destructive">
        <XCircle className="h-4 w-4" />
        <AlertDescription>
          {message || "Conversion failed. Please try again."}
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        {status === "completed" ? (
          <CheckCircle2 className="h-5 w-5 text-green-500" />
        ) : (
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
        )}
        <span className="font-medium capitalize">
          {status === "pending" || status === "processing"
            ? "Converting"
            : status}
        </span>
      </div>

      {message && <p className="text-sm text-muted-foreground">{message}</p>}

      {progress !== undefined && progress > 0 && (
        <Progress value={progress} className="h-2" />
      )}
    </div>
  );
}
