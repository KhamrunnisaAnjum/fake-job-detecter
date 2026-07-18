"use client";

import { useState } from "react";
import { 
  Moon, 
  Sun, 
  Trash2, 
  Download, 
  User, 
  Mail, 
  Shield,
  Check
} from "lucide-react";
import { format } from "date-fns";

export default function SettingsPage() {
  const [darkMode, setDarkMode] = useState(false);
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const [clearing, setClearing] = useState(false);

  // In a real app, we'd delete via backend. Here we just pretend if we had a clear endpoint, 
  // or we could implement a DELETE /history/all endpoint.
  // We'll just show the UI for now as requested.

  const handleClearHistory = async () => {
    setClearing(true);
    // simulated delay
    await new Promise(r => setTimeout(r, 1000));
    setClearing(false);
    setShowClearConfirm(false);
    alert("History cleared successfully.");
  };

  const handleExport = async () => {
    // In a real app, this might trigger a download of the SQLite DB or a full CSV dump
    try {
      const res = await fetch("http://127.0.0.1:8000/history?limit=10000");
      if (res.ok) {
        const history = await res.json();
        const headers = ["ID", "Title", "Company", "Prediction", "Probability", "Risk", "Source", "Date"];
        const csvContent = [
          headers.join(","),
          ...history.map((row: any) => 
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
        link.setAttribute("download", `jobx_full_export_${format(new Date(), "yyyyMMdd")}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to export database.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto pb-12 animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-500">Manage your preferences, account, and data.</p>
      </div>

      <div className="space-y-8">
        
        {/* User Profile */}
        <section className="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <User className="mr-2 h-5 w-5 text-gray-500" /> User Profile
          </h2>
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
            <div className="h-20 w-20 rounded-full bg-gray-100 flex items-center justify-center border-2 border-dashed border-gray-300">
               <span className="text-2xl font-bold text-gray-400">U</span>
            </div>
            <div className="flex-1 space-y-4 w-full">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                <input type="text" defaultValue="Admin User" className="w-full sm:max-w-md rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-black" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1 flex items-center gap-2">
                    <Mail size={14} /> Email Address
                </label>
                <input type="email" defaultValue="admin@jobx.ai" className="w-full sm:max-w-md rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-black bg-gray-50 text-gray-500" disabled />
              </div>
            </div>
          </div>
          <div className="mt-6">
            <button className="px-4 py-2 bg-black text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
                Save Changes
            </button>
          </div>
        </section>

        {/* Appearance */}
        <section className="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Appearance</h2>
          <div className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
             <div>
                 <p className="font-medium text-gray-900">Dark Mode</p>
                 <p className="text-sm text-gray-500">Toggle dark mode theme for the dashboard.</p>
             </div>
             <button 
                onClick={() => setDarkMode(!darkMode)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2 ${darkMode ? 'bg-black' : 'bg-gray-200'}`}
             >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${darkMode ? 'translate-x-6' : 'translate-x-1'}`} />
             </button>
          </div>
          <div className="mt-4 flex gap-4">
              <button 
                onClick={() => setDarkMode(false)} 
                className={`flex-1 flex flex-col items-center justify-center p-4 border rounded-xl transition-all ${!darkMode ? 'border-black bg-gray-50' : 'border-gray-200 hover:border-gray-300'}`}
              >
                  <Sun size={24} className={!darkMode ? 'text-black' : 'text-gray-400'} />
                  <span className={`mt-2 text-sm font-medium ${!darkMode ? 'text-black' : 'text-gray-500'}`}>Light</span>
              </button>
              <button 
                onClick={() => setDarkMode(true)} 
                className={`flex-1 flex flex-col items-center justify-center p-4 border rounded-xl transition-all ${darkMode ? 'border-black bg-gray-50' : 'border-gray-200 hover:border-gray-300'}`}
              >
                  <Moon size={24} className={darkMode ? 'text-black' : 'text-gray-400'} />
                  <span className={`mt-2 text-sm font-medium ${darkMode ? 'text-black' : 'text-gray-500'}`}>Dark</span>
              </button>
          </div>
        </section>

        {/* Data Management */}
        <section className="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm border-l-4 border-l-red-500">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Shield className="mr-2 h-5 w-5 text-red-500" /> Data & Privacy
          </h2>
          
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 border border-gray-200 rounded-xl gap-4">
                <div>
                    <p className="font-medium text-gray-900">Export Database</p>
                    <p className="text-sm text-gray-500 max-w-md">Download all scan history records in CSV format for offline analysis.</p>
                </div>
                <button 
                    onClick={handleExport}
                    className="flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors shrink-0"
                >
                    <Download size={16} /> Export Data
                </button>
            </div>

            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 border border-red-100 bg-red-50 rounded-xl gap-4">
                <div>
                    <p className="font-medium text-red-900">Clear History</p>
                    <p className="text-sm text-red-700 max-w-md">Permanently delete all scan records from the database. This action cannot be undone.</p>
                </div>
                {!showClearConfirm ? (
                    <button 
                        onClick={() => setShowClearConfirm(true)}
                        className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 transition-colors shrink-0"
                    >
                        <Trash2 size={16} /> Clear All
                    </button>
                ) : (
                    <div className="flex items-center gap-2 shrink-0">
                        <button 
                            onClick={() => setShowClearConfirm(false)}
                            className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900"
                        >
                            Cancel
                        </button>
                        <button 
                            onClick={handleClearHistory}
                            disabled={clearing}
                            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
                        >
                            {clearing ? "Clearing..." : "Yes, Delete"}
                        </button>
                    </div>
                )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
