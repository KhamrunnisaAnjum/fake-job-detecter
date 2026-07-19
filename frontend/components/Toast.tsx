"use client";

import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, AlertCircle, X } from "lucide-react";
import { useEffect } from "react";

export type ToastType = "success" | "error" | "info";

export interface ToastProps {
    message: string;
    type: ToastType;
    onClose: () => void;
}

export default function Toast({ message, type, onClose }: ToastProps) {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose();
        }, 5000);
        return () => clearTimeout(timer);
    }, [onClose]);

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, y: 50, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 20, scale: 0.9 }}
                className={`fixed bottom-6 right-6 flex items-center gap-3 px-5 py-3.5 rounded-xl shadow-lg border z-50 ${
                    type === "success" ? "bg-[#F0FDF4] border-[#BBF7D0] text-[#166534]" :
                    type === "error" ? "bg-[#FEF2F2] border-[#FECACA] text-[#991B1B]" :
                    "bg-white border-[#E5E7EB] text-[#111111]"
                }`}
            >
                {type === "success" && <CheckCircle2 className="w-5 h-5 text-[#22C55E]" />}
                {type === "error" && <AlertCircle className="w-5 h-5 text-[#EF4444]" />}
                
                <span className="text-sm font-medium pr-4">{message}</span>
                
                <button onClick={onClose} className="p-1 hover:bg-black/5 rounded-full transition-colors ml-auto">
                    <X className="w-4 h-4 opacity-50" />
                </button>
            </motion.div>
        </AnimatePresence>
    );
}
