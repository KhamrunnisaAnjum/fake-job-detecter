import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import SidebarWrapper from "@/components/SidebarWrapper";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  title: "JOBX",
  description: "Advanced AI Threat Detection",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-[#F5F5F4] text-[#111111] antialiased min-h-screen overflow-x-hidden selection:bg-black selection:text-white`}>
        <div className="flex">
            <SidebarWrapper />
            <main className="flex-1 lg:pl-[260px] min-h-screen relative">
                <div className="w-full max-w-[1600px] mx-auto p-8">
                    {children}
                </div>
            </main>
        </div>
      </body>
    </html>
  );
}
