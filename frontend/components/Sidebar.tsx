"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { 
    LayoutDashboard, 
    Briefcase,
    MessageSquare,
    History,
    PieChart,
    Settings,
    LogOut,
    Info,
    Shield
} from "lucide-react";

export default function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();

    if (pathname === "/login" || pathname === "/register") return null;

    const navItems = [
        { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
        { name: "Scan Job", href: "/scan", icon: Briefcase },
        { name: "Message Analyzer", href: "/messages", icon: MessageSquare },
        { name: "History", href: "/history", icon: History },
        { name: "Reports", href: "/reports", icon: PieChart },
        { name: "Settings", href: "/settings", icon: Settings },
        { name: "About", href: "/about", icon: Info },
    ];

    const handleLogout = async () => {
        try {
            await fetch("http://localhost:8000/api/logout", { method: "POST" });
        } catch (e) {}
        document.cookie = "jobx_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        router.push("/login");
    };

    return (
        <motion.div 
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            className="w-[260px] bg-white h-screen fixed top-0 left-0 flex flex-col z-40 border-r border-[#E5E7EB] font-sans"
        >
            <div className="p-6 pb-4 flex items-center gap-3">
                <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center text-white">
                    <Shield className="w-4 h-4" />
                </div>
                <span className="text-[16px] font-bold text-[#111111] tracking-tight">JOBX</span>
            </div>

            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1.5 no-scrollbar">
                
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link key={item.name} href={item.href}>
                            <motion.div
                                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer transition-all duration-150 ${
                                    isActive 
                                    ? "bg-black text-white shadow-md font-medium" 
                                    : "text-[#6B7280] hover:bg-gray-100 hover:text-[#111111] font-medium"
                                }`}
                            >
                                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-[#6B7280]"}`} />
                                <span className="text-[13px]">{item.name}</span>
                            </motion.div>
                        </Link>
                    );
                })}
            </div>

            <div className="p-4 border-t border-[#E5E7EB]">
                <button 
                    onClick={handleLogout}
                    className="flex w-full items-center gap-3 px-3 py-2.5 rounded-lg text-[#6B7280] font-medium hover:bg-gray-100 hover:text-[#111111] transition-all text-[13px]"
                >
                    <LogOut className="w-4 h-4" />
                    Sign out
                </button>
            </div>
        </motion.div>
    );
}
