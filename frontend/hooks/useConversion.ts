import { useMutation, useQuery } from "@tanstack/react-query";
import { api, type ConversionResponse, type StatusResponse } from "@/lib/api";

interface ConversionOptions {
  onSuccess?: (data: ConversionResponse) => void;
  onError?: (error: Error) => void;
}

export function useConversion(options?: ConversionOptions) {
  const mutation = useMutation({
    mutationFn: async (params: {
      fileIds: string[];
      parser: "pdfplumber" | "tabula";
      merge: boolean;
      outputFormat?: "csv" | "excel" | "json" | "text";
    }) => {
      return api.convert(params);
    },
    onSuccess: options?.onSuccess,
    onError: options?.onError,
  });

  return {
    startConversion: mutation.mutateAsync,
    converting: mutation.isPending,
    error: mutation.error,
  };
}

interface StatusOptions {
  enabled?: boolean;
  pollingInterval?: number;
  onComplete?: (data: StatusResponse) => void;
}

export function useConversionStatus(
  jobId: string | null,
  options?: StatusOptions
) {
  const query = useQuery({
    queryKey: ["conversion-status", jobId],
    queryFn: () => api.getStatus(jobId!),
    enabled: Boolean(jobId) && options?.enabled !== false,
    refetchInterval: (query) => {
      const data = query.state.data;
      // Stop polling when completed or error
      if (data?.status === "completed" || data?.status === "error") {
        if (data.status === "completed") {
          options?.onComplete?.(data);
        }
        return false;
      }
      return options?.pollingInterval ?? 1000;
    },
  });

  return {
    data: query.data,
    isLoading: query.isLoading,
    error: query.error,
  };
}
