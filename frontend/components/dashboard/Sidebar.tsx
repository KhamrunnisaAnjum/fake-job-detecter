"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  FiHome,
  FiSearch,
  FiMessageSquare,
  FiClock,
  FiPieChart,
  FiFileText,
  FiSettings,
  FiInfo,
  FiLogOut,
} from "react-icons/fi";

const menu = [
  {
    title: "Dashboard",
    icon: FiHome,
    href: "/dashboard",
  },
  {
    title: "Scan New Job",
    icon: FiSearch,
    href: "/scan",
  },
  {
    title: "Message Analyzer",
    icon: FiMessageSquare,
    href: "/analyzer",
  },
  {
    title: "My History",
    icon: FiClock,
    href: "/history",
  },
  {
    title: "Risk Distribution",
    icon: FiPieChart,
    href: "/reports",
  },
  {
    title: "My Reports",
    icon: FiFileText,
    href: "/reports",
  },
  {
    title: "Settings",
    icon: FiSettings,
    href: "/settings",
  },
  {
    title: "About",
    icon: FiInfo,
    href: "/about",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-72 min-h-screen bg-white border-r border-neutral-200 flex flex-col justify-between">
      <div>
        <div className="px-8 pt-8 pb-10">
          <h1 className="text-3xl font-bold">
            JobX
            <span className="text-neutral-400"></span>
          </h1>

          <p className="text-sm text-neutral-500 mt-1">Fake Job Detector</p>
        </div>

        <nav className="px-4 space-y-2">
          {menu.map((item) => {
            const Icon = item.icon;

            const active = pathname === item.href;

            return (
              <Link
                key={item.title}
                href={item.href}
                className={`flex items-center gap-4 rounded-2xl px-5 py-4 transition

                ${
                  active
                    ? "bg-black text-white shadow-lg"
                    : "text-neutral-600 hover:bg-neutral-100"
                }

                `}
              >
                <Icon size={20} />

                <span className="font-medium">{item.title}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="border-t border-neutral-200 p-6">
        <div className="mb-5 flex items-center gap-3">
          <div className="h-12 w-12 rounded-full bg-black flex items-center justify-center text-white font-bold">
            A
          </div>

          <div>
            <h3 className="font-semibold">Abdul Rehman</h3>

            <p className="text-sm text-neutral-500">Premium User</p>
          </div>
        </div>

        <button className="flex w-full items-center justify-center gap-3 rounded-2xl border border-neutral-200 py-3 hover:bg-neutral-100 transition">
          <FiLogOut />
          Logout
        </button>
      </div>
    </aside>
  );
}
