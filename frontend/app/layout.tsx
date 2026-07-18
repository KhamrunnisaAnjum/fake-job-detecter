import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "JobX AI | Fake Job Detection",
  description: "Detect fake job advertisements using Machine Learning.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-screen flex bg-[#f8f9fa] text-gray-900 font-sans">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8">
            <div className="mx-auto max-w-7xl h-full">
                {children}
            </div>
        </main>
      </body>
    </html>
  );
}
