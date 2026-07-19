"use client";
import { apiFetch } from "@/utils/api";

import { useEffect, useState } from "react";
import { format } from "date-fns";
import { motion, AnimatePresence } from "framer-motion";
import { 
    Search, 
    Trash2, 
    Download,
    ChevronRight,
    ChevronDown
} from "lucide-react";

export default function HistoryPage() {
    const [scans, setScans] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [filterRisk, setFilterRisk] = useState("All Scan Alerts");
    const [expandedId, setExpandedId] = useState<number | null>(null);

    const fetchHistory = async () => {
        try {
            const res = await apiFetch("http://127.0.0.1:8000/history?limit=100");
            if (res.ok) setScans(await res.json());
        } catch (error) {
            console.error("Failed to fetch history");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        let interval: NodeJS.Timeout;
        fetchHistory();
        interval = setInterval(fetchHistory, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleDelete = async (id: number, e: React.MouseEvent) => {
        e.stopPropagation();
        if(!confirm("Are you sure you want to delete this log?")) return;
        
        try {
            const res = await apiFetch(`http://127.0.0.1:8000/history/${id}`, { method: "DELETE" });
            if (res.ok) {
                setScans(prev => prev.filter(s => s.id !== id));
                if(expandedId === id) setExpandedId(null);
            }
        } catch (error) {
            console.error("Failed to delete");
        }
    };

    const exportCSV = () => {
        const headers = ["ID", "Title", "Company", "Source", "Risk", "Score", "Date"];
        const rows = scans.map(s => {
            const comp = s.source === "Paste" ? "N/A" : s.company;
            return [
                s.id, `"${s.title.replace(/"/g, '""')}"`, `"${comp.replace(/"/g, '""')}"`, s.source, s.risk, `${s.probability}%`, s.created_at
            ];
        });
        const csvContent = "data:text/csv;charset=utf-8," 
            + headers.join(",") + "\n" 
            + rows.map(e => e.join(",")).join("\n");
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "JOBX_history.csv");
        document.body.appendChild(link);
        link.click();
    };

    const filteredScans = scans.filter(s => {
        const matchesSearch = s.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
                              s.company.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesFilter = filterRisk === "All Scan Alerts" || s.risk === filterRisk;
        return matchesSearch && matchesFilter;
    });

    const getRiskColors = (risk: string) => {
        if (risk === "High Risk") return { text: "#DC2626", bg: "#FEF2F2", border: "#DC2626" }; // Red
        if (risk === "Medium Risk") return { text: "#D97706", bg: "#FFFBEB", border: "#F59E0B" }; // Amber/Orange
        return { text: "#16A34A", bg: "#F0FDF4", border: "#16A34A" }; // Green
    };

    const toggleExpand = (id: number) => {
        setExpandedId(prev => prev === id ? null : id);
    };

    return (
        <div className="w-full max-w-5xl mx-auto flex flex-col gap-8 pb-12">
            
            {/* Header Section */}
            <div>
                <h1 className="text-3xl font-bold text-[#111111] tracking-tight">My Scan History</h1>
                <p className="text-sm text-[#6B7280] mt-2">All your private job scan records — only visible to you.</p>
            </div>

            {/* Search & Filter Card */}
            <div className="bg-[#FFFFFF] rounded-2xl border border-[#E5E7EB] p-6">
                <div className="flex items-center gap-2 mb-4">
                    <Search className="w-5 h-5 text-[#6B7280]" />
                    <h2 className="text-base font-semibold text-[#111111]">Search & Filter</h2>
                </div>
                <p className="text-sm text-[#6B7280] mb-6">Filter your personal scan logs</p>

                <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
                    {/* Search Bar */}
                    <div className="relative w-full md:w-1/2">
                        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]" />
                        <input 
                            type="text"
                            placeholder="Search by title..."
                            value={searchTerm}
                            onChange={e => setSearchTerm(e.target.value)}
                            className="w-full pl-9 pr-4 py-2.5 bg-[#F9FAFB] border border-[#E5E7EB] rounded-lg text-sm focus:ring-2 focus:ring-[#111111] focus:border-transparent text-[#111111] outline-none transition-all"
                        />
                    </div>

                    {/* Filter Dropdown */}
                    <select
                        value={filterRisk}
                        onChange={e => setFilterRisk(e.target.value)}
                        className="w-full md:w-1/3 py-2.5 px-4 bg-[#F9FAFB] border border-[#E5E7EB] rounded-lg text-sm text-[#111111] focus:ring-2 focus:ring-[#111111] outline-none transition-all appearance-none cursor-pointer"
                        style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 24 24\' stroke=\'%236B7280\'%3E%3Cpath stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'2\' d=\'M19 9l-7 7-7-7\'%3E%3C/path%3E%3C/svg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 1rem center', backgroundSize: '1em' }}
                    >
                        <option value="All Scan Alerts">All Scan Alerts</option>
                        <option value="High Risk">High Risk</option>
                        <option value="Medium Risk">Medium Risk</option>
                        <option value="Low Risk">Low Risk</option>
                    </select>

                    {/* Export Button */}
                    <button 
                        onClick={exportCSV} 
                        className="w-full md:w-auto px-6 py-2.5 border border-[#E5E7EB] bg-[#FFFFFF] hover:bg-[#F9FAFB] text-[#111111] font-medium rounded-lg text-sm flex items-center justify-center gap-2 transition-colors shrink-0"
                    >
                        ⬇ Export CSV
                    </button>
                </div>
            </div>

            {/* History List */}
            <div className="flex flex-col gap-3">
                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className="w-8 h-8 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
                    </div>
                ) : filteredScans.length === 0 ? (
                    <div className="text-center py-12 bg-[#FFFFFF] border border-[#E5E7EB] rounded-2xl">
                        <p className="text-[#6B7280] text-sm">No scan records found.</p>
                    </div>
                ) : (
                    filteredScans.map(scan => {
                        const isExpanded = expandedId === scan.id;
                        const colors = getRiskColors(scan.risk);
                        
                        return (
                            <div 
                                key={scan.id} 
                                className="bg-[#FFFFFF] border border-[#E5E7EB] rounded-xl overflow-hidden transition-all duration-200"
                            >
                                {/* Collapsed Header Area */}
                                <div 
                                    onClick={() => toggleExpand(scan.id)}
                                    className="flex items-center p-4 cursor-pointer hover:bg-[#F9FAFB] transition-colors relative"
                                >
                                    {/* Left colored border indicator */}
                                    <div 
                                        className="absolute left-0 top-0 bottom-0 w-1.5"
                                        style={{ backgroundColor: colors.border }}
                                    />
                                    
                                    <div className="pl-3 pr-2 text-[#9CA3AF]">
                                        {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                                    </div>
                                    
                                    <div className="flex-1 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 ml-1">
                                        <p className="text-sm font-medium text-[#111111] line-clamp-1 flex-1">
                                            {scan.title}
                                        </p>
                                        <p className="text-sm text-[#6B7280] shrink-0">
                                            — {scan.risk} · {scan.probability}% · {format(new Date(scan.created_at), 'yyyy-MM-dd HH:mm')}
                                        </p>
                                    </div>
                                </div>

                                {/* Expanded Content Area */}
                                <AnimatePresence>
                                    {isExpanded && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: "auto", opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            transition={{ duration: 0.2 }}
                                            className="border-t border-[#E5E7EB] bg-[#FFFFFF]"
                                        >
                                            <div className="p-6 md:p-8 flex flex-col gap-6 relative">
                                                
                                                {/* Delete Button (Top Right) */}
                                                <div className="absolute top-6 right-6">
                                                    <button 
                                                        onClick={(e) => handleDelete(scan.id, e)}
                                                        className="px-3 py-1.5 border border-[#E5E7EB] rounded-md text-xs font-medium text-[#6B7280] hover:text-[#DC2626] hover:bg-[#FEF2F2] hover:border-[#FECACA] transition-all flex items-center gap-1.5"
                                                    >
                                                        <Trash2 className="w-3.5 h-3.5" />
                                                        Delete
                                                    </button>
                                                </div>

                                                {/* Core Stats Row */}
                                                <div className="flex flex-col gap-4 max-w-sm">
                                                    <div className="flex items-center gap-2">
                                                        <span className="text-sm font-semibold text-[#111111] w-12">Risk:</span>
                                                        <span 
                                                            className="px-2.5 py-0.5 rounded-full text-xs font-medium"
                                                            style={{ backgroundColor: colors.bg, color: colors.text }}
                                                        >
                                                            {scan.risk}
                                                        </span>
                                                    </div>

                                                    <div>
                                                        <div className="flex items-center gap-2 mb-2">
                                                            <span className="text-sm font-semibold text-[#111111] w-12">Score:</span>
                                                            <span className="text-sm text-[#111111]">{scan.probability}%</span>
                                                        </div>
                                                        <div className="w-full h-1.5 bg-[#F3F4F6] rounded-full overflow-hidden">
                                                            <div 
                                                                className="h-full rounded-full transition-all duration-500"
                                                                style={{ width: `${scan.probability}%`, backgroundColor: colors.border }}
                                                            />
                                                        </div>
                                                    </div>

                                                    <div className="flex items-center gap-2 mt-2">
                                                        <span className="text-sm font-semibold text-[#111111] w-12">Mode:</span>
                                                        <span className="px-2 py-0.5 bg-[#F3F4F6] text-[#4B5563] text-xs font-medium rounded">
                                                            {scan.source.toLowerCase()}
                                                        </span>
                                                    </div>
                                                </div>



                                                {/* AI Explanation / Details */}
                                                {scan.explanation && (
                                                    <div className="mt-2">
                                                        <h4 className="text-sm font-semibold text-[#111111] mb-2">AI Analysis:</h4>
                                                        <p className="text-sm text-[#4B5563] leading-relaxed">
                                                            {scan.explanation}
                                                        </p>
                                                    </div>
                                                )}

                                                {/* Flags */}
                                                {scan.warning_flags && scan.warning_flags.length > 0 && (
                                                    <div className="mt-2">
                                                        <h4 className="text-sm font-semibold text-[#111111] mb-3">Detected Indicators:</h4>
                                                        <ul className="flex flex-col gap-2">
                                                            {scan.warning_flags.map((flag: string, idx: number) => (
                                                                <li key={idx} className="flex items-start gap-2 text-sm text-[#4B5563]">
                                                                    <span className="text-[#DC2626] mt-0.5">•</span>
                                                                    <span>{flag.replace("⚠️", "").trim()}</span>
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                )}

                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        );
                    })
                )}
            </div>

        </div>
    );
}
