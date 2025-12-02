"use client";

import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileText, Table, FileSpreadsheet, ArrowRight } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";

const conversionTypes = [
  {
    id: "pdf-to-csv",
    title: "PDF to CSV",
    description: "Extract tables from PDF files and convert to CSV format",
    icon: Table,
    href: "/convert/pdf-to-csv",
    available: true,
  },
  {
    id: "pdf-to-excel",
    title: "PDF to Excel",
    description: "Convert PDF documents to Excel spreadsheets",
    icon: FileSpreadsheet,
    href: "/convert/pdf-to-excel",
    available: false,
  },
  {
    id: "pdf-to-json",
    title: "PDF to JSON",
    description: "Extract structured data from PDFs as JSON",
    icon: FileText,
    href: "/convert/pdf-to-json",
    available: false,
  },
  {
    id: "pdf-to-text",
    title: "PDF to Text",
    description: "Extract all text content from PDF files",
    icon: FileText,
    href: "/convert/pdf-to-text",
    available: false,
  },
];

export default function Home() {
  return (
    <div className="relative min-h-screen">
      {/* Header with Theme Toggle */}
      <header className="container mx-auto px-4 py-4 max-w-7xl">
        <div className="flex justify-end">
          <ThemeToggle />
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-linear-to-r from-hunter-green to-fern bg-clip-text text-transparent">
            File Conversion Suite
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Convert your files instantly with our powerful conversion tools.
            Fast, secure, and easy to use.
          </p>
        </div>

        {/* Conversion Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {conversionTypes.map((conversion) => {
            const Icon = conversion.icon;
            return (
              <Link
                key={conversion.id}
                href={conversion.available ? conversion.href : "#"}
                className={`group ${
                  !conversion.available ? "pointer-events-none" : ""
                }`}
              >
                <Card
                  className={`h-full transition-all duration-300 hover:shadow-lg hover:-translate-y-1 ${
                    conversion.available
                      ? "border-border hover:border-fern"
                      : "opacity-60 bg-muted/50"
                  }`}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between mb-2">
                      <div
                        className={`p-3 rounded-lg ${
                          conversion.available
                            ? "bg-fern/10 text-fern"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        <Icon className="h-6 w-6" />
                      </div>
                      {conversion.available && (
                        <ArrowRight className="h-5 w-5 text-muted-foreground group-hover:text-fern group-hover:translate-x-1 transition-all" />
                      )}
                      {!conversion.available && (
                        <span className="text-xs bg-muted px-2 py-1 rounded-full text-muted-foreground">
                          Coming Soon
                        </span>
                      )}
                    </div>
                    <CardTitle className="text-xl">
                      {conversion.title}
                    </CardTitle>
                    <CardDescription>{conversion.description}</CardDescription>
                  </CardHeader>
                  {conversion.available && (
                    <CardContent>
                      <div className="text-sm text-fern font-medium group-hover:underline">
                        Start Converting →
                      </div>
                    </CardContent>
                  )}
                </Card>
              </Link>
            );
          })}
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="text-center">
            <div className="w-12 h-12 rounded-full bg-fern/10 flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 text-fern"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Lightning Fast</h3>
            <p className="text-muted-foreground text-sm">
              Process your files in seconds with our optimized conversion engine
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 rounded-full bg-fern/10 flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 text-fern"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Secure & Private</h3>
            <p className="text-muted-foreground text-sm">
              Your files are processed securely and deleted after conversion
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 rounded-full bg-fern/10 flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 text-fern"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">High Quality</h3>
            <p className="text-muted-foreground text-sm">
              Advanced algorithms ensure accurate and reliable conversions
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
