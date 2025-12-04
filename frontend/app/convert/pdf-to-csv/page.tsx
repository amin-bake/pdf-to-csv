"use client";

import { ConversionPageLayout } from "@/components/conversion/ConversionPageLayout";
import { useConversionPage } from "@/hooks/useConversionPage";
import { getConversionConfig } from "@/lib/conversionConfig";

export default function PdfToCsvPage() {
  const config = getConversionConfig("csv");
  const conversionPageProps = useConversionPage({
    outputFormat: config.format,
    fileExtension: config.fileExtension,
  });

  return (
    <ConversionPageLayout
      config={config}
      {...conversionPageProps}
      onParserChange={conversionPageProps.setParser}
      onMergeChange={conversionPageProps.setMerge}
    />
  );
}
