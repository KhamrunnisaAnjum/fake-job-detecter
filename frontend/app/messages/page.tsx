"use client";
import { apiFetch } from "@/utils/api";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
    AlertTriangle, 
    Search, 
    CheckCircle2,
    XCircle,
    Info,
    MessageSquare
} from "lucide-react";

export default function MessageAnalyzerPage() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [message, setMessage] = useState("");
    const [source, setSource] = useState("WhatsApp");

    const handleScan = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const res = await apiFetch("http://127.0.0.1:8000/analyze-message", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, source })
            });
            if (!res.ok) {
                const errorData = await res.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP Error ${res.status}`);
            }
            const data = await res.json();
            setResult(data);
        } catch (error) {
            console.error("API Error", error);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (risk: string) => {
        if (risk === "High Risk") return "#DC2626"; // Danger
        if (risk === "Medium Risk") return "#F59E0B"; // Warning
        return "#16A34A"; // Success
    };

    return (
        <div className="w-full flex flex-col xl:flex-row gap-6 items-start">
            
            {/* LEFT COLUMN: Input Form */}
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full xl:w-[50%] bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] overflow-hidden flex flex-col"
            >
                <div className="p-6 border-b border-[#E5E7EB]">
                    <h2 className="text-lg font-semibold text-[#111111] tracking-tight">Message Analyzer</h2>
                    <p className="text-sm text-[#6B7280] mt-1">Scan WhatsApp, Telegram, LinkedIn, or Email messages for scams.</p>
                </div>

                <form onSubmit={handleScan} className="p-6 flex flex-col gap-5 flex-1">
                    <div>
                        <label className="block text-xs font-semibold text-[#111111] mb-1.5">Message Source</label>
                        <select 
                            value={source}
                            onChange={(e) => setSource(e.target.value)}
                            className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-2.5 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none"
                        >
                            <option value="WhatsApp">WhatsApp</option>
                            <option value="Telegram">Telegram</option>
                            <option value="LinkedIn">LinkedIn</option>
                            <option value="Email">Email</option>
                            <option value="SMS">SMS</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>

                    <div className="flex-1 flex flex-col">
                        <label className="block text-xs font-semibold text-[#111111] mb-1.5">Paste Message Here</label>
                        <textarea 
                            required 
                            value={message} 
                            onChange={e=>setMessage(e.target.value)} 
                            className="w-full bg-[#FFFFFF] border border-[#E5E7EB] rounded-lg px-3 py-3 text-sm focus:ring-1 focus:ring-[#111111] focus:border-[#111111] transition-all outline-none flex-1 min-h-[300px] resize-none" 
                            placeholder="e.g., 'Hello! We are hiring for part time online work. You can earn ₹5000 daily from home. Reply to start...'"
                        ></textarea>
                    </div>

                    <div className="pt-4 mt-2">
                        <button 
                            type="submit" 
                            disabled={loading || !message.trim()}
                            className="w-full flex items-center justify-center gap-2 bg-[#111111] hover:bg-black text-white font-medium py-3 px-4 rounded-lg transition-colors disabled:opacity-50"
                        >
                            {loading ? (
                                <div className="w-4 h-4 border-2 border-[#FFFFFF]/30 border-t-[#FFFFFF] rounded-full animate-spin"></div>
                            ) : (
                                <><Search className="w-4 h-4" /> Analyze Message</>
                            )}
                        </button>
                    </div>
                </form>
            </motion.div>

            {/* RIGHT COLUMN: Results */}
            <div className="w-full xl:w-[50%] flex flex-col gap-6">
                <AnimatePresence mode="wait">
                    {!result && !loading ? (
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="bg-[#FFFFFF] rounded-[18px] p-10 shadow-sm border border-[#E5E7EB] flex flex-col items-center justify-center text-center h-[460px]"
                        >
                            <div className="w-16 h-16 bg-[#F5F5F4] rounded-full flex items-center justify-center mb-4">
                                <MessageSquare className="w-6 h-6 text-[#6B7280]" />
                            </div>
                            <h3 className="text-base font-semibold text-[#111111]">Scan Social Messages</h3>
                            <p className="text-sm text-[#6B7280] max-w-[280px] mt-2">Paste suspicious DMs, SMS, or emails. We'll extract URLs, analyze the text, and detect phishing attempts instantly.</p>
                        </motion.div>
                    ) : null}

                    {loading && (
                        <motion.div 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="bg-[#FFFFFF] rounded-[18px] p-10 shadow-sm border border-[#E5E7EB] flex flex-col items-center justify-center text-center h-[460px]"
                        >
                            <div className="w-12 h-12 mb-6 relative">
                                <div className="absolute inset-0 border-2 border-[#E5E7EB] rounded-full"></div>
                                <div className="absolute inset-0 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
                            </div>
                            <h3 className="text-base font-semibold text-[#111111]">Scanning Message...</h3>
                            <p className="text-sm text-[#6B7280] mt-2">Checking heuristics, TF-IDF vectors, and risk patterns.</p>
                        </motion.div>
                    )}

                    {result && !loading && (
                        <motion.div 
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex flex-col gap-6"
                        >
                            {/* Score Card */}
                            <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col items-center relative overflow-hidden">
                                
                                <div className="absolute top-0 left-0 w-full h-1" style={{ backgroundColor: getRiskColor(result.risk) }}></div>
                                
                                <h2 className="text-sm font-semibold text-[#111111] mb-6">AI Threat Score</h2>
                                
                                {/* Circular Progress */}
                                <div className="relative w-36 h-36 flex items-center justify-center mb-6">
                                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                                        <circle cx="50" cy="50" r="45" fill="none" stroke="#F5F5F4" strokeWidth="6" />
                                        <motion.circle 
                                            initial={{ strokeDasharray: "0 282.7" }}
                                            animate={{ strokeDasharray: `${(result.probability / 100) * 282.7} 282.7` }}
                                            transition={{ duration: 1.2, ease: "easeOut" }}
                                            cx="50" cy="50" r="45" 
                                            fill="none" 
                                            stroke={getRiskColor(result.risk)}
                                            strokeWidth="6" 
                                            strokeLinecap="round"
                                        />
                                    </svg>
                                    <div className="absolute flex flex-col items-center">
                                        <span className="text-3xl font-bold text-[#111111]">{result.probability.toFixed(0)}%</span>
                                    </div>
                                </div>

                                <div className="px-3 py-1 rounded border text-xs font-semibold flex items-center gap-1.5"
                                     style={{ 
                                         backgroundColor: `${getRiskColor(result.risk)}10`, 
                                         color: getRiskColor(result.risk),
                                         borderColor: `${getRiskColor(result.risk)}30`
                                     }}>
                                    {result.risk === 'High Risk' ? <XCircle className="w-3.5 h-3.5"/> : result.risk === 'Medium Risk' ? <AlertTriangle className="w-3.5 h-3.5" /> : <CheckCircle2 className="w-3.5 h-3.5"/>}
                                    {result.prediction}
                                </div>
                            </div>

                            {/* Details Card */}
                            <div className="bg-[#FFFFFF] rounded-[18px] p-8 shadow-sm border border-[#E5E7EB] flex flex-col gap-6">
                                
                                {/* Explanation */}
                                <div>
                                    <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">AI Explanation</h3>
                                    <p className="text-sm text-[#111111] leading-relaxed bg-[#F5F5F4] p-4 rounded-lg border border-[#E5E7EB]">
                                        {result.explanation}
                                    </p>
                                </div>

                                {/* Warning Flags */}
                                {result.warning_flags && result.warning_flags.length > 0 && (
                                    <div>
                                        <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-3">Detected Red Flags</h3>
                                        <div className="space-y-2">
                                            {result.warning_flags.map((flag: string, i: number) => (
                                                <div key={i} className="flex items-start gap-2 bg-[#DC2626]/5 p-3 rounded-md border border-[#DC2626]/20">
                                                    <AlertTriangle className="w-4 h-4 text-[#DC2626] shrink-0 mt-0.5" />
                                                    <span className="text-xs font-medium text-[#DC2626] leading-tight">{flag.replace("⚠️", "")}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Recommendation */}
                                <div>
                                    <h3 className="text-xs font-semibold text-[#6B7280] uppercase tracking-wider mb-2">Recommended Action</h3>
                                    <div className="p-4 rounded-md border text-sm flex items-center gap-3"
                                         style={{ 
                                            backgroundColor: `${getRiskColor(result.risk)}05`, 
                                            color: getRiskColor(result.risk),
                                            borderColor: `${getRiskColor(result.risk)}30`
                                         }}>
                                        <Info className="w-4 h-4 shrink-0" />
                                        <span className="font-medium">{result.recommended_action}</span>
                                    </div>
                                </div>

                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
