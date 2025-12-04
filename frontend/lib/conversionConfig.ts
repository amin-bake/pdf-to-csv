/**
 * Configuration types and utilities for PDF conversion pages
 */

export type OutputFormat = "csv" | "excel" | "json" | "text";

export interface ConversionConfig {
  format: OutputFormat;
  title: string;
  description: string;
  fileExtension: string;
  buttonText: string;
}

export const conversionConfigs: Record<OutputFormat, ConversionConfig> = {
  csv: {
    format: "csv",
    title: "PDF to CSV Converter",
    description: "Upload PDF files and convert tables to CSV format",
    fileExtension: ".csv",
    buttonText: "Convert to CSV",
  },
  excel: {
    format: "excel",
    title: "PDF to Excel Converter",
    description: "Upload PDF files and convert tables to Excel format",
    fileExtension: ".xlsx",
    buttonText: "Convert to Excel",
  },
  json: {
    format: "json",
    title: "PDF to JSON Converter",
    description: "Upload PDF files and convert tables to JSON format",
    fileExtension: ".json",
    buttonText: "Convert to JSON",
  },
  text: {
    format: "text",
    title: "PDF to Text Converter",
    description: "Upload PDF files and extract text content",
    fileExtension: ".txt",
    buttonText: "Convert to Text",
  },
};

export function getConversionConfig(format: OutputFormat): ConversionConfig {
  return conversionConfigs[format];
}
