import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PDF to CSV Converter",
  description: "Convert PDF tables to CSV files with ease",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {/* Animated Background */}
        <div className="fixed inset-0 -z-10 bg-background">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#3a5a4015_1px,transparent_1px),linear-gradient(to_bottom,#3a5a4015_1px,transparent_1px)] bg-size-[14px_24px]" />
          <div className="absolute left-1/2 top-0 -translate-x-1/2 h-[600px] w-[600px] rounded-full bg-[radial-gradient(circle_300px_at_50%_300px,#58815730,transparent)]" />
        </div>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
