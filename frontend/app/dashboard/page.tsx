"use client";
import { apiFetch } from "@/utils/api";

import { useEffect, useState } from "react";
import { formatDistanceToNow, format } from "date-fns";
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell,
  LineChart,
  Line,
  PieChart,
  Pie,
  AreaChart,
  Area,
  BarChart,
  Bar,
  Legend
} from "recharts";
import { 
    Activity, 
    ShieldAlert, 
    ShieldCheck, 
    AlertTriangle,
    ArrowUpRight,
    Search,
    FileText,
    Download,
    Calendar,
    Clock,
    AlertCircle
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [report, setReport] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    async function fetchData() {
      try {
        const [statsRes, reportsRes, historyRes] = await Promise.all([
            apiFetch("http://127.0.0.1:8000/stats"),
            apiFetch("http://127.0.0.1:8000/reports"),
            apiFetch("http://127.0.0.1:8000/history?limit=10")
        ]);
        
        if(statsRes.ok) setStats(await statsRes.json());
        if(reportsRes.ok) setReport(await reportsRes.json());
        if(historyRes.ok) setHistory(await historyRes.json());
      } catch (error) {
        console.error("Failed to fetch dashboard data", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
      return (
          <div className="flex items-center justify-center h-[60vh] w-full">
              <div className="w-6 h-6 border-2 border-[#111111] border-t-transparent rounded-full animate-spin"></div>
          </div>
      );
  }

  const safeStats = stats || { total_scans: 0, high_risk: 0, medium_risk: 0, low_risk: 0, today_scans: 0, average_score: 0, latest_threats: [] };
  const safeReport = report || { distribution: [], scans_over_time: [], high_risk_trend: [] };
  const CHART_COLORS = ['#DC2626', '#F59E0B', '#16A34A']; // Danger, Warning, Success

  const mergedActivity = safeReport.scans_over_time.map((item: any) => {
      const hr = safeReport.high_risk_trend.find((h: any) => h.date === item.date);
      const hCount = hr ? hr.high_risk_count : 0;
      
      const dateObj = new Date(item.date);
      const shortMonth = dateObj.toLocaleDateString('en-US', { month: 'short' });
      
      return {
          date: shortMonth,
          "Safe Scans": item.count - hCount,
          "High Risk": hCount
      };
  });

  const exportAnalyticsPDF = () => {
      let token = null;
      const cookies = document.cookie.split(';');
      for (let c of cookies) {
          const [k, v] = c.trim().split('=');
          if (k === 'jobx_token') token = v;
      }
      fetch(`http://localhost:8000/api/analytics/pdf`, {
          method: "GET",
          headers: {
              "Authorization": `Bearer ${token}`
          }
      })
      .then(res => {
          if(!res.ok) throw new Error("Export failed");
          return res.blob();
      })
      .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "jobx_analytics.pdf";
          document.body.appendChild(a);
          a.click();
          a.remove();
      })
      .catch(err => alert("Failed to download PDF"));
  };

  return (
    <div className="w-full flex flex-col gap-8">
        {/* Page Header */}
        <div className="flex justify-between items-center mb-2">
            <div>
                <h1 className="text-3xl font-bold tracking-tight text-[#111111]">Dashboard</h1>
                <p className="text-sm text-[#6B7280] mt-1">Overview of your threat detection metrics</p>
            </div>
            <div className="flex gap-3">
                <button 
                    onClick={exportAnalyticsPDF}
                    className="bg-[#FFFFFF] border border-[#E5E7EB] hover:bg-[#F9FAFB] text-[#111111] text-sm font-medium py-2.5 px-5 rounded-lg transition-colors flex items-center gap-2"
                >
                    <Download className="w-4 h-4" />
                    Analytics PDF
                </button>
                <Link href="/scan">
                    <button className="bg-[#111111] hover:bg-black text-white text-sm font-medium py-2.5 px-5 rounded-lg transition-colors flex items-center gap-2">
                        <Search className="w-4 h-4" />
                        New Scan
                    </button>
                </Link>
            </div>
        </div>

        {/* ROW 1: 4 EQUAL STATS CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard title="Total Scans" value={safeStats.total_scans} trend="+12%" icon={Activity} />
            <StatCard title="High Risk Threats" value={safeStats.high_risk} trend="+3%" icon={ShieldAlert} />
            <StatCard title="Today's Volume" value={safeStats.today_scans} trend="+8%" icon={AlertTriangle} />
            <StatCard title="Avg Fraud Score" value={`${safeStats.average_score}%`} trend="-2%" icon={ShieldCheck} />
        </div>

        {/* ROW 2: FRAUD TREND & RISK TIMELINE (2 cols each) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Risk Timeline Replaced by Activity Feed */}
            <div className="bg-[#FFFFFF] rounded-2xl p-6 border border-[#E5E7EB] shadow-sm flex flex-col h-[400px]">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-sm font-semibold text-[#111111]">Activity feed</h2>
                    <Link href="/history" className="text-xs font-semibold text-[#F59E0B] hover:text-orange-600 flex items-center gap-1">
                        <ArrowUpRight className="w-3.5 h-3.5" /> Assign New Task
                    </Link>
                </div>
                <div className="flex-1 overflow-y-auto pr-1 space-y-4 no-scrollbar">
                    {history.slice(0, 10).map((item) => {
                        let colorHex = '#10B981'; // Green
                        if (item.risk === 'High Risk') colorHex = '#DC2626'; // Red
                        if (item.risk === 'Medium Risk') colorHex = '#F59E0B'; // Orange

                        return (
                            <div key={item.id} className="bg-white border border-[#E5E7EB] rounded-sm overflow-hidden flex flex-col relative shadow-sm hover:shadow-md transition-shadow">
                                {/* Left Color Border */}
                                <div className="absolute left-0 top-0 bottom-0 w-1.5" style={{ backgroundColor: colorHex }}></div>
                                
                                <div className="flex items-center p-3 pl-5">
                                    {/* Donut Chart */}
                                    <div className="w-12 h-12 relative shrink-0 mr-4">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie
                                                    data={[{ value: item.probability }, { value: 100 - item.probability }]}
                                                    cx="50%" cy="50%"
                                                    innerRadius={18} outerRadius={24}
                                                    startAngle={90} endAngle={-270}
                                                    dataKey="value"
                                                    stroke="none"
                                                >
                                                    <Cell fill={colorHex} />
                                                    <Cell fill="#F3F4F6" />
                                                </Pie>
                                            </PieChart>
                                        </ResponsiveContainer>
                                        <div className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-[#111111]">
                                            {item.probability}%
                                        </div>
                                    </div>
                                    
                                    {/* Middle Content */}
                                    <div className="flex-1 min-w-0">
                                        <h3 className="text-sm font-bold text-[#374151] truncate">
                                            {item.title}
                                        </h3>
                                        <p className="text-[11px] text-[#6B7280] truncate mt-0.5">
                                            {item.company || "Unknown Sender"}
                                        </p>
                                        <div className="flex items-center gap-3 mt-1.5 text-[10px] text-[#9CA3AF]">
                                            <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {format(new Date(item.created_at), 'dd.MM.yyyy')}</span>
                                            <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {format(new Date(item.created_at), 'hh:mm a')}</span>
                                        </div>
                                    </div>
                                    
                                    {/* Right Icon */}
                                    <div className="flex flex-col items-center justify-center pl-3 pr-2 shrink-0 min-w-[50px]">
                                        <ShieldCheck className={`w-5 h-5 mb-1 ${item.prediction === 'Fake' ? 'text-[#DC2626]' : 'text-[#10B981]'}`} />
                                        <span className="text-[9px] text-[#9CA3AF] font-medium">{item.prediction}</span>
                                    </div>
                                </div>
                                
                                {/* Bottom Bar */}
                                <div className="bg-[#F9FAFB] border-t border-[#E5E7EB] flex items-center h-9">
                                    <div className="flex-1 flex items-center gap-2 pl-6">
                                        <AlertCircle className="w-3.5 h-3.5" style={{ color: colorHex }} />
                                        <span className="text-[11px] font-bold" style={{ color: colorHex }}>{item.risk}</span>
                                    </div>
                                    <div className="flex-1 flex items-center justify-start gap-2 border-l border-[#E5E7EB] pl-4 h-full cursor-pointer hover:bg-[#F3F4F6] transition-colors" onClick={() => window.location.href = '/reports'}>
                                        <div className="w-3.5 h-3.5 rounded-full bg-[#10B981] flex items-center justify-center">
                                            <div className="w-1.5 h-1.5 bg-white rounded-full"></div>
                                        </div>
                                        <span className="text-[11px] font-bold text-[#374151]">View Report</span>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
                <div className="mt-4 pt-3 border-t border-[#E5E7EB] text-center">
                    <Link href="/history" className="text-xs font-semibold text-[#F59E0B] hover:text-orange-600">
                        Load more items in activity feed
                    </Link>
                </div>
            </div>

            {/* Scan Activity - Bar Chart */}
            <div className="bg-[#FFFFFF] rounded-2xl p-6 border border-[#E5E7EB] shadow-sm flex flex-col">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-sm font-semibold text-[#111111]">Scan Activity</h2>
                </div>
                <div className="flex-1 min-h-[260px] w-full -ml-4">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={mergedActivity} margin={{ top: 5, right: 10, left: -20, bottom: 0 }} barGap={4}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                            <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dy={10} />
                            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#6B7280' }} dx={-10} allowDecimals={false} />
                            <Tooltip cursor={{ fill: '#F5F5F4' }} contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }} />
                            <Legend wrapperStyle={{ fontSize: '12px', color: '#111111', fontWeight: 500, paddingBottom: '20px' }} iconType="circle" />
                            <Bar dataKey="Safe Scans" fill="#16A34A" radius={[6, 6, 6, 6]} barSize={14} />
                            <Bar dataKey="High Risk" fill="#DC2626" radius={[6, 6, 6, 6]} barSize={14} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>

        {/* ROW 2.5: RISK DIST (1 col), RECENT ACTIVITY (1 col), LATEST (2 col)? Actually let's put Risk Dist and Recent Activity in a 2-col layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Risk Distribution Chart - 1 Column */}
            <div className="lg:col-span-1 bg-[#FFFFFF] rounded-2xl p-6 border border-[#E5E7EB] shadow-sm flex flex-col justify-center">
                <h2 className="text-sm font-semibold text-[#111111] mb-4">Risk Status</h2>
                
                <div className="flex-1 w-full flex items-center justify-between mt-2">
                    {/* Left Side: Stats Grid */}
                    <div className="w-1/2 grid grid-cols-2 gap-y-8 gap-x-2">
                        <div>
                            <div className="flex items-center gap-2 mb-1.5">
                                <div className="w-3 h-3 rounded-full bg-[#6366F1]"></div>
                                <span className="text-xs text-[#6B7280] font-medium">Total</span>
                            </div>
                            <p className="text-xl font-bold text-[#111111] ml-5">{safeStats.total_scans}</p>
                        </div>
                        <div>
                            <div className="flex items-center gap-2 mb-1.5">
                                <div className="w-3 h-3 rounded-full bg-[#DC2626]"></div>
                                <span className="text-xs text-[#6B7280] font-medium">High Risk</span>
                            </div>
                            <p className="text-xl font-bold text-[#111111] ml-5">{safeStats.high_risk}</p>
                        </div>
                        <div>
                            <div className="flex items-center gap-2 mb-1.5">
                                <div className="w-3 h-3 rounded-full bg-[#F59E0B]"></div>
                                <span className="text-xs text-[#6B7280] font-medium">Medium</span>
                            </div>
                            <p className="text-xl font-bold text-[#111111] ml-5">{safeStats.medium_risk}</p>
                        </div>
                        <div>
                            <div className="flex items-center gap-2 mb-1.5">
                                <div className="w-3 h-3 rounded-full bg-[#10B981]"></div>
                                <span className="text-xs text-[#6B7280] font-medium">Low Risk</span>
                            </div>
                            <p className="text-xl font-bold text-[#111111] ml-5">{safeStats.low_risk}</p>
                        </div>
                    </div>

                    {/* Right Side: Donut */}
                    <div className="w-1/2 relative h-[180px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={safeReport.distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={55}
                                    outerRadius={80}
                                    paddingAngle={2}
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {safeReport.distribution.map((entry: any, index: number) => {
                                        let color = '#111111';
                                        if (entry.name === 'High Risk') color = '#DC2626';
                                        if (entry.name === 'Medium Risk') color = '#F59E0B';
                                        if (entry.name === 'Low Risk') color = '#10B981';
                                        return <Cell key={`cell-${index}`} fill={color} />;
                                    })}
                                </Pie>
                                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }} />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                            <span className="text-2xl font-bold text-[#111111]">100%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Activity Panel - 1 Column */}
            <div className="lg:col-span-1 bg-[#FFFFFF] rounded-2xl p-6 border border-[#E5E7EB] shadow-sm flex flex-col">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-sm font-semibold text-[#111111]">Recent Activity</h2>
                    <Link href="/history" className="text-xs font-medium text-[#6B7280] hover:text-[#111111]">View all</Link>
                </div>
                <div className="flex-1 overflow-y-auto space-y-5 no-scrollbar">
                    {history.slice(0, 6).map((item) => (
                        <div key={item.id} className="flex gap-3 items-start">
                            <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${item.risk === 'High Risk' ? 'bg-[#DC2626]' : item.risk === 'Medium Risk' ? 'bg-[#F59E0B]' : 'bg-[#16A34A]'}`}></div>
                            <div>
                                <p className="text-sm text-[#111111] font-medium leading-tight line-clamp-1">{item.title}</p>
                                <p className="text-xs text-[#6B7280] mt-1">{formatDistanceToNow(new Date(item.created_at))} ago</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

        </div>

        {/* ROW 3: LATEST HIGH RISK SCANS (FULL WIDTH TABLE) */}
        <div className="bg-[#FFFFFF] rounded-2xl border border-[#E5E7EB] shadow-sm overflow-hidden">
            <div className="px-6 py-5 border-b border-[#E5E7EB] flex justify-between items-center">
                <h2 className="text-sm font-semibold text-[#111111]">Latest High-Risk Scans</h2>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm whitespace-nowrap">
                    <thead className="bg-[#F5F5F4] text-[#6B7280] border-b border-[#E5E7EB]">
                        <tr>
                            <th className="px-6 py-4 font-medium">Job Title</th>
                            <th className="px-6 py-4 font-medium">Company</th>
                            <th className="px-6 py-4 font-medium">Score</th>
                            <th className="px-6 py-4 font-medium">Status</th>
                            <th className="px-6 py-4 font-medium text-right">Date</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E5E7EB]">
                        {safeStats.latest_threats.map((threat: any) => (
                            <tr key={threat.id} className="hover:bg-[#F5F5F4]/50 transition-colors cursor-pointer">
                                <td className="px-6 py-4 font-medium text-[#111111]">{threat.title}</td>
                                <td className="px-6 py-4 text-[#6B7280]">{threat.company || "N/A"}</td>
                                <td className="px-6 py-4">
                                    <span className="font-semibold text-[#DC2626]">{threat.probability}%</span>
                                </td>
                                <td className="px-6 py-4">
                                    <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-[#DC2626]/10 text-[#DC2626] border border-[#DC2626]/20">
                                        High Risk
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-right text-[#6B7280]">
                                    {formatDistanceToNow(new Date(threat.created_at))} ago
                                </td>
                            </tr>
                        ))}
                        {safeStats.latest_threats.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-12 text-center text-[#6B7280]">No high risk threats detected.</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>

        {/* ROW 4: RECENT PREDICTIONS (50%) & RECENT REPORTS (50%) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Recent Predictions */}
            <div className="bg-[#FFFFFF] rounded-2xl border border-[#E5E7EB] shadow-sm overflow-hidden flex flex-col">
                <div className="px-6 py-5 border-b border-[#E5E7EB] flex justify-between items-center bg-[#FFFFFF]">
                    <h2 className="text-sm font-semibold text-[#111111]">Recent Predictions</h2>
                    <Link href="/history" className="text-xs font-medium text-[#6B7280] hover:text-[#111111]">View all</Link>
                </div>
                <div className="divide-y divide-[#E5E7EB]">
                    {history.slice(0, 5).map((item) => (
                        <div key={item.id} className="flex justify-between items-center p-6 hover:bg-[#F5F5F4]/50 transition-colors">
                            <div>
                                <p className="text-sm font-medium text-[#111111]">{item.title}</p>
                                <p className="text-xs text-[#6B7280] mt-1">{item.company || item.source}</p>
                            </div>
                            <div className="text-right flex flex-col items-end">
                                <span className="text-sm font-semibold text-[#111111]">{item.probability}%</span>
                                <span className={`text-xs font-medium mt-1 ${item.risk === 'High Risk' ? 'text-[#DC2626]' : item.risk === 'Medium Risk' ? 'text-[#F59E0B]' : 'text-[#16A34A]'}`}>
                                    {item.risk}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recent Reports */}
            <div className="bg-[#FFFFFF] rounded-2xl border border-[#E5E7EB] shadow-sm overflow-hidden flex flex-col">
                <div className="px-6 py-5 border-b border-[#E5E7EB] flex justify-between items-center bg-[#FFFFFF]">
                    <h2 className="text-sm font-semibold text-[#111111]">Generated Reports</h2>
                    <Link href="/reports" className="text-xs font-medium text-[#6B7280] hover:text-[#111111]">View Analytics</Link>
                </div>
                <div className="divide-y divide-[#E5E7EB]">
                    {safeReport.scans_over_time.slice(-5).reverse().map((reportItem: any, idx: number) => (
                        <div key={idx} className="flex justify-between items-center p-6 hover:bg-[#F5F5F4]/50 transition-colors cursor-pointer">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-lg bg-[#F5F5F4] flex items-center justify-center border border-[#E5E7EB]">
                                    <FileText className="w-5 h-5 text-[#6B7280]" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-[#111111]">Daily Summary Report</p>
                                    <p className="text-xs text-[#6B7280] mt-1">{format(new Date(reportItem.date), 'MMMM do, yyyy')}</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-[#111111]/5 text-[#111111] border border-[#111111]/10">
                                    {reportItem.count} Scans
                                </span>
                            </div>
                        </div>
                    ))}
                    {safeReport.scans_over_time.length === 0 && (
                        <div className="p-12 text-center text-[#6B7280] text-sm">
                            No reports generated yet.
                        </div>
                    )}
                </div>
            </div>

        </div>
    </div>
  );
}

function StatCard({ title, value, trend, icon: Icon }: any) {
    return (
        <div className="bg-[#FFFFFF] rounded-2xl p-6 border border-[#E5E7EB] shadow-sm flex flex-col justify-between h-[140px]">
            <div className="flex justify-between items-start">
                <p className="text-sm font-medium text-[#6B7280]">{title}</p>
                <div className="w-8 h-8 rounded-lg bg-[#F5F5F4] flex items-center justify-center">
                    <Icon className="w-4 h-4 text-[#111111]" />
                </div>
            </div>
            <div className="flex items-baseline gap-3 mt-auto">
                <h3 className="text-3xl font-bold tracking-tight text-[#111111]">{value}</h3>
                <span className="text-sm font-medium text-[#16A34A] flex items-center bg-[#16A34A]/10 px-2 py-0.5 rounded-full border border-[#16A34A]/20">
                    <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
                    {trend}
                </span>
            </div>
        </div>
    );
}
