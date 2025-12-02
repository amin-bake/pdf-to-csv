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
          <div
            className="absolute inset-0 opacity-[0.08]"
            style={{
              backgroundImage:
                "linear-gradient(to right, var(--color-primary) 1px, transparent 1px), linear-gradient(to bottom, var(--color-primary) 1px, transparent 1px)",
              backgroundSize: "14px 24px",
            }}
          />
          <div
            className="absolute left-1/2 top-0 -translate-x-1/2 h-[600px] w-[600px] rounded-full opacity-20"
            style={{
              background:
                "radial-gradient(circle 300px at 50% 300px, var(--color-accent), transparent)",
            }}
          />
        </div>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
