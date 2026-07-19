"use client";

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
    </div>
  );
}
