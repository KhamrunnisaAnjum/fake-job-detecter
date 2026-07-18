"use client";

import { useEffect, useState } from "react";
import { 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  Search, 
  Activity,
  ArrowUpRight,
  Clock
} from "lucide-react";
import { format } from "date-fns";

type Threat = {
  title: string;
  company: string;
  probability: number;
  created_at: string;
};

type Stats = {
  total_scans: number;
  high_risk: number;
  medium_risk: number;
  low_risk: number;
  latest_threats: Threat[];
};

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await fetch("http://127.0.0.1:8000/stats");
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (err) {
        console.error("Failed to fetch stats", err);
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
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
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">Overview of your AI scan activity and detected threats.</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500 bg-white px-4 py-2 rounded-full border border-gray-200 shadow-sm">
          <Activity size={16} className="text-green-500 animate-pulse" />
          System Online
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <MetricCard 
          title="Total Scans" 
          value={stats?.total_scans || 0} 
          icon={<Search size={24} className="text-blue-500" />} 
          trend="+12% from last week"
        />
        <MetricCard 
          title="High Risk" 
          value={stats?.high_risk || 0} 
          icon={<ShieldAlert size={24} className="text-red-500" />} 
          trend="Critical threats stopped"
        />
        <MetricCard 
          title="Medium Risk" 
          value={stats?.medium_risk || 0} 
          icon={<AlertTriangle size={24} className="text-orange-500" />} 
          trend="Needs verification"
        />
        <MetricCard 
          title="Low Risk" 
          value={stats?.low_risk || 0} 
          icon={<ShieldCheck size={24} className="text-emerald-500" />} 
          trend="Safe applications"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
           <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Latest Critical Threats</h2>
              <button className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center">
                  View All <ArrowUpRight size={16} className="ml-1" />
              </button>
           </div>
           
           <div className="overflow-x-auto">
             <table className="min-w-full divide-y divide-gray-200">
               <thead>
                 <tr>
                   <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Title</th>
                   <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                   <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fraud Prob.</th>
                   <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-gray-100">
                 {stats?.latest_threats && stats.latest_threats.length > 0 ? (
                    stats.latest_threats.map((threat, idx) => (
                        <tr key={idx} className="hover:bg-gray-50 transition-colors">
                            <td className="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{threat.title}</td>
                            <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{threat.company}</td>
                            <td className="px-4 py-4 whitespace-nowrap text-sm">
                                <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                    {threat.probability}%
                                </span>
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500 text-right">
                                {format(new Date(threat.created_at), "MMM d, h:mm a")}
                            </td>
                        </tr>
                    ))
                 ) : (
                    <tr>
                        <td colSpan={4} className="px-4 py-8 text-center text-sm text-gray-500">
                            No recent threats detected.
                        </td>
                    </tr>
                 )}
               </tbody>
             </table>
           </div>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">System Status</h2>
            <div className="space-y-6">
                <StatusItem icon={<Search className="text-blue-500" />} label="ML Model" status="Active (v2.1)" />
                <StatusItem icon={<Activity className="text-green-500" />} label="Rule Engine" status="Online (15 rules)" />
                <StatusItem icon={<Clock className="text-orange-500" />} label="Last Database Sync" status="2 mins ago" />
                
                <div className="pt-6 border-t border-gray-100">
                    <p className="text-xs text-gray-500 mb-2">Resource Usage</p>
                    <div className="flex justify-between items-end mb-1">
                        <span className="text-sm font-medium text-gray-700">CPU</span>
                        <span className="text-xs text-gray-500">12%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5 mb-4">
                        <div className="bg-black h-1.5 rounded-full" style={{ width: '12%' }}></div>
                    </div>
                    
                    <div className="flex justify-between items-end mb-1">
                        <span className="text-sm font-medium text-gray-700">Memory</span>
                        <span className="text-xs text-gray-500">42%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5">
                        <div className="bg-black h-1.5 rounded-full" style={{ width: '42%' }}></div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon, trend }: { title: string, value: number, icon: React.ReactNode, trend: string }) {
    return (
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
                <div className="p-2.5 bg-gray-50 rounded-xl">
                    {icon}
                </div>
                <span className="text-xs font-medium text-gray-500 bg-gray-50 px-2 py-1 rounded-md">{title}</span>
            </div>
            <div>
                <h3 className="text-3xl font-bold text-gray-900 mb-1">{value.toLocaleString()}</h3>
                <p className="text-xs text-gray-500">{trend}</p>
            </div>
        </div>
    )
}

function StatusItem({ icon, label, status }: { icon: React.ReactNode, label: string, status: string }) {
    return (
        <div className="flex items-center">
            <div className="p-2 bg-gray-50 rounded-lg mr-3">
                {icon}
            </div>
            <div>
                <p className="text-sm font-medium text-gray-900">{label}</p>
                <p className="text-xs text-gray-500">{status}</p>
            </div>
        </div>
    )
}
