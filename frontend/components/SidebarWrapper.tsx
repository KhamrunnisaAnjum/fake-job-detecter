"use client";

import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";

export default function SidebarWrapper() {
  const pathname = usePathname();
  
  // Hide sidebar on login page
  if (pathname === "/login") {
    return null;
  }

  return <Sidebar />;
}
