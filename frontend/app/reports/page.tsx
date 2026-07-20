"use client";
import { apiFetch } from "@/utils/api";

import { useEffect, useState } from "react";
import { 
  PieChart, 
  Pie, 
  Cell, 
  Tooltip as RechartsTooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";
import { motion } from "framer-motion";
import { Download, PieChart as PieChartIcon } from "lucide-react";

export default function ReportsPage() {
    const [report, setReport] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let interval: NodeJS.Timeout;
        async function fetchReports() {
            try {
                const res = await apiFetch("http://127.0.0.1:8000/reports");
                if (res.ok) {
                    setReport(await res.json());
                }
            } catch (error) {
                console.error("Failed to fetch reports");
            } finally {
                setLoading(false);
            }
        }
        fetchReports();
        interval = setInterval(fetchReports, 5000); // Real-Time Polling
        return () => clearInterval(interval);
    }, []);

    const exportPDF = () => {
        let token = null;
        const cookies = document.cookie.split(';');
        for (let c of cookies) {
            const [k, v] = c.trim().split('=');
            if (k === 'jobx_token') token = v;
        }
        
        fetch(`http://localhost:8000/api/reports/pdf`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(res => res.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "jobx_analytics.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(err => alert("Failed to download PDF"));
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full min-h-[400px]">
                <div className="w-6 h-6 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    const defaultReport = report || { distribution: [], scans_over_time: [], high_risk_trend: [] };
    const CHART_COLORS = ['#DC2626', '#F59E0B', '#16A34A']; // Danger, Warning, Success

    return (
        <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full flex flex-col gap-6"
        >
            <div className="flex justify-between items-center bg-[#FFFFFF] rounded-[18px] shadow-sm border border-[#E5E7EB] p-8">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-[#F5F5F4] rounded-lg flex items-center justify-center border border-[#E5E7EB]">
                        <PieChartIcon className="w-6 h-6 text-[#111111]" />
                    </div>
                    <div>
                        <h1 className="text-xl font-semibold text-[#111111] tracking-tight">Analytics & Reports</h1>
                        <p className="text-sm text-[#6B7280] mt-1">Deep insights into your threat detection data.</p>
                    </div>
                </div>
                <button onClick={exportPDF} className="flex items-center gap-2 bg-[#FFFFFF] border border-[#E5E7EB] text-[#111111] font-medium py-2 px-4 rounded-md hover:bg-[#F5F5F4] transition-colors text-sm shadow-sm">
                    <Download className="w-4 h-4" /> Export PDF
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                {/* Risk Distribution Pie Chart */}
                <div className="bg-[#FFFFFF] rounded-[18px] p-6 shadow-sm border border-[#E5E7EB] flex flex-col">
                    <h2 className="text-sm font-semibold text-[#111111] mb-6">Overall Risk Distribution</h2>
                    <div className="h-[250px] w-full relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={defaultReport.distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={90}
                                    paddingAngle={3}
                                    dataKey="value"
                                >
                                    {defaultReport.distribution.map((entry: any, index: number) => (
                                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} stroke="transparent" />
                                    ))}
                                </Pie>
                                <RechartsTooltip 
                                    contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <span className="text-[10px] font-semibold text-[#6B7280] uppercase tracking-wider">Risk Level</span>
                        </div>
                    </div>
                    
                    <div className="flex justify-center gap-6 mt-6">
                        {defaultReport.distribution.map((entry: any, index: number) => (
                            <div key={index} className="flex items-center gap-2">
                                <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: CHART_COLORS[index % CHART_COLORS.length] }}></div>
                                <span className="text-xs font-medium text-[#6B7280]">{entry.name}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Scans Over Time Line Chart */}
                <div className="lg:col-span-2 flex flex-col gap-6">
                    
                    {/* Trend 1 */}
                    <div className="bg-[#FFFFFF] rounded-[18px] p-6 shadow-sm border border-[#E5E7EB] flex-1">
                        <h2 className="text-sm font-semibold text-[#111111] mb-6">Scan Activity Trend (Last 14 Days)</h2>
                        <div className="h-[180px] w-full -ml-4">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={defaultReport.scans_over_time} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                    <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dy={10} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dx={-10} allowDecimals={false} />
                                    <RechartsTooltip cursor={{ stroke: '#E5E7EB', strokeWidth: 1 }} contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }} />
                                    <Line type="monotone" dataKey="count" stroke="#111111" strokeWidth={2} dot={{ r: 3, fill: '#111111' }} activeDot={{ r: 5 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Trend 2 */}
                    <div className="bg-[#FFFFFF] rounded-[18px] p-6 shadow-sm border border-[#E5E7EB] flex-1">
                        <h2 className="text-sm font-semibold text-[#111111] mb-6 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-[#DC2626]"></span>
                            High Risk Trend
                        </h2>
                        <div className="h-[180px] w-full -ml-4">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={defaultReport.high_risk_trend} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                    <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dy={10} />
                                    <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dx={-10} allowDecimals={false} />
                                    <RechartsTooltip cursor={{ stroke: '#E5E7EB', strokeWidth: 1 }} contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }} />
                                    <Line type="monotone" dataKey="high_risk_count" stroke="#DC2626" strokeWidth={2} dot={{ r: 3, fill: '#DC2626' }} activeDot={{ r: 5 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                </div>
            </div>

        </motion.div>
    );
}
