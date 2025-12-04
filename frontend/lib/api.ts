// Microservices URLs
const UPLOAD_SERVICE_URL =
  process.env.NEXT_PUBLIC_UPLOAD_SERVICE_URL || "http://localhost:5001";
const CONVERSION_SERVICE_URL =
  process.env.NEXT_PUBLIC_CONVERSION_SERVICE_URL || "http://localhost:5002";
const DOWNLOAD_SERVICE_URL =
  process.env.NEXT_PUBLIC_DOWNLOAD_SERVICE_URL || "http://localhost:5003";

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp?: string;
}

async function apiRequest<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result: ApiResponse<T> = await response.json();

  if (!result.success) {
    throw new Error(result.error?.message || "Request failed");
  }

  return result.data!;
}

export interface UploadResponse {
  fileId: string;
  filename: string;
  size: number;
  uploadedAt: string;
}

export interface ConversionResponse {
  jobId: string;
  status: string;
  message: string;
}

export interface StatusResponse {
  jobId: string;
  status: "pending" | "processing" | "converting" | "completed" | "error";
  progress: number;
  message?: string;
  currentFile?: string;
  error?: string;
  convertedFiles?: Array<{
    fileId: string;
    filename: string;
    size: number;
  }>;
  errors?: string[];
}

export const api = {
  upload: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    return apiRequest(`${UPLOAD_SERVICE_URL}/api/upload`, {
      method: "POST",
      body: formData,
    });
  },

  convert: async (params: {
    fileIds: string[];
    parser: "pdfplumber" | "tabula";
    merge: boolean;
    outputFormat?: "csv" | "excel" | "json" | "text";
  }): Promise<ConversionResponse> => {
    return apiRequest(`${CONVERSION_SERVICE_URL}/api/convert`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
  },

  getStatus: async (jobId: string): Promise<StatusResponse> => {
    return apiRequest(`${CONVERSION_SERVICE_URL}/api/status/${jobId}`);
  },

  download: async (fileId: string, fileName?: string): Promise<void> => {
    const response = await fetch(
      `${DOWNLOAD_SERVICE_URL}/api/download/${fileId}`
    );

    if (!response.ok) {
      throw new Error(`Download failed: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName || "download.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  downloadBatch: async (
    fileIds: string[],
    fileNames?: Record<string, string>
  ): Promise<void> => {
    const response = await fetch(`${DOWNLOAD_SERVICE_URL}/api/download/batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fileIds, fileNames }),
    });

    if (!response.ok) {
      throw new Error(`Batch download failed: ${response.status}`);
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "converted-files.zip";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },
};
