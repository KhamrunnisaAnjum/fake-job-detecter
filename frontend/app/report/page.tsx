"use client";
<<<<<<< HEAD

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Bar,
} from "recharts";

const pieData = [
  { name: "Safe", value: 78 },
  { name: "Medium", value: 15 },
  { name: "High", value: 7 },
];

const weeklyData = [
  { day: "Mon", scans: 120 },
  { day: "Tue", scans: 180 },
  { day: "Wed", scans: 160 },
  { day: "Thu", scans: 240 },
  { day: "Fri", scans: 210 },
  { day: "Sat", scans: 190 },
  { day: "Sun", scans: 260 },
];

const COLORS = ["#22c55e", "#facc15", "#ef4444"];

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-[#F6F7FB] p-10">
      <div className="max-w-7xl mx-auto">
        <p className="uppercase tracking-[4px] text-sm text-neutral-500">
          JobX
        </p>

        <h1 className="mt-2 text-5xl font-bold">Risk Distribution</h1>

        <div className="grid grid-cols-4 gap-6 mt-10">
          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <h3 className="text-neutral-500">Jobs Scanned</h3>
            <h2 className="mt-3 text-4xl font-bold">15,482</h2>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <h3 className="text-neutral-500">Safe</h3>
            <h2 className="mt-3 text-4xl font-bold text-green-600">78%</h2>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <h3 className="text-neutral-500">Medium</h3>
            <h2 className="mt-3 text-4xl font-bold text-yellow-500">15%</h2>
          </div>

          <div className="rounded-3xl bg-white p-6 shadow-sm">
            <h3 className="text-neutral-500">High</h3>
            <h2 className="mt-3 text-4xl font-bold text-red-500">7%</h2>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8 mt-10">
          <div className="rounded-3xl bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold mb-8">Risk Percentage</h2>

            <ResponsiveContainer width="100%" height={320}>
              <PieChart>
                <Pie data={pieData} dataKey="value" outerRadius={120} label>
                  {pieData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index]} />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="rounded-3xl bg-white p-8 shadow-sm">
            <h2 className="text-2xl font-bold mb-8">Weekly Scans</h2>

            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="day" />

                <YAxis />

                <Tooltip />

                <Bar dataKey="scans" fill="#111827" radius={[10, 10, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
=======
import { apiFetch } from "@/utils/api";

import { useEffect, useState } from "react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart, 
  Pie, 
  Cell,
  LineChart,
  Line,
  Legend
} from "recharts";
import { BarChart3, TrendingUp, PieChart as PieChartIcon } from "lucide-react";

type ReportsData = {
  distribution: { name: string; value: number }[];
  scans_over_time: { date: string; count: number }[];
  high_risk_trend: { date: string; high_risk_count: number }[];
};

const COLORS = {
  "High Risk": "#ef4444",   // red-500
  "Medium Risk": "#f97316", // orange-500
  "Low Risk": "#10b981",    // emerald-500
};

export default function ReportsPage() {
  const [data, setData] = useState<ReportsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchReports() {
      try {
        const res = await apiFetch("http://127.0.0.1:8000/reports");
        if (res.ok) {
          const json = await res.json();
          setData(json);
        }
      } catch (err) {
        console.error("Failed to fetch reports", err);
      } finally {
        setLoading(false);
      }
    }

    fetchReports();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto pb-12 animate-in fade-in duration-500">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">Analytics & Reports</h1>
          <p className="mt-1 text-sm text-gray-500">Visual insights based on your AI detection history.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        
        {/* Scans Over Time */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm flex flex-col h-96">
            <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
                <BarChart3 className="text-blue-500" size={20} /> 
                Scans Over Time (Last 14 Days)
            </h2>
            <div className="flex-1 w-full">
              {data?.scans_over_time && data.scans_over_time.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data.scans_over_time} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                    <XAxis 
                        dataKey="date" 
                        axisLine={false} 
                        tickLine={false} 
                        tick={{ fontSize: 12, fill: '#6b7280' }} 
                        dy={10}
                    />
                    <YAxis 
                        axisLine={false} 
                        tickLine={false} 
                        tick={{ fontSize: 12, fill: '#6b7280' }} 
                    />
                    <Tooltip 
                        cursor={{fill: '#f9fafb'}}
                        contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Bar dataKey="count" fill="#111827" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-sm text-gray-400">No data available</div>
              )}
            </div>
        </div>

        {/* Risk Distribution */}
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm flex flex-col h-96">
            <h2 className="text-lg font-semibold text-gray-900 mb-2 flex items-center gap-2">
                <PieChartIcon className="text-purple-500" size={20} /> 
                Risk Distribution
            </h2>
            <div className="flex-1 w-full flex items-center justify-center">
               {data?.distribution && data.distribution.some(d => d.value > 0) ? (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={data.distribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={80}
                      outerRadius={110}
                      paddingAngle={5}
                      dataKey="value"
                      stroke="none"
                    >
                      {data.distribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[entry.name as keyof typeof COLORS] || "#000"} />
                      ))}
                    </Pie>
                    <Tooltip 
                        contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Legend verticalAlign="bottom" height={36} iconType="circle" />
                  </PieChart>
                </ResponsiveContainer>
               ) : (
                <div className="h-full flex items-center justify-center text-sm text-gray-400">No data available</div>
               )}
            </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm h-96 flex flex-col">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
             <TrendingUp className="text-red-500" size={20} />
             High Risk Trend (Last 14 Days)
          </h2>
          <div className="flex-1 w-full">
            {data?.high_risk_trend && data.high_risk_trend.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data.high_risk_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                        <XAxis 
                            dataKey="date" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fontSize: 12, fill: '#6b7280' }} 
                            dy={10}
                        />
                        <YAxis 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fontSize: 12, fill: '#6b7280' }} 
                        />
                        <Tooltip 
                            contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Line 
                            type="monotone" 
                            dataKey="high_risk_count" 
                            name="High Risk Scans"
                            stroke="#ef4444" 
                            strokeWidth={3}
                            dot={{ r: 4, strokeWidth: 2 }}
                            activeDot={{ r: 6 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            ) : (
                <div className="h-full flex items-center justify-center text-sm text-gray-400">No data available</div>
            )}
          </div>
      </div>
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
    </div>
  );
}
