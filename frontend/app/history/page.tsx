"use client";

import { useEffect, useState } from "react";
import { format } from "date-fns";
import { 
  Trash2, 
  Download, 
  Search,
  Filter,
  MoreVertical,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle
} from "lucide-react";

type ScanRecord = {
  id: number;
  title: string;
  company: string;
  prediction: string;
  probability: number;
  risk: string;
  source: string;
  created_at: string;
};

export default function HistoryPage() {
  const [history, setHistory] = useState<ScanRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/history?limit=100");
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (err) {
      console.error("Failed to fetch history", err);
    } finally {
      setLoading(false);
    }
  }

  async function deleteRecord(id: number) {
    if (!confirm("Are you sure you want to delete this record?")) return;
    
    try {
      const res = await fetch(`http://127.0.0.1:8000/history/${id}`, {
        method: "DELETE"
      });
      if (res.ok) {
        setHistory(history.filter(record => record.id !== id));
      }
    } catch (err) {
      console.error("Failed to delete record", err);
    }
  }

  function exportCSV() {
    const headers = ["ID", "Title", "Company", "Prediction", "Probability", "Risk", "Source", "Date"];
    const csvContent = [
      headers.join(","),
      ...history.map(row => 
        [
          row.id, 
          `"${row.title.replace(/"/g, '""')}"`, 
          `"${row.company.replace(/"/g, '""')}"`, 
          row.prediction, 
          row.probability, 
          row.risk, 
          row.source, 
          row.created_at
        ].join(",")
      )
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `jobx_history_${format(new Date(), "yyyyMMdd")}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const filteredHistory = history.filter(record => 
    record.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    record.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
    record.risk.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto pb-12 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">Scan History</h1>
          <p className="mt-1 text-sm text-gray-500">View and manage all your past AI analyses.</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input 
              type="text"
              placeholder="Search history..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-black w-64"
            />
          </div>
          <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-600 transition-colors tooltip" title="Filter">
            <Filter size={18} />
          </button>
          <button 
            onClick={exportCSV}
            className="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
          >
            <Download size={16} />
            Export CSV
          </button>
        </div>
      </div>

      <div className="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="flex h-64 items-center justify-center">
             <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-black"></div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Job / Source</th>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Risk Level</th>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Fraud Prob.</th>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
                  <th scope="col" className="relative px-6 py-4">
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-100">
                {filteredHistory.length > 0 ? (
                  filteredHistory.map((record) => (
                    <tr key={record.id} className="hover:bg-gray-50/50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex flex-col">
                          <span className="text-sm font-semibold text-gray-900">{record.title}</span>
                          <span className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                            {record.source === 'Message' ? 'Message Analysis' : record.company}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <RiskBadge risk={record.risk} />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                           <span className="text-sm font-medium text-gray-900">{record.probability}%</span>
                           <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                              <div 
                                className={`h-full ${record.risk === 'High Risk' ? 'bg-red-500' : record.risk === 'Medium Risk' ? 'bg-orange-500' : 'bg-emerald-500'}`} 
                                style={{ width: `${record.probability}%` }}
                              />
                           </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {format(new Date(record.created_at), "MMM d, yyyy h:mm a")}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button 
                          onClick={() => deleteRecord(record.id)}
                          className="text-gray-400 hover:text-red-600 transition-colors p-1"
                          title="Delete record"
                        >
                          <Trash2 size={18} />
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                      No records found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function RiskBadge({ risk }: { risk: string }) {
  if (risk === "High Risk") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200">
        <ShieldAlert size={12} />
        {risk}
      </span>
    );
  }
  if (risk === "Medium Risk") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800 border border-orange-200">
        <AlertTriangle size={12} />
        {risk}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
      <ShieldCheck size={12} />
      {risk}
    </span>
  );
}
